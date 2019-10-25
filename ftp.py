
import os,datetime
import sys
from pprint import pprint
from ftplib import FTP





conn = FTP('10.100.162.117')
conn.login("richuser", "mr@20invenT")

# 昨天的日期 '20191021'
sdate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d')
ftpPath = '/home/richuser/l3fw_mr/kpi_import/' + sdate + r'/'
localPath = os.path.abspath('E:\\工具\\资料\\宝鸡\\研究\\Python\\python3\\WCDMA_MR\\mr_data\\')

conn.cwd(ftpPath)
localPath = os.path.abspath(localPath)
os.chdir(localPath)


def getSite(conn):
    conn.pwd()
    try:
        conn.cwd(ftpPath)
        _, siteDirs = get_dirs_files(conn)
        return list(siteDirs)

    except Exception as error:
        print(str(error))
        return 0



def get_dirs_files(conn):
    dir_res = []
    conn.dir('.', dir_res.append)
    files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
    dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
    return files, dirs

def walk1(next_dir):
    print(next_dir)


def walk(next_dir):
    print(next_dir)
    ftp_dir = conn.pwd()
    local_dir = os.getcwd()

    try:
        os.mkdir(next_dir)
    except OSError:
        pass
    except Exception as error:
        print(str(error))

    os.chdir(next_dir)
    local_curr_dir = os.getcwd()
    conn.cwd(next_dir)
    ftp_curr_dir = conn.pwd()

    files, dirs = get_dirs_files(conn)

    print('Curr FTP Path:  {}\nCurr Local Path:  {}\n'.format(ftp_curr_dir, local_curr_dir))



    # 文件夹 列表 和 文件列表
    sys.stdout.write("FILES: %s" % files)
    sys.stdout.write("DIRS: %s" % dirs)
    print('\n')

    #  遍历文件夹内的文件 并复制到本地目录
    for f in files:
        sys.stdout.write("%s : %s" % (next_dir, f))
        sys.stdout.write("download : %s" % os.path.abspath(f))
        outf = open(f, "wb")
        try:
            conn.retrbinary("RETR %s" % f, outf.write)
        finally:
            outf.close()

        #  遍历子目录, 并子目录内的文件复制到本地目录
        for d in dirs:
            os.chdir(local_curr_dir)
            conn.cwd(ftp_curr_dir)
            walk(d)

    os.chdir(local_dir)
    conn.cwd(ftp_dir)

def run(conn):
    # 获取基站文件夹
    sites = getSite(conn)
    for site in sites:
        walk(site)



if __name__ == '__main__':
    run(conn)

