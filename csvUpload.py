import os,datetime
from multiprocessing import Pool
from ftplib import FTP



server = {'host': '10.231.143.105', 'port': 21,
          'user' : 'smnra', 'password' : 'smnra000',
          'city' : 'BAOJI',
          'sdate' : (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d'),
          'localPath' : 'C:\\umr\\csv',
          'ftpPath' : '/' + (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d') + '/' + 'BAOJI',
          'upLoadArg': [{'conn' : '', 'localFilePath' : ''},]

          }


def initFtpDir():
    # 初始化 FTP 服务器的 文件夹
    tmpArg = {'conn': '', 'cityFtpPath': ''}
    # 初始化连接信息
    # 参数为  城市名,本地文件夹, ftp主机ip ,用户名 , 密码
    tmpArg['conn'] = FTP()
    tmpArg['conn'].connect(host=server['host'], port=server['port'])
    tmpArg['conn'].login(server['user'], server['password'])

    # 初始化文件夹信息
    tmpArg['conn'].cwd('/')
    try:
        tmpArg['conn'].mkd(server['sdate'])
    except Exception as error:
        print('{} 目录已存在文件夹 {}.'.format(tmpArg['conn'].pwd(), server['sdate']))
        print(error)

    try:
        tmpArg['conn'].cwd(server['sdate'])
        tmpArg['conn'].mkd(server['city'])
    except Exception as error:
        print('{} 目录已存在文件夹 {}.'.format(tmpArg['conn'].pwd(), server['city']))
        print(error)



def mftp():
    tmpArg = {'conn': '',  'cityFtpPath': ''}

    def callback4(s):
        print("帮助信息：让僵尸走进房间: " + s)

    def createConn():
        # 初始化连接信息
        # 参数为  城市名,本地文件夹, ftp主机ip ,用户名 , 密码
        tmpArg['conn'] = FTP()
        tmpArg['conn'].connect(host=server['host'], port=server['port'])
        tmpArg['conn'].login(server['user'], server['password'])

        # 初始化本地路径 和 ftp服务器路径
        tmpArg['cityFtpPath'] = '/' + server['sdate'] + '/' + server['city']
        tmpArg['conn'].cwd(tmpArg['cityFtpPath'])

        # 将连接 和 路径信息 添加到 全局变量 列表中
        server['upLoadArg'].append(tmpArg)

        return tmpArg

    return createConn()


def callback(s):
    print(u'FTP 回传信息{}'.format(str(s)))



def uploadFile(fileName):
    # 参数为 本地文件路径, ftp文件路径
    print('新的文件传输进程启动:{}.'.format(fileName))

    localFilePath = os.path.join(server['localPath'], fileName)
    ftpFilePath = server['ftpPath'] + '/' + fileName
    ftpArg = mftp()
    with open(localFilePath, 'rb') as  f_up:
        ftpArg['conn'].storbinary('STOR ' + ftpFilePath, f_up, 4096,)

    ftpArg['conn'].close()
    return '文件上传成功: {}.'.format(localFilePath)


def upLoadDir(localPath):
    # 最大的进程数为3
    po = Pool(5)

    # 初始化FTP服务器 文件夹
    initFtpDir()

    #  获取本地文件列表
    csvFileList = os.listdir(localPath)

    # 遍历 所有文件
    for fileName in csvFileList:
        po.apply_async(uploadFile, args=(fileName,), callback=callback)
        # 添加上传任务到进程池

    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接受新的请求
    po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
    print("-----end-----")







if __name__ == '__main__':
    upLoadDir(server['localPath'])



