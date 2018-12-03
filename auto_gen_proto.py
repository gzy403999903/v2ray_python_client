import os
import shutil
import grpc_tools.protoc as proto
import pathlib
import sys


def fixDir():
    if not pathlib.Path("v2ray.com/core").exists():
        try:
            os.mkdir("v2ray.com")
        except FileExistsError as e:
            print(e)
        except PermissionError as e:
            print(e)
    for (path, _, fileName) in os.walk('.'):
        for i in fileName:
            if i.endswith(".proto"):
                return path


def genProto():
    for (path, _, fileName) in os.walk("./"):
        for i in fileName:
            if i.endswith(".proto"):
                p = path + "/" + i
                proto.main(
                    "--proto_path=./ --python_out=./ --grpc_python_out=./ {}".format(
                        p).split())


path = fixDir()
if not pathlib.Path("core").exists():
    try:
        os.renames(path, "core")
    except PermissionError as e:
        print(e)
        sys.exit()
try:
    shutil.move('core', 'v2ray.com/core')
except PermissionError as e:
    print(e)
    sys.exit()

genProto()
