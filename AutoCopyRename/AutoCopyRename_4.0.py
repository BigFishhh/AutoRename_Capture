'''
Copyright: Copyright(c)2019
Createdon: 2019-11-26
Author: Penk
Version: 4.0
Title: 自动复制和重命名程序
'''

import ffmpeg
import sys
import os
import shutil
import threading

#=================获取视频信息================
def getinfo(path, VID):
    #运行ffmpeg probe
    probe = ffmpeg.probe(os.path.join(path, VID))
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type']), None)
    if video_stream is None:
        print('No video stream found', file=sys.stderr)
        sys.exit(1)

    #宽
    width = int(video_stream['width'])
    #高
    height = int(video_stream['height'])
    #帧率
    frames_rate = video_stream['avg_frame_rate']
    #转化为整数
    i = frames_rate.split('/')
    frames_rate = round(int(i[0]) / int(i[-1]))
    info = "{}×{}p_{}f_".format(width, height, frames_rate)
    #print(info)
    #返回视频信息
    return info

#==================重命名=====================
def rename(path, VID, info):
    newVID = os.path.splitext(VID)[0] + '.mp4'
    if os.path.exists(path+'/'+info+newVID):
        os.remove(path+'/'+info+newVID)
        print("已覆盖", info+newVID)
    os.rename(path+'/'+VID, path+'/'+info+newVID)

#==================复制文件===================
def move_file(path, dst_path, file):

    shutil.copyfile(path+'/'+file, dst_path+'/'+file)

#===================线程1======================
def thread1():
    vid_num1 = 0
    for VID in vid_dirs[0:half]:
            print(os.path.join(path, VID))
            info = getinfo(path, VID)
            move_file(path, dst_path + '/视频', VID)
            rename(dst_path + '/视频', VID, info)
            vid_num1 += 1
    return vid_num1

#===================线程2======================
def thread2():
    vid_num2 = 0
    for VID in vid_dirs[half:]:
            print(os.path.join(path, VID))
            info = getinfo(path, VID)
            move_file(path, dst_path + '/视频', VID)
            rename(dst_path + '/视频', VID, info)
            vid_num2 += 1
    return vid_num2

#==================创建线程类===================
class MyThread(threading.Thread):

    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.vid_num = self.func()

    def get_num(self):
        return self.vid_num

if __name__ == '__main__':
    #目录路径
    #path = sys.argv[1]
    #dst_path = sys.argv[2]
    print('输入目录路径：')
    path = input()
    print('输入目的路径：')
    dst_path = input().strip('"')
    #路径下所有文件,照片视频分开
    dirs = os.listdir(path)
    pic_dirs = []
    vid_dirs = []
    for file in dirs:
        if file.__contains__(".mp4") or file.__contains__(".MP4") or file.__contains__('.insv'):
            vid_dirs.append(file)
        elif file.__contains__(".jpg") or file.__contains__(".JPG"):
            pic_dirs.append(file)
    print(pic_dirs)
    print(vid_dirs)
    half = len(vid_dirs) // 2
    print(half)
    pic_num = 0
    vid_num = 0

    #若目的路径与原目录相同则只重命名
    if path == dst_path:
        for VID in vid_dirs:
                print(os.path.join(path, VID))
                info = getinfo(path, VID)
                rename(dst_path, VID, info)
                vid_num += 1
    else:
        #创建文件夹，分别对照片和视频复制和命名
        if not os.path.exists(dst_path + '/视频'):
            os.mkdir(dst_path + '/视频')
        if not os.path.exists(dst_path + '/照片'):
            os.mkdir(dst_path + '/照片')
        #复制照片
        for PIC in pic_dirs:
                print(os.path.join(path, PIC))
                move_file(path, dst_path+'/照片', PIC)
                pic_num += 1
        #使用多线程复制视频
        threads = []
        t1 = MyThread(thread1)
        threads.append(t1)
        t2 = MyThread(thread2)
        threads.append(t2)
        for t in threads:
            t.setDaemon(False)
            t.start()
        for t in threads:
            t.join()
        vid_num1 = t1.get_num()
        vid_num2 = t2.get_num()
        vid_num = vid_num1 + vid_num2

    print('成功处理{}张照片,{}个视频。'.format(pic_num, vid_num))
