'''
用ffmprg-python截图，但有损失。。。
'''
import ffmpeg
import os

#===================截图======================
def VideoScreenshot(dst_path, time):

    dir = os.listdir(dst_path)
    #创建截图文件夹
    if not os.path.exists(dst_path+'/VideoScreenshot'):
        os.mkdir(dst_path+'/VideoScreenshot')
    for vid in dir:
        vsc = dst_path + '/VideoScreenshot/' + vid + '_' + time + '.jpg'
        (
            ffmpeg.input(dst_path+'/'+vid, ss=time)
                  #.output(vsc, vframes=1, format='image2', vcodec='mjpeg')
                  #.run(capture_stdout=True)
                  .output(vsc, vframes='2', f='image2', vcodec='mjpeg')
                  .run(quiet=False, overwrite_output=True)
        )
        print(vsc)

if __name__ == '__main__':
    print('输入路径：')
    dst_path = input().strip('"')
    print('第几秒')
    time = input()
    VideoScreenshot(dst_path, time)