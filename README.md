# ROS2 System Status Monitor

## 项目简介

这是一个基于 ROS2 Humble 的系统状态监控项目，用于实时获取并显示 Linux 系统的运行状态信息。

主要监控以下信息：

* 记录时间
* 主机名
* CPU 使用率
* 内存使用率
* 内存总大小
* 剩余内存
* 网络发送数据量
* 网络接收数据量

项目使用 ROS2 自定义消息进行系统状态数据传输，并使用 Qt 实现简单的图形化显示界面。

## 环境

* Ubuntu 22.04
* ROS2 Humble
* Python 3
* PyQt5
* psutil

## 项目结构

```text
src/
├── status_interfaces/
│   ├── CMakeLists.txt
│   ├── package.xml
│   └── msg/
│       └── SystemStatus.msg
│
└── status_publisher/
    ├── package.xml
    ├── setup.py
    ├── setup.cfg
    ├── resource/
    │   └── status_publisher
    ├── status_publisher/
    │   ├── __init__.py
    │   └── sys_status_pub.py
    └── test/
        ├── test_copyright.py
        ├── test_flake8.py
        └── test_pep257.py
```

## 功能

`status_interfaces` 用于定义 ROS2 自定义消息 `SystemStatus`。

`status_publisher` 负责获取 Linux 系统状态信息，并通过 ROS2 发布，同时使用 Qt 窗口显示实时数据。

## 运行

进入 ROS2 工作空间后编译：

```bash
colcon build
```

加载环境：

```bash
source install/setup.bash
```

运行：

```bash
ros2 run status_publisher sys_status_pub
```
