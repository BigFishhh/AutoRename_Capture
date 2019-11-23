'''
对视频每分钟截图
'''
import os

VideoScreenshotPath = r"C:\Users\insta360\Desktop\VideoScreenshot.bat"
print('路径：')
Dir = input()
print('最大多少分钟：')
times = input()
for i in range(int(times) + 1):
    time = i * 60 + 3
    os.system(VideoScreenshotPath + ' ' + '"{}"'.format(Dir) + ' {} 0 0'.format(time))
