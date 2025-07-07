"""
PDF转Word转换器命令行版本
支持批量转换和单文件转换
"""
import argparse
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from app.converter import DocumentConverter

def main():
    parser = argparse.ArgumentParser(description='PDF与Word文档转换工具')
    parser.add_argument('input_file', help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（可选）')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误：文件 '{args.input_file}' 不存在")
        sys.exit(1)
    
    try:
        # 创建转换器
        converter = DocumentConverter(args.input_file, args.output)
        
        if args.verbose:
            print(f"输入文件: {args.input_file}")
            print(f"输出文件: {args.output or '自动生成'}")
        
        # 执行转换
        output_file = converter.convert()
        
        print(f"转换成功！输出文件: {output_file}")
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
