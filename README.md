# v2ray_python_client
这个是v2ray python调用api的实例，可以根据这个实例调用所有的api，service_client.py是新增文件，里面有没有写完的方法，最近添加了查看v2ray的统计信息的接口。
## 说明
- 最开始写这个的驱动是我要调用官方api，最后发现网上是没有python调用相关的信息，只找到了一个可能是官方开发写的一个教程，是go语言的，直接调用了源代码里面的各种库，但是那个是go啊，咱们又不会，而且**直接依赖源代码**，这个很麻烦，于是就想着用python重新写
- go的调用例子url：[api go 调用实例](https://medium.com/@TachyonDevel/%E8%B0%83%E7%94%A8-v2ray-%E6%8F%90%E4%BE%9B%E7%9A%84-api-%E6%8E%A5%E5%8F%A3%E8%BF%9B%E8%A1%8C%E7%94%A8%E6%88%B7%E5%A2%9E%E5%88%A0%E6%93%8D%E4%BD%9C-adf9ff972973)
- 本项目主要含有两个主要文件，client.py和get_proto.py，get_proto.py是前置处理文件，client.py是api调用文件
- 其他非go语言调用均可参照此项目
## 使用
啦啦啦啦，最新的使用方法来了，全自动下载到编译，无需任何操作，本次更新引入了auto_proto_process.py文件，里面是自动检查当前编译版本是不是最新，如果不是最新会自动下载最新的代码，然后调用get_proto.py进行proto文件编译。直接运行，就可以获取最新代码的编译结果啦：

```commandline
    python auto_proto_process.py
```

编译结束后，就可以运行各种client了。


## client.py 说明
这个就比较简单了，直接按照go api调用过程翻译就行了，当新增方法是，主要查看.proto文件的类描述，里面很多时候使用了v2ray.com.core.common.serial.typed_message的这个类

三个service的.proto文件在以下路径：
1. v2ray/com/core/app/proxyman/command/command.proto
2. v2ray/com/core/app/stats/command/command.proto
3. v2ray/com/core/app/log/command/config.proto

## service_client.py
client.py 的扩展文件，这个的目标是实现所有的api接口，但是精力有限，有空就会完成一些。

目前完成的接口:
1. add_user
2. remove_user
3. get_stats

## 项目依赖
因为v2ray的api使用了gRPC，gRPC又需要protobuf，所有我们的项目也依赖这俩，除此之外我们还依赖了gRPC的编译工具，关于python gRPC更多的信息参见[gRPC](https://grpc.io/docs/quickstart/python.html)，源代码里面，作者是把proto文件编译成为了go文件，因为我们要使用python，所有需要把proto文件编译成为.py文件

安装gRPC和gRPC-tool

```commandline
    python -m pip install grpcio
    python -m pip install grpcio-tools
```

## 其他文件

### get_proto.py
> 更新了以后基本不需要使用这个文件，被auto_proto_process.py代替，auto_proto_process.py会帮助我们调用这个文件


这个文件主要是把v2ray里面的proto文件编译成为.py的文件，做法是先寻找源代码里面所有的.proto文件，然后调用gRPC的命令去编译文件，编译过程中涉及到一堆的修改文件夹操作，所以我们需要去下载[v2ray](https://github.com/v2ray/v2ray-core)的项目源码

使用方式如下：

```commandline
    python get_proto.py -d 源代码目录地址
```

例如：

```commandline
    python get_proto.py -d c:\\v2ray-master
```

里面主要是文件夹的复制、删除、移动等操作，核心的是运行了一条命令
```commandline
    python -m grpc.tools.protoc -I=. --python_out=grpc_dir --grpc_python_out=grpc_dir *.proto *.proto (各种proto同文件)
```



