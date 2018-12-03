import uuid
from bs4 import BeautifulSoup
import requests
import configparser
import re
import os
import zipfile
import shutil

CONFIG_INI = 'config.ini'


def is_version_higher(v1, v2):
    p = re.compile('v(\d+\.)*\d+')
    if p.fullmatch(v2) is not None and p.fullmatch(v1) is not None:
        vs1 = list(map(int, v1[1:].split('.')))
        vs2 = list(map(int, v2[1:].split('.')))
        length = max(len(vs1), len(vs2))
        vs1.extend([0] * (length - len(vs1)))
        vs2.extend([0] * (length - len(vs2)))
        for i in range(length):
            if vs1[i] > vs2[i]:
                return True
            elif vs1[i] < vs2[i]:
                return False
    else:
        raise Exception('版本号异常')

    return False


local_tag = 'v0'

cf = configparser.ConfigParser()

if os.path.exists(CONFIG_INI):
    cf.read(CONFIG_INI)
    if cf.has_option('CONFIG', 'latest_version'):
        local_tag = cf.get('CONFIG', 'latest_version')
else:
    cf.add_section('CONFIG')

data = requests.get('https://github.com/v2ray/v2ray-core/releases/latest')
soup = BeautifulSoup(data.text, "html.parser")
latest_version = soup.find('span', {'class': 'css-truncate-target'}).text

if is_version_higher(latest_version, local_tag):
    try:
        if os.path.exists('v2ray-core-master'):
            shutil.rmtree('v2ray-core-master')
        if os.path.exists('source.zip'):
            os.remove('source.zip')

        print('正在下载.....')
        zip_request = requests.get(
            'https://github.com/v2ray/v2ray-core/archive/master.zip')
        source_zip = open('source.zip', mode='wb')
        source_zip.write(zip_request.content)
        azip = zipfile.ZipFile('source.zip')
        print('开始解压.....')
        azip.extractall()
        print('解压完成')
        azip.close()
        c = os.system('python get_proto.py -d v2ray-core-master')
        c.bit_length()
        shutil.rmtree('v2ray-core-master')
        cf.set('CONFIG', 'latest_version', latest_version)
        cf.write(open(CONFIG_INI, mode='w', encoding='utf-8'))
    except Exception as e:
        print('更新文件出错：%s' % str(e))
        exit(0)
else:
    print('文件已经是最新，不需要更新')
