'''
Copyright: Copyright(c)2019
Createdon: 2019-10-26
Author: Penk
Version: 2.0
Title: 自动复制和重命名程序
'''

import ffmpeg
import sys
import os
import shutil

#====================获取视频信息================
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
    os.rename(path+'/'+VID, path+'/'+info+VID)

#==================复制文件===================
def move_file(path, dst_path, file):
    shutil.copyfile(path+'/'+file, dst_path+'/'+file)


if __name__ == '__main__':
    #目录路径
    #path = sys.argv[1]
    #dst_path = sys.argv[2]
    print('输入目录路径：')
    path = input()
    print('输入目的路径：')
    dst_path = input().strip('"')
    if not os.path.exists(dst_path+'/视频'):
        os.mkdir(dst_path+'/视频')
    if not os.path.exists(dst_path+'/照片'):
        os.mkdir(dst_path+'/照片')

    #路径下所有文件
    dirs = os.listdir(path)
    #print(dirs)
    pic_num = 0
    vid_num = 0
    for file in dirs:
        if file.__contains__(".jpg") or file.__contains__(".JPG"):
            PIC = file
            print(os.path.join(path, PIC))
            move_file(path, dst_path+'/照片', PIC)
            pic_num += 1
        elif file.__contains__(".mp4") or file.__contains__(".MP4"):
            VID = file
            print(os.path.join(path, VID))
            info = getinfo(path, VID)
            move_file(path, dst_path+'/视频', VID)
            rename(dst_path+'/视频', VID, info)
            vid_num += 1
    print('成功处理{}张照片,{}个视频。\n按任意键结束。'.format(pic_num, vid_num))


