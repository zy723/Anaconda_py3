#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class RenameFiles():
    def __init__(self):
        self.path = r'H:\教学视频'
        self.i = 0
        self.reWord = '【瑞客论坛 www.ruike1.com】'

    def renameFile(self, path=None):
        if path is None:
            filelist = self.path
        else:
            filelist = path

        total_num = len(filelist)
        for item in os.listdir(filelist):
            sChildPath = os.path.join(filelist, item)
            if os.path.isfile(sChildPath):
                src = os.path.join(os.path.abspath(filelist), item)
                if self.reWord in item:
                    dst = os.path.join(os.path.abspath(filelist), src.replace(self.reWord, ''))
                    os.rename(src, dst)
                    print('converting %s to %s ...' % (src, dst))
                    self.i += 1
            else:

                self.renameFile(sChildPath)

        print('total %d to rename & converted %d ' % (total_num, self.i))


if __name__ == '__main__':
    newname = RenameFiles()
    newname.renameFile()
