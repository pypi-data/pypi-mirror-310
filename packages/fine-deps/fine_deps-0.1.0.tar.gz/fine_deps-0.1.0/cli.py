import click
from pathlib import Path
from .analyzer import DependencyAnalyzer

@click.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--pyproject', '-p', type=click.Path(exists=True),
              help='指定 pyproject.toml 文件的路径（可选）')
@click.option('--long', '-l', is_flag=True, help='显示完整的使用位置信息')
@click.option('--output', '-o', type=click.Path(), help='输出结果到文件')
@click.option('--format', '-f', type=click.Choice(['json', 'toml']), 
              default='json', help='输出文件格式 (json 或 toml)')
@click.option('--quiet', '-q', is_flag=True, help='不在控制台显示结果')
def main(project_path: str, pyproject: str = None, long: bool = False, 
         output: str = None, format: str = 'json', quiet: bool = False):
    """
    分析Python项目的依赖情况
    
    PROJECT_PATH: 要分析的项目路径
    """
    click.echo(f"正在分析项目: {project_path}")
    
    analyzer = DependencyAnalyzer(project_path, pyproject)
    analyzer.analyze_project()
    
    if not quiet:
        analyzer.display_results(show_full_path=long)
    
    if output:
        analyzer.export_results(output, format)
        click.echo(f"分析结果已保存到: {output}")

if __name__ == '__main__':
    main() 