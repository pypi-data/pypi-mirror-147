'''Tools for building AppImages.'''
__all__ = ['AppImageBuilder']
from os import system, makedirs, chmod, stat, chdir, getcwd
from os.path import abspath, join, isabs
from shutil import rmtree, copy, copytree, move
from urllib.request import urlretrieve
from stat import S_IEXEC
from glob import glob
from textwrap import dedent
from pathlib import Path
import sys


apprun_content = '''#!/bin/sh
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${HERE}/usr/sbin/:${HERE}/usr/games/\
:${HERE}/bin/:${HERE}/sbin/${PATH:+:$PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/bin/:${HERE}/usr/lib/\
:${HERE}/usr/lib/i386-linux-gnu/:${HERE}/usr/lib/x86_64-linux-gnu/\
:${HERE}/usr/lib32/:${HERE}/usr/lib64/:${HERE}/lib/\
:${HERE}/lib/i386-linux-gnu/:${HERE}/lib/x86_64-linux-gnu/:${HERE}/lib32/\
:${HERE}/lib64/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONPATH="${HERE}/usr/bin/:${HERE}/usr/share/pyshared/${PYTHONPATH\
:+:$PYTHONPATH}"
export XDG_DATA_DIRS="${HERE}/usr/share/${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}"
export PERLLIB="${HERE}/usr/share/perl5/:${HERE}/usr/lib/perl5/${PERLLIB:+\
:$PERLLIB}"
export GSETTINGS_SCHEMA_DIR="${HERE}/usr/share/glib-2.0/schemas/\
${GSETTINGS_SCHEMA_DIR:+:$GSETTINGS_SCHEMA_DIR}"
export QT_PLUGIN_PATH="${HERE}/usr/lib/qt4/plugins/\
:${HERE}/usr/lib/i386-linux-gnu/qt4/plugins/\
:${HERE}/usr/lib/x86_64-linux-gnu/qt4/plugins/:${HERE}/usr/lib32/qt4/plugins/\
:${HERE}/usr/lib64/qt4/plugins/:${HERE}/usr/lib/qt5/plugins/\
:${HERE}/usr/lib/i386-linux-gnu/qt5/plugins/\
:${HERE}/usr/lib/x86_64-linux-gnu/qt5/plugins/:${HERE}/usr/lib32/qt5/plugins/\
:${HERE}/usr/lib64/qt5/plugins/${QT_PLUGIN_PATH:+:$QT_PLUGIN_PATH}"
EXEC=$(grep -e '^Exec=.*' "${HERE}"/*.desktop | head -n 1 | cut -d "=" -f 2 | \
cut -d " " -f 1)
exec "${EXEC}" "$@"'''


desktop_content_tmpl = '''[Desktop Entry]
Name=%s
Exec=%s
Icon=icon
Type=Application
Categories=Game;'''


