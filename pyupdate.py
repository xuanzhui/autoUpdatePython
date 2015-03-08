#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xuanzhui'

import urllib.request
import re
import subprocess
from downloader import DownloadException,Downloader


#return filename
def retrievePkg(pkgurl):
    dn=Downloader(pkgurl)
    try:
        return dn.download(showProcess=True)
    except DownloadException as e:
        print('DownloadException:', e.reason)


def getPkgUrl():
    baseurl='https://www.python.org/downloads/mac-osx/'
    page = urllib.request.urlopen(baseurl).read()

    mat=re.search(b'(https://www.python.org/ftp/.*.pkg?)', page)
    if mat:
        pkgurl=mat.group(1)

        mat=re.search(b'python-(.*?)-', pkgurl)

        if mat:
            version=mat.group(1)
        else:
            version=None

        return version.decode(), pkgurl.decode()
    else:
        return None


#return True if local version is the same as the latest
def compareVersion(latestVer):
    output=subprocess.check_output(['python','--version'])
    mat=re.search(b'Python\s*(.*)', output)
    if mat:
        localVer=mat.group(1).decode()
        if localVer==latestVer:
            return True
        else:
            return False
    else:
        return False


def installPkg(pkgname):
    pass

version, pkgurl= getPkgUrl()
if not version:
    print('cannot auto determine latest version')
    exit(1)

if compareVersion(version):
    print('local version is the same as the latest, ignore this update')

#retrievePkg('https://www.python.org/ftp/python/3.4.3/python-3.4.3-macosx10.6.pkg')



