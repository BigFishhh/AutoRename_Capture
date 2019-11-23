'''
调用VideoScreenshot脚本截图，效果一样
'''
import os

VideoScreenshotPath = r"C:\Users\insta360\Desktop\VideoScreenshot.bat"
print('路径：')
Dir = input()
print('第几秒：')
time = input()
os.system(VideoScreenshotPath + ' ' + '"{}"'.format(Dir) + ' {} 0 0'.format(time))
