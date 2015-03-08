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

    baseurl = "https://www.python.org/downloads/%s/" % (subdir[rostype])

    #print(baseurl)

    page = urllib.request.urlopen(baseurl).read()

    if rostype=='Windows':
        if platform.architecture() and platform.architecture()[0] == '64bit':
            patn=b'(https://www.python.org/ftp/python/.*.amd64.msi?)'
        else:
            patn=b'(https://www.python.org/ftp/python/.*.msi?)'
    elif rostype=='Darwin':
        patn=b'(https://www.python.org/ftp/python/.*.pkg?)'
    else:
        patn=b'(https://www.python.org/ftp/python/.*.tar.xz?)'


    mat = re.search(patn, page)
    if mat:
        pkgurl = mat.group(1)

        mat = re.search(b'python/(.*?)/', pkgurl)

        if mat:
            version = mat.group(1)
        else:
            version = None

        return version.decode(), pkgurl.decode()
    else:
        return None


if __name__ == '__main__':
    '''
    for x in ['Windows', 'Linux', 'Darwin']:
        print(getPkgUrl(x))
    '''

    version, pkgurl = getPkgUrl()
    print('find latest version :', version)

'''
    absp=retrievePkg(pkgurl)
    print('file absolute path is :', absp)
'''
