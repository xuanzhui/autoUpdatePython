#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xuanzhui'

import urllib.request
import platform
import re
from downloader import DownloadException, Downloader

# return filename
def retrievePkg(pkgurl):
    dn = Downloader(pkgurl)
    try:
        return dn.download(showProcess=True)
    except DownloadException as e:
        print('DownloadException:', e.reason)


def latestVersion():
    ss=urllib.request.urlopen('https://www.python.org/downloads/').read()

    sr=re.search(b'https://www.python.org/ftp/python/(.*?)/', ss)
    if sr:
        return sr.group(1).decode()
    else:
        return None

#ostype can be constants (Windows, Linux, Darwin)
#Darwin means Mac OS
def getPkgUrl(ostype=None):
    if not ostype:
        rostype = platform.system()
    else:
        rostype = ostype

    if rostype not in ['Windows', 'Linux', 'Darwin']:
        print('only "Windows", "Linux" and "Darwin"(Darwin means Mac OS) is support')
        exit(0)

    subdir = {'Windows': 'windows', 'Linux': 'source', 'Darwin': 'mac-osx'}

    version=latestVersion()

    if not version:
        print('can NOT determine latest version, exit now')
        exit(0)

    baseurl = "https://www.python.org/downloads/%s/" % (subdir[rostype])

    #print(baseurl)

    page = urllib.request.urlopen(baseurl).read()

    if rostype=='Windows':
        if platform.architecture() and platform.architecture()[0] == '64bit':
            patn="(https://www.python.org/ftp/python/%s/.*.amd64.msi?)" % version
        else:
            patn="(https://www.python.org/ftp/python/%s/.*.msi?)" % version
    elif rostype=='Darwin':
        patn="(https://www.python.org/ftp/python/%s/.*.pkg?)" % version
    else:
        patn="(https://www.python.org/ftp/python/%s/.*.tar.xz?)" % version

    patn=patn.encode()

    mat = re.search(patn, page)
    if mat:
        pkgurl = mat.group(1)

        return version, pkgurl.decode()
    else:
        return None


if __name__ == '__main__':

    for x in ['Windows', 'Linux', 'Darwin']:
        print(getPkgUrl(x))


'''
    version, pkgurl = getPkgUrl()
    print('find latest version :', version)
'''
'''
    absp=retrievePkg(pkgurl)
    print('file absolute path is :', absp)
'''
