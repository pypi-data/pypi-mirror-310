# drawer python 实现

这是《编译原理》课程上机实验要求实现的绘图语言（命名为 drawer）的 python 实现

# 运行

## 前置要求

安装以下软件

-   [python3](https://python.org)
-   [poetry](https://python-poetry.org/)

系统要求: 因为 `python` 是跨平台的，理论上没有系统要求。但开发时用的是 `Ubuntu 22.04.3 LTS`.

## 具体步骤

```shell
poetry install
poetry shell # 进入虚拟环境
```

```sh
make parser
```

# 项目组成

## [命令行程序](./src/cli/main.py)

这是命令行接口，用来调用该解释器

## [解释器核心](./src/drawer/__init__.py)

通过解析字符串，导出一系列的指令序列，供外部程序使用

## [语法定义文件](./Drawer.g4)

定义了 drawer 语言的语法
