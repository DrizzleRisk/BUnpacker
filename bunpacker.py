#coding=utf-8
import sys,shutil
reload(sys)
sys.setdefaultencoding('utf-8')
import os,time,zipfile
from xml.dom import minidom

PACKAGE_NAME = ''
START_ACTIVITY = ''
APK_PATH = ''
def Title():
    print '[>>>]       BUnpacker         [<<<]'
    print '[>>>]    code by Drizzle      [<<<]'
    print '[>>>]        2016.10          [<<<]'
def CheckEnv():
    Title()
    print '[*] Init env'
    global APK_PATH
    global PACKAGE_NAME
    global START_ACTIVITY
    #初始化环境
    if not os.path.exists('result'):
        os.mkdir('result')
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    CPU = 'x86'
    os.popen('adb root')
    result = os.popen('adb shell cat /proc/cpuinfo').read()
    if result.find('ARM') != -1:
        CPU = 'armeabi'
    print '[*] Target: '+CPU
    print '[---------------------------------------]'
    os.popen('adb push ext-tools/' + CPU + '/bulib /data/local/tmp')
    os.popen('adb install ' + APK_PATH)
    print '[---------------------------------------]'
    #获取包信息备用
    print '[*] Get package info'
    nxml = open('tmp/nxml.xml','w')
    zf = zipfile.ZipFile(APK_PATH, 'r')
    content = zf.read('AndroidManifest.xml')
    nxml.write(content)
    nxml.close()
    content = os.popen('java -jar ext-tools/AXMLPrinter2.jar tmp/nxml.xml').read()
    mfest = minidom.parseString(content)
    manifest = mfest.getElementsByTagName('manifest')
    activities = mfest.getElementsByTagName("activity")
    for node in manifest:
        PACKAGE_NAME = node.getAttribute("package")
    for activity in activities:
            for sitem in activity.getElementsByTagName("action"):
                val = sitem.getAttribute("android:name")
                if val == "android.intent.action.MAIN" :
                    START_ACTIVITY = activity.getAttribute("android:name")

def Dump():
    print '[*] Dump dex'
    global PACKAGE_NAME
    global START_ACTIVITY
    os.popen('adb shell am force-stop ' + PACKAGE_NAME)
    time.sleep(1)
    os.popen('adb shell am start -n ' + PACKAGE_NAME + '/' + START_ACTIVITY)
    content = os.popen('adb shell ./data/local/tmp/bulib ' + PACKAGE_NAME).read()
    print '[---------------------------------------]'
    os.popen('adb pull ' + content + ' result/' + PACKAGE_NAME + '.dex')
    print '[---------------------------------------]'
    if os.path.exists('result/' + PACKAGE_NAME + '.dex'):
        print '[*] Success >> ' + 'result/' + PACKAGE_NAME + '.dex'
    #清理环境
    if os.path.exists('tmp'):
        shutil.rmtree('tmp')

def Useage():
    Title()
    print '[*] Useage: tunpacker.py jiagu.apk'
    print '[*] 1.Before Running ,make sure a rooted Android system has been connected to your PC'
    print '[*] 2.Only for testing,Do not be evil !'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Useage()
    else:
        APK_PATH = sys.argv[1]
        CheckEnv()
        Dump()
