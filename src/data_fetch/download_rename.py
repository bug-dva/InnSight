#!/usr/bin/env python

"""
usage: python download_rename.py datalink.txt dataset/
every line in datalink.txt is a file address
the program will rename them by the info provided in according link
"""

from urllib.request import urlopen
import sys


def download(url, filename):
    data = urlopen(url).read()
    f = open(filename, 'wb')  # download the file, if exist, replace
    f.write(data)
    f.close()


def rename(url):
    data_info = url.split(".com/")[1]
    dataname = data_info.split("/")
    filename = dataname[0] + "_" + dataname[1] + "_" + dataname[2] + "_" + dataname[3] + "_" + dataname[5]
    return filename


if __name__ == '__main__':
    file = sys.argv[1]
    save_path = sys.argv[2]
    f = open(file, "r")
    for line in f.read().splitlines():
        print(line)
        try:
            download(line, save_path + rename(line))
        except Exception as e:
            print(e)
            print("Link unavailable")
            pass
