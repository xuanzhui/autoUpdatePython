#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xuanzhui'

import sys
import re
import subprocess
import pydownload

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
    cmdl=['sudo','installer', '-pkg', pkgname, '-target', '/']
    p=subprocess.Popen(cmdl)
    p.wait()

if sys.platform!='darwin':
    print('ONLY Mac is supported')
    exit(0)

version, pkgurl= pydownload.getPkgUrl()
if not version:
    print('cannot auto determine latest version')
    exit(1)

print('find latest version :', version)

if compareVersion(version):
    print('local version is the same as the latest, ignore this update')

absp=pydownload.retrievePkg(pkgurl)
print('file downloaded at :', absp)

installPkg(absp)


