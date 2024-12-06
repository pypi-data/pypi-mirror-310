import ast
import os
import sys
import json
import toml
import pkg_resources
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, Optional, Any

from rich.console import Console
from rich.table import Table

from .utils import is_stdlib_module

class DependencyAnalyzer:
    def __init__(self, project_path: str, pyproject_path: Optional[str] = None):
        """
        初始化依赖分析器
        
        Args:
            project_path: 要分析的项目路径
            pyproject_path: pyproject.toml 文件路径（可选）
        """
        self.project_root = Path(project_path)
        self.pyproject_path = Path(pyproject_path) if pyproject_path else self.project_root / "pyproject.toml"
        self.imports: Dict[str, Set[str]] = defaultdict(set)
        self.stdlib_imports: Dict[str, Set[str]] = defaultdict(set)
        self.third_party_imports: Dict[str, Set[str]] = defaultdict(set)
        self.local_imports: Dict[str, Set[str]] = defaultdict(set)
        self.console = Console()
        
        # 获取已安装的包列表
        self.installed_packages = {pkg.key for pkg in pkg_resources.working_set}

    def analyze_file(self, file_path: Path) -> None:
        """分析单个文件的导入语句"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        self._categorize_import(name.name, str(file_path))
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self._categorize_import(node.module, str(file_path))
        except Exception as e:
            self.console.print(f"[red]Error analyzing {file_path}: {e}[/red]")

    def _categorize_import(self, module_name: str, file_path: str) -> None:
        """对导入进行分类"""
        base_module = module_name.split('.')[0]
        self.imports[base_module].add(file_path)
        
        if is_stdlib_module(base_module):
            self.stdlib_imports[base_module].add(file_path)
        elif base_module in self.installed_packages:
            self.third_party_imports[base_module].add(file_path)
        else:
            self.local_imports[base_module].add(file_path)

    def analyze_project(self) -> None:
        """分析整个项目"""
        for root, _, files in os.walk(self.project_root):
            if any(ignored in root for ignored in ['venv', '.git', '__pycache__', '.pytest_cache']):
                continue
            for file in files:
                if file.endswith('.py'):
                    self.analyze_file(Path(root) / file)

    def display_results(self, show_full_path: bool = False) -> None:
        """
        显示分析结果
        
        Args:
            show_full_path: 是否显示完整的文件路径
        """
        # 标准库表格
        self._display_category_table(
            "标准库依赖", 
            self.stdlib_imports, 
            "blue",
            show_full_path
        )
        
        # 第三方库表格
        self._display_category_table(
            "第三方库依赖", 
            self.third_party_imports, 
            "green",
            show_full_path
        )
        
        # 本地模块表格
        self._display_category_table(
            "本地模块导入", 
            self.local_imports, 
            "yellow",
            show_full_path
        )

    def _display_category_table(self, title: str, imports: Dict[str, Set[str]], 
                              color: str, show_full_path: bool) -> None:
        """显示特定类别的依赖表格"""
        if not imports:
            return
            
        table = Table(title=title)
        table.add_column("模块名", style=color)
        table.add_column("使用位置", style="white")
        
        for module, files in sorted(imports.items()):
            if show_full_path:
                file_list = "\n".join(sorted(files))
            else:
                file_list = "\n".join(sorted(
                    Path(f).relative_to(self.project_root).as_posix() 
                    for f in files
                ))
                if len(file_list) > 100 and not show_full_path:
                    file_list = file_list[:100] + "..."
            table.add_row(module, file_list)
        
        self.console.print(table)
        self.console.print()

    def export_results(self, output_path: str, format: str = 'json') -> None:
        """
        导出分析结果到文件
        
        Args:
            output_path: 输出文件路径
            format: 输出格式 ('json' 或 'toml')
        """
        result_data = {
            "project_path": str(self.project_root),
            "dependencies": {
                "standard_library": {
                    module: sorted(list(files))
                    for module, files in self.stdlib_imports.items()
                },
                "third_party": {
                    module: sorted(list(files))
                    for module, files in self.third_party_imports.items()
                },
                "local_modules": {
                    module: sorted(list(files))
                    for module, files in self.local_imports.items()
                }
            },
            "summary": {
                "total_stdlib_modules": len(self.stdlib_imports),
                "total_third_party_modules": len(self.third_party_imports),
                "total_local_modules": len(self.local_imports)
            }
        }

        # 将文件路径转换为相对路径
        for category in result_data["dependencies"].values():
            for module in category:
                category[module] = [
                    str(Path(f).relative_to(self.project_root))
                    for f in category[module]
                ]

        output_path = Path(output_path)
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
        else:  # toml
            with open(output_path, 'w', encoding='utf-8') as f:
                toml.dump(result_data, f) 