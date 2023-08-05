'''Tools for building AppImages.'''
__all__ = ['FlatpakBuilder']
from subprocess import Popen, PIPE, run
from os import system, makedirs, chmod, stat, chdir, getcwd, walk
from os.path import abspath, join, isabs, exists
from shutil import rmtree, copy, copytree, move
from urllib.request import urlretrieve
from json import dumps
from logging import info
from stat import S_IEXEC
from glob import glob
from textwrap import dedent
from pathlib import Path
from fnmatch import fnmatch
import sys


class FlatpakBuilder:
    '''This class provides tools for building Flatpak repositories.'''

    def __init__(self, cmd, app_id, repo_path, gpg_sign, gpg_homedir,
                 url, exclude=None, branch='stable', dirs=None):
        '''The constructor.

        Arguments:
        cmd -- the instance of the Panda3D's bdist_apps command.
        app_id -- the app_id of your application e.g. org.panda3d.Asteroids)
        repo_path -- the local path to the repo
            e.g. /home/you/asteroids/flatpak
        gpg_sign -- the if of your key e.g. D43B6D...B5
        gpg_homedir -- the path of your key e.g. /home/you/asteroids/gpg
        url -- the url of the published repo
        exclude -- the files that you want to ignore e.g. ['options*.ini']
        branch -- the branch of this build
        dirs -- the directories that you want in the repo e.g. ['assets']'''
        self._cmd = cmd
        self._name = cmd.distribution.get_name()
        self._exclude = exclude or []
        self._branch = branch
        self._app_id = app_id
        self._url = url
        self._dirs = dirs or []
        self._repo_path = repo_path
        self._gpg_sign = gpg_sign
        self._gpg_homedir = gpg_homedir

    def build(self):
        '''Builds a Flatpak repository.'''
        build_cmd = self._cmd.distribution.get_command_obj('build_apps')
        build_base = abspath(build_cmd.build_base)
        bld_dir = join(build_base, 'manylinux2010_x86_64')
        flatpak_dir = join(build_base, 'flatpak')
        rmtree(flatpak_dir, ignore_errors=True)
        copytree(bld_dir, flatpak_dir)
        with InsideDir(flatpak_dir):
            self.__do_flatpak()

    def __do_flatpak(self):
        name = self._cmd.distribution.get_name().lower()
        build_cmd = self._cmd.distribution.get_command_obj('build_apps')
        dst = abspath(build_cmd.build_base)
        files = []
        rmtree('built', ignore_errors=True)
        rmtree('.flatpak-builder/build', ignore_errors=True)
        for root, _, files_ in walk('.'):
            if len(root.split('/')) == 1 or not root.split('/')[1].startswith('.'):
                for file_ in files_:
                    if not any(fnmatch(file_, exclude) for exclude in self._exclude):
                        files += [root[2:] + ('/' if len(root) > 1 else '') +
                                  file_]
        modules_lst = []
        for dir_ in self._dirs:
            modules_lst += [{'name': dir_,
                             'buildsystem': 'simple',
                             'build-commands': ['install -d ' + dir_],
                             'sources': []}]
        modules_lst += [
            {'name': name,
             'buildsystem': 'simple',
             'build-commands': ['install -D %s /app/bin/%s' % (name, name)],
             'sources': [{'type': 'file', 'path': name}]}]
        json = {
            'app-id': self._app_id,
            'branch': self._branch,
            'default-branch': 'stable',
            'runtime': 'org.freedesktop.Platform',
            'runtime-version': '20.08',
            'sdk': 'org.freedesktop.Sdk',
            'command': name,
            'modules': modules_lst,
            'finish-args': [
                '--socket=x11', '--share=network', '--share=ipc',
                '--device=dri', '--filesystem=host',
                '--socket=pulseaudio', '--env=PYTHONPATH=/app/bin']}
        for file_ in files:
            enc_file = file_.replace('/', '____')
            cmd = 'install -D "%s" "/app/bin/%s"' % (enc_file, file_)
            json['modules'][0]['build-commands'] += [cmd]
            json['modules'][0]['sources'] += [
                {'type': 'file', 'path': file_, 'dest-filename': enc_file}]
        with open(self._app_id + '.json', 'w') as fjson:
            fjson.write(dumps(json))
        cmd = ('flatpak-builder --gpg-sign=%s --gpg-homedir=%s '
               '--repo=%s --force-clean --disable-rofiles-fuse '
               'built %s.json') % (
                   self._gpg_sign, self._gpg_homedir,
                   self._repo_path, self._app_id)
        info(cmd)
        system(cmd)
        cmd = ('flatpak build-sign %s --gpg-sign=%s --gpg-homedir=%s') % (
            self._repo_path, self._gpg_sign, self._gpg_homedir)
        info(cmd)
        system(cmd)
        cmd = ('flatpak build-update-repo %s --gpg-sign=%s '
               '--gpg-homedir=%s') % (
            self._repo_path, self._gpg_sign, self._gpg_homedir)
        dist_dir = self._cmd.dist_dir
        build_cmd = self._cmd.distribution.get_command_obj('build_apps')
        build_base = abspath(build_cmd.build_base)
        system('gpg2 --homedir=%s --export %s > %s' % (
            self._gpg_homedir,
            self._gpg_sign,
            join(build_base, 'flatpak_key.gpg')))
        key_cmd = "base64 %s | tr -d '\n'" % join(build_base, 'flatpak_key.gpg')
        gpg_key = self.__exec_cmd(key_cmd)
        with open(join(dist_dir, '%s-%s.flatpakref' % (name, self._branch)), 'w') as f:
            tmpl = '''[Flatpak Ref]
            Name=%s
            Branch=%s
            Title=%s
            Url=%s
            RuntimeRepo=https://dl.flathub.org/repo/flathub.flatpakrepo
            IsRuntime=false
            GPGKey=%s'''
            fref = tmpl % (
                self._app_id,
                self._branch,
                self._app_id,
                self._url,
                gpg_key)
            f.write(dedent(fref))

    def __exec_cmd(self, cmd):
        '''Synchronously executes a command and returns its output.'''
        proc = run(cmd, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return proc.stdout.strip() + proc.stderr.strip()



class InsideDir:
    '''Context manager for temporarily working inside a directory.'''

    def __init__(self, dir_):
        self.dir = dir_
        self.old_dir = getcwd()

    def __enter__(self):
        chdir(self.dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        chdir(self.old_dir)
