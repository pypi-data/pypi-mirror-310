# magic-dash

命令行工具，用于快捷生成一系列标准[Dash](https://github.com/plotly/dash)应用工程模板。

<div>

[![GitHub](https://shields.io/badge/license-MIT-informational)](https://github.com/CNFeffery/feffery-antd-components/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/magic-dash.svg?color=dark-green)](https://pypi.org/project/feffery-dash-utils/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

## 目录

[安装](#install)<br>
[使用](#usage)<br>

<a name="install" ></a>

## 安装

```bash
pip install magic-dash -U
```

<a name="usage" ></a>

## 使用

### 查看内置项目模板

```bash
magic-dash list
```

### 生成指定项目模板

- 默认生成到当前路径

```bash
magic-dash create --name magic-dash
```

- 指定生成路径

```bash
magic-dash create --name magic-dash --path 目标路径
```

### 查看命令说明

```bash
magic-dash --help

magic-dash list --help

magic-dash create --help
```
