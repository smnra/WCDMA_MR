from ftp import *

from multiprocessing import Process,Queue,Pipe,Pool,current_process
import os, time, random


def worker(msg):
    t_start = time.time()
    print("%s开始执行，进程号为%d" % (msg, os.getpid()))
    time.sleep(random.random() * 2)  # random.random()随机成0-1的浮点数
    t_stop = time.time()
    print(msg, "执行完毕，耗时%0.2f" % (t_stop - t_start))

def callback(x):
    print(' {}'.format(current_process().name,x))





if __name__ == '__main__':
    # 获取基站文件夹
    sites = getSite(conn)





    result = []
    po = Pool(3)  # 最大的进程数为3

    for site in sites:
        '''每次循环将会用空闲出来的子进程去调用目标'''
        # f.walk(site)
        po.apply_async(walk,args=(site,))

    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接受新的请求
    po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
    '''如果没有添加join()，会导致有的代码没有运行就已经结束了'''
    print("-----end-----")