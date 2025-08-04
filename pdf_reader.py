#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文本提取工具
使用PyPDF2库来读取PDF文件中的文字内容
"""

import sys
import os
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("错误：未安装PyPDF2库")
    print("请运行以下命令安装：")
    print("pip install PyPDF2")
    sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """
    从PDF文件中提取文本
    
    Args:
        pdf_path (str): PDF文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"文件不存在：{pdf_path}")
        
        # 检查文件扩展名
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"文件不是PDF格式：{pdf_path}")
        
        text_content = []
        
        # 打开PDF文件
        with open(pdf_path, 'rb') as file:
            # 创建PDF读取器对象
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 获取页数
            num_pages = len(pdf_reader.pages)
            print(f"PDF文件共有 {num_pages} 页")
            
            # 逐页提取文本
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text.strip():  # 如果页面有文本内容
                    text_content.append(f"\n--- 第 {page_num + 1} 页 ---\n")
                    text_content.append(page_text)
                else:
                    print(f"第 {page_num + 1} 页没有可提取的文本内容")
        
        return '\n'.join(text_content)
        
    except Exception as e:
        print(f"提取PDF文本时出错：{str(e)}")
        return None


def save_text_to_file(text_content, output_path):
    """
    将提取的文本保存到文件
    
    Args:
        text_content (str): 文本内容
        output_path (str): 输出文件路径
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"文本已保存到：{output_path}")
    except Exception as e:
        print(f"保存文件时出错：{str(e)}")


def main():
    """主函数"""
    print("PDF文本提取工具")
    print("=" * 50)
    
    # 获取PDF文件路径
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = input("请输入PDF文件路径：").strip()
    
    # 提取文本
    print(f"正在处理PDF文件：{pdf_path}")
    text_content = extract_text_from_pdf(pdf_path)
    
    if text_content:
        print("\n提取的文本内容：")
        print("=" * 50)
        print(text_content)
        print("=" * 50)
        
        # 询问是否保存到文件
        save_option = input("\n是否将文本保存到文件？(y/n): ").strip().lower()
        if save_option in ['y', 'yes', '是']:
            # 生成输出文件名
            pdf_name = Path(pdf_path).stem
            output_path = f"{pdf_name}_extracted_text.txt"
            save_text_to_file(text_content, output_path)
    else:
        print("无法提取PDF文本内容")


if __name__ == "__main__":
    main() 