#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xuanzhui'

import sys
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

        sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)  speed (%0.2f) kB/s\r" %
                         (bytesRead, totalSize, percent, chunk / interval / 1000))

        if bytesRead >= totalSize:
            sys.stdout.write('\n')

    def readChunkToFile(self, response, filename, chunkSize=102400, reportHook=False):
        totalSize = response.getheader('Content-Length').strip()
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

    def download(self, showProcess=False):
        if not self.path:
            raise DownloadException('download path not set!')

        idx = self.path.rfind('/')
        if not idx:
            raise DownloadException('illegal path!')

        filename = self.path[idx + 1:]

        resp = urllib.request.urlopen(self.path)

        if not self.readChunkToFile(resp, filename, reportHook=showProcess):
            raise DownloadException('file is not fully retrieved!')

        return filename


if __name__ == '__main__':
    dn = Downloader('https://www.python.org/ftp/python/3.4.3/python-3.4.3-macosx10.6.pkg')
    dn.download(True)