# Fine Analyze Dependencies

一个强大的 Python 项目依赖分析工具，可以帮助你分析项目中使用的所有依赖，包括标准库、第三方库和本地模块。

## 特性

- 🔍 自动识别并分类项目中的所有导入
- 🎨 美观的控制台输出（使用 rich 库）
- 📊 支持导出分析结果（JSON/TOML 格式）
- 🔗 显示每个依赖的具体使用位置
- 📝 支持完整路径和相对路径显示
- 🎯 准确区分标准库、第三方库和本地模块

## 安装

使用 pip 安装：


## 使用方法

### 基本使用

分析项目依赖：
    fine-analyze /path/to/your/project


这将显示项目中使用的所有依赖，分为三类：
- 标准库依赖
- 第三方库依赖
- 本地模块导入

### 命令行选项

Options:
-p, --pyproject PATH 指定 pyproject.toml 文件的路径（可选）
-l, --long 显示完整的使用位置信息
-o, --output PATH 输出结果到文件
-f, --format [json|toml] 输出文件格式 (默认: json)
-q, --quiet 不在控制台显示结果
--help 显示帮助信息

fine-analyze /path/to/project --long

2. 导出分析结果为 JSON 文件：

fine-analyze /path/to/project -o dependencies.json

3. 导出为 TOML 格式：
4. 
fine-analyze /path/to/project -o dependencies.toml -f toml

4. 安静模式（只导出文件）：
fine-analyze /path/to/project -q -o dependencies.json

5. 指定 pyproject.toml 文件：
fine-analyze /path/to/project -p /path/to/pyproject.toml


## 输出示例

### 控制台输出

### JSON 输出示例



## 开发说明

### 项目结构


fine_analyze_dependencies/
├── fine_analyze_dependencies/
│ ├── init.py
│ ├── analyzer.py # 核心分析逻辑
│ ├── cli.py # 命令行接口
│ └── utils.py # 工具函数
├── tests/
│ └── init.py
├── pyproject.toml
└── README.md



## 贡献指南

欢迎提交 Pull Requests！以下是一些贡献指南：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 作者

Your Name - [@yourusername](https://github.com/yourusername)

## 致谢

- [rich](https://github.com/Textualize/rich) - 提供精美的终端输出
- [click](https://click.palletsprojects.com/) - 命令行接口框架