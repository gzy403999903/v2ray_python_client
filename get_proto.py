import os
import shutil
import getopt
import sys

command_str = ''


def walk(dir, name):
    global command_str

    for fs in os.listdir(dir):

        path = os.path.join(dir, fs)

        if os.path.isdir(path):
            walk(path, name + '/' + fs)
        elif '.proto' in fs:
            command_str += (' ' + name + '/' + str(fs))
            print(name + '/' + str(fs))


def file_copy(from_dir, to_dir):
    dir_queue = ['']
    while len(dir_queue) > 0:
        dir = dir_queue.pop()
        for fs in os.listdir(from_dir + '/' + dir):
            path = from_dir + '/' + dir + '/' + fs
            if os.path.isdir(path):
                dir_queue.append(dir + '/' + fs)
            else:
                shutil.copyfile(path, to_dir + '/' + dir + '/' + fs)


if __name__ == '__main__':
    dir = '.'
    try:
        options, args = getopt.getopt(sys.argv[1:], 'd:', ['code_dir='])
    except Exception as e:
        print(e)
        sys.exit(0)
    for o, a in options:
        if o in ('-d', '--code_dir'):
            dir = a

    print('文件夹路径：%s' % dir)
    fss = os.listdir(dir)
    if 'app' in fss and 'transport' in fss and 'common' in fss:
        if os.path.exists('grpc_dir'):
            shutil.rmtree('grpc_dir', ignore_errors=True)
        if os.path.exists('v2ray.com'):
            shutil.rmtree('v2ray.com', ignore_errors=True)
        if os.path.exists('v2ray'):
            shutil.rmtree('v2ray', ignore_errors=True)
        shutil.copytree(dir, 'v2ray.com/core')
        os.mkdir('grpc_dir')
    else:
        print('源代码目录输入错误,该文件夹不是v2ray源码的文件夹')
        print('请运行：get_proto.py -d c:\\\\v2ray_source_code_dir')
        sys.exit(0)

    walk('v2ray.com', 'v2ray.com')

    command_str = 'python -m grpc.tools.protoc -I=. --python_out=grpc_dir --grpc_python_out=grpc_dir ' + command_str

    print('\n -----------执行脚本生成-----------  \n')

    print(command_str)

    print('\n -----------开始执行-----------  \n')

    c = os.system(command_str)
    c.bit_length()
    print('\n -----------执行完成-----------  \n')

    print('\n -----------开始复制文件-----------  \n')
    file_copy('grpc_dir/v2ray.com/core', 'grpc_dir/v2ray/com/core')
    shutil.copytree('grpc_dir/v2ray', 'v2ray')
    print('\n -----------文件复制完成-----------  \n')
