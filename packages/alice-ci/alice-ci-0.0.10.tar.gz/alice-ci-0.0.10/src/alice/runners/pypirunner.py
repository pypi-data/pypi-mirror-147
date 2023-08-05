import json
import logging
import os
import re
import subprocess
import sys
from urllib import request, error
from pkg_resources import parse_version
from os import environ, path
from alice.runners.pyutils import PackageManager, glob, grab_from
from alice.exceptions import ConfigException, RunnerError


def get_uri(config, default):
    url = config.get("repo", {}).get("uri", default)
    if url is not None:
        if not re.match('(?:http|ftp|https)://', url):
            url = f"https://{url}"
    return url


def get_user(config, default):
    if "repo" in config:
        if "username" in config["repo"]:
            data = config["repo"]["username"]
            if isinstance(data, str):
                return data
            else:
                return grab_from(data)
    return default


def get_pass(config, default):
    if "repo" in config:
        if "password" in config["repo"]:
            data = config["repo"]["password"]
            if isinstance(data, str):
                return data
            else:
                return grab_from(data)
    return default


# Parses and stores the config from yaml
class PypiConfig:
    def __init__(self, config={}) -> None:
        self.workdir = path.abspath(config.get("workdir", "."))
        self.repo_uri = get_uri(config, None)
        self.repo_user = get_user(config, None)
        self.repo_pass = get_pass(config, None)
        self.packages = set(config.get("packages", []))
        self.upload = config.get("upload", False)
        self.fail_if_exists = config.get("fail_if_exists", False)

    # returns a PyPiConfig with merged values
    def copy(self, job_config={}):
        p = PypiConfig()
        p.workdir = path.abspath(path.join(self.workdir, job_config.get("workdir", ".")))
        p.repo_uri = get_uri(job_config, self.repo_uri)
        p.repo_user = get_user(job_config, self.repo_user)
        p.repo_pass = get_pass(job_config, self.repo_pass)
        job_pkg_set = set(job_config["packages"])
        job_pkg_set.update(self.packages)
        p.packages = job_pkg_set
        p.upload = job_config.get("upload", self.upload)
        p.fail_if_exists = job_config.get("fail_if_exists", self.fail_if_exists)
        return p


# TODO: consider "--skip-existing" flag for twine
class PyPiRunner():
    def __init__(self, config) -> None:
        logging.info("[PyPiRunner] Initializing")
        self.workdir = config["workdir"]
        self.config = PypiConfig(config)

    def __versions(self, repo, pkg_name):
        if repo is not None:
            url = f'{repo}/{pkg_name}/json'
        else:
            url = f"https://pypi.python.org/pypi/{pkg_name}/json"
        try:
            releases = json.loads(request.urlopen(url).read())['releases']
        except error.URLError as e:
            raise RunnerError(f"{url}: {e}")

        return sorted(releases, key=parse_version, reverse=True)

    def build(self, config, package):
        pkg_path = path.join(config.workdir, package)
        if not path.isdir(pkg_path):
            raise ConfigException(f"Path does not exists: {pkg_path}")
        command = [sys.executable, "-m", "build", package]
        with subprocess.Popen(command, cwd=config.workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            p.wait()
            if p.returncode != 0:
                print("STDOUT:")
                sys.stdout.buffer.write(p.stdout.read())
                print("STDERR:")
                sys.stdout.buffer.write(p.stderr.read())
                raise RunnerError(f"[PyPiRunner] Failed to build {package}")

    def find_unuploaded(self, repo, file_list, pkg_name):
        versions = self.__versions(repo, pkg_name)
        unuploaded = []
        for file in file_list:
            # flake8: noqa W605
            re_groups = re.findall("(\d*\.\d*\.\d*)", file)
            if len(re_groups) < 1:
                raise RunnerError(f"Unable to determine version of file {file}")
            file_version = re_groups[0]
            if file_version not in versions:
                unuploaded.append(file)
            else:
                print(f"[PyPiRunner] File already uploaded: {os.path.basename(file)}")
        return unuploaded


    def upload(self, config, package):
        command = [sys.executable, "-m", "twine", "upload", "--verbose"]
        if config.repo_uri is not None:
            command.append("--repository-url")
            command.append(config.repo_uri)
        if config.repo_user is not None:
            command.append("-u")
            command.append(config.repo_user)
        if config.repo_pass is not None:
            command.append("-p")
            command.append(config.repo_pass)
        
        dist_path = os.path.abspath(os.path.join(config.workdir, package, "dist"))
        files = glob(os.path.join(dist_path, "*"), config.workdir)
        for file in files:
            print(f"[PyPiRunner] Found: {file}")

        to_upload = self.find_unuploaded(config.repo_uri, files, package)
        if len(to_upload) == 0:
            return
        command += to_upload
        with subprocess.Popen(command, cwd=config.workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            p.wait()
            if p.returncode != 0:
                print("STDOUT:")
                sys.stdout.buffer.write(p.stdout.read())
                print("STDERR:")
                sys.stdout.buffer.write(p.stderr.read())
                raise RunnerError(f"[PyPiRunner] Failed to upload {package} ({p.returncode})")

    def run(self, job_spec):
        job_config = self.config.copy(job_spec)

        PackageManager.getInstance().ensure("build")
        for package in job_config.packages:
            print(f"[PyPiRunner] Building {package}")
            self.build(job_config, package)
            print(f"[PyPiRunner] Package {package} built")

        if job_config.upload:
            PackageManager.getInstance().ensure("twine")
            for package in job_config.packages:
                print(f"[PyPiRunner] Uploading {package}")
                self.upload(job_config, package)
        else:
            print(f"[PyPiRunner] Upload disabled, skiping")
