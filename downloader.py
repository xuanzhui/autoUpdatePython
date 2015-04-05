#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xuanzhui'

import sys
import os
import urllib.request
import time


class DownloadException(Exception):
    def __init__(self, reason):
        self.reason = reason


class Downloader:
    def __init__(self, path=None):
        self.path = path

    def setDownloadPath(self, path):
        self.path = path

    def chunkReport(self, bytesRead, totalSize, chunk, interval):
        percent = float(bytesRead) / totalSize
        percent = round(percent * 100, 2)

        if interval == 0:
            interval = 0.000001

        sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)  speed (%0.2f) kB/s                  \r" %
                         (bytesRead, totalSize, percent, chunk / interval / 1024))

        if bytesRead >= totalSize:
            sys.stdout.write('\n')

    def readChunkToFile(self, response, filename, chunkSize=102400, reportHook=False):
        totalSize = response.getheader('Content-Length')

        if not totalSize:
            if reportHook:
                print('can NOT determine total size, will download without hint')
            with open(filename, 'wb') as fw:
                fw.write(response.read())
            return True

        totalSize=totalSize.strip()
        totalSize = int(totalSize)
        bytesRead = 0

        with open(filename, 'wb') as fw:
            while 1:
                if reportHook:
                    stime = time.time()
                    # print(stime)

                chunk = response.read(chunkSize)
                fw.write(chunk)

                if reportHook:
                    etime = time.time()
                    # print(etime)

                bytesRead += len(chunk)

                if not chunk:
                    break

                if reportHook:
                    self.chunkReport(bytesRead, totalSize, len(chunk), etime - stime)

        return bytesRead == totalSize

    def download(self, checkperSize=102400, showProcess=False):
        if not self.path:
            raise DownloadException('download path not set!')

        idx = self.path.rfind('/')
        if not idx:
            raise DownloadException('illegal path!')

        filename = self.path[idx + 1:]

        resp = urllib.request.urlopen(self.path)

        if not self.readChunkToFile(resp, filename, chunkSize=checkperSize,reportHook=showProcess):
            raise DownloadException('file is not fully retrieved!')

        return os.path.abspath(filename)


if __name__ == '__main__':
    #dn = Downloader('http://img2.ph.126.net/5Fko2oCImsGp2V9eoh-7JA==/6598141790494356305.jpg')
    #absp=dn.download(True)

    dn = Downloader('http://www.valentina-db.com/de/studio/download/current/vstudio_mac_32?format=raw')
    absp=dn.download(checkperSize=10240, showProcess=True)
    print('downloaded file path:',absp)