class AppImageBuilder:
    '''This class provides tools for building and updating AppImages.'''

    def __init__(self, cmd):
        '''The constructor.

        Arguments:
        cmd -- the instance of the Panda3D's bdist_apps command.'''
        self._cmd = cmd
        self._name = cmd.distribution.get_name()

    def build(self, longname=None, branch='', zsync_path=None):
        '''Builds an AppImage.

        Arguments:
        longname -- you can specify a longer name if you need it (it will be
            used in the .desktop entry)
        branch -- you can specify a name for the branch (it will be used in the
            AppImage's filename)
        zsync_path -- if you specify it, then your AppImage can be updated with
            the build() method. You must upload the .zsync file there.
            e.g. https://www.yourdomain.com/downloads/'''
        build_cmd = self._cmd.distribution.get_command_obj('build_apps')
        build_base = abspath(build_cmd.build_base)
        dist_dir = self._cmd.dist_dir
        longname = longname or self._name
        dirname = self._name.capitalize() + '.AppDir'
        with InsideDir(build_base):
            rmtree(dirname, ignore_errors=True)
            makedirs(dirname)
        with InsideDir(build_base + '/' + dirname):
            with open('AppRun', 'w') as f_apprun: f_apprun.write(apprun_content)
            chmod('AppRun', stat('AppRun').st_mode | S_IEXEC)
            desktop_content = desktop_content_tmpl % (longname, self._name)
            with open(self._name.capitalize() + '.desktop', 'w') as fdesktop:
                fdesktop.write(desktop_content)
            if build_cmd.icons:
                ico_path = build_cmd.icons[self._name][0]
                if not isabs(ico_path):
                    prj_dir = Path(getcwd()).parent.parent.absolute()
                    ico_path = join(prj_dir, ico_path)
                copy(ico_path, './icon.png')
            else:
                Path('icon.svg').touch()
            copytree('%s/manylinux2010_x86_64' % build_base, './usr/bin')
            src = 'https://github.com/AppImage/AppImageUpdate/releases/' + \
                  'download/continuous/appimageupdatetool-x86_64.AppImage'
            dst = './usr/bin/appimageupdatetool-x86_64.AppImage'
            self._download(src, dst)  # for AppImage's self-updating
        with InsideDir(build_base):
            src = 'https://github.com/AppImage/AppImageKit/releases/' + \
                  'download/12/appimagetool-x86_64.AppImage'
            tool = 'appimagetool-x86_64.AppImage'
            self._download(src, tool)
            hbranch = ('-' + branch) if branch else ''
            tgt_name = '%s%s-x86_64.AppImage' % (self._name.capitalize(), hbranch)
            with open(dirname + '/usr/bin/appimage_name.txt', 'w') as fan:
                fan.write(tgt_name)
            with open(dirname + '/usr/bin/appimage_version.txt', 'w') as fav:
                fav.write(self._cmd.distribution.get_version())
            tmpl = './%s %s %s'
            cmd = tmpl % (tool, dirname, tgt_name)
            if zsync_path:
                tmpl = ' -u "zsync|%s%s%s-x86_64.AppImage.zsync"'
                cmd += tmpl % (zsync_path, self._name.capitalize(), hbranch)
            print(cmd)
            system(cmd)
            move(tgt_name, join(dist_dir, tgt_name))
            if zsync_path:
                move(tgt_name + '.zsync', join(dist_dir, tgt_name + '.zsync'))

    def _download(self, path, fname):
        '''Downloads the file referred by path into fname.'''
        urlretrieve(path, fname)
        chmod(fname, stat(fname).st_mode | S_IEXEC)

    def __redirect(self, callback):  # redirect output to console
        from os import ttyname  # here because it doesn't work on windows
        with open(ttyname(0), 'w') as fout:
            sys.stdout = fout
            callback(glob('/tmp/.mount_%s*' % self._name.capitalize())[0])

    def __update(self, _dir):
        print('Current version: ' + self.__get_ver(_dir))
        print('Update in progress...')
        with open(_dir + '/usr/bin/appimage_name.txt') as fname:
            name = fname.read().strip()
        system('appimageupdatetool-x86_64.AppImage ' + name)
        msg = '''\
            Update finished.
            Launch again with --version to check your version.'''
        print(dedent(msg))

    def __get_ver(self, _dir):
        with open(_dir + '/usr/bin/appimage_version.txt') as fver:
            return fver.read().strip()

    def update(self):
        '''Updates the AppImage.'''
        self.__redirect(self.__update)

    # def __print_ver(_dir):
    #     print(self.__get_ver(_dir))

    # def version(self):
    #     '''Prints the version of the current AppImage.'''
    #     self.__redirect(self.__print_ver)


class InsideDir:
    '''Context manager for temporarily working inside a directory.'''

    def __init__(self, dir_):
        self.dir = dir_
        self.old_dir = getcwd()

    def __enter__(self):
        chdir(self.dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        chdir(self.old_dir)
