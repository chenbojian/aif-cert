#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文本转JSON转换器
将PDF提取的文本文件转换为标准JSON格式
"""

import re
import json
import sys
from pathlib import Path


def extract_questions_from_text(text_content):
    """
    从文本内容中提取问题
    
    Args:
        text_content (str): 文本内容
        
    Returns:
        list: 提取的问题列表
    """
    questions = []
    
    # 使用正则表达式匹配问题模式
    # 匹配 "Topic X Question #Y" 格式
    question_pattern = r'Topic \d+ Question #(\d+)'
    
    # 分割文本为行
    lines = text_content.split('\n')
    
    current_question = None
    current_question_text = []
    current_answers = []
    current_correct_answer = None
    in_question = False
    in_answers = False
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行和页面分隔符
        if not line or line.startswith('--- 第') or line.startswith('https://'):
            continue
            
        # 检查是否是新问题的开始
        question_match = re.search(question_pattern, line)
        if question_match:
            # 保存前一个问题（如果存在）
            if current_question is not None:
                questions.append({
                    'id': f"Question {current_question}",
                    'question': ' '.join(current_question_text).strip(),
                    'answers': '\n'.join(current_answers).strip(),
                    'correct_answer': current_correct_answer,
                    'explanation': ''
                })
            
            # 开始新问题
            current_question = question_match.group(1)
            current_question_text = []
            current_answers = []
            current_correct_answer = None
            in_question = True
            in_answers = False
            continue
        
        # 检查是否是正确答案行
        if line.startswith('Correct Answer:'):
            current_correct_answer = line.replace('Correct Answer:', '').strip()
            in_question = False
            in_answers = False
            continue
            
        # 跳过社区投票分布等额外信息
        if line.startswith('Community vote distribution') or line.startswith('Other'):
            continue
            
        # 检查是否是选项（A. B. C. D. E. F. 等）
        option_match = re.match(r'^([A-F])\.\s*(.+)$', line)
        if option_match:
            in_question = False
            in_answers = True
            option_letter = option_match.group(1)
            option_text = option_match.group(2)
            current_answers.append(f"{option_letter}. {option_text}")
            continue
            
        # 如果正在处理选项，继续添加选项内容
        if in_answers and line and not line.startswith('Topic'):
            if current_answers:
                # 将当前行添加到最后一个选项
                current_answers[-1] += ' ' + line
            continue
            
        # 如果正在处理问题文本，添加到问题内容
        if in_question and line and not line.startswith('Topic'):
            current_question_text.append(line)
    
    # 添加最后一个问题
    if current_question is not None:
        questions.append({
            'id': f"Question {current_question}",
            'question': ' '.join(current_question_text).strip(),
            'answers': '\n'.join(current_answers).strip(),
            'correct_answer': current_correct_answer,
            'explanation': ''
        })
    
    return questions


def clean_text(text):
    """
    清理文本内容
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 清理后的文本
    """
    # 移除行首行尾空白
    text = text.strip()
    return text


def clean_answers_text(text):
    """
    清理答案文本，保留选项之间的换行符
    
    Args:
        text (str): 原始答案文本
        
    Returns:
        str: 清理后的答案文本
    """
    # 移除行首行尾空白
    text = text.strip()
    # 清理每个选项内部的空白，但保留选项之间的换行符
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # 清理每行内部的空白字符
        cleaned_line = re.sub(r'\s+', ' ', line.strip())
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)


def convert_pdf_text_to_json(input_file, output_file):
    """
    将PDF文本文件转换为JSON格式
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print(f"正在处理文件: {input_file}")
        
        # 提取问题
        questions = extract_questions_from_text(text_content)
        
        print(f"成功提取 {len(questions)} 个问题")
        
        # 清理问题内容
        for question in questions:
            question['question'] = clean_text(question['question'])
            question['answers'] = clean_answers_text(question['answers'])
        
        # 写入JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        print(f"转换完成！输出文件: {output_file}")
        
        # 显示前几个问题的统计信息
        print(f"\n转换统计:")
        print(f"- 总问题数: {len(questions)}")
        
        # 统计单选题和多选题
        single_choice = sum(1 for q in questions if len(q['correct_answer']) == 1)
        multi_choice = sum(1 for q in questions if len(q['correct_answer']) > 1)
        
        print(f"- 单选题: {single_choice}")
        print(f"- 多选题: {multi_choice}")
        
        # 显示前3个问题作为示例
        print(f"\n前3个问题示例:")
        for i, question in enumerate(questions[:3]):
            print(f"\n{question['id']}:")
            print(f"问题: {question['question'][:100]}...")
            print(f"选项数: {len(question['answers'].split('\\n'))}")
            print(f"正确答案: {question['correct_answer']}")
        
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        return False
    
    return True


def main():
    """主函数"""
    print("PDF文本转JSON转换器")
    print("=" * 50)
    
    # 获取输入文件路径
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "AWS Certified Solution Architect - Associate SAA-C03 Exam_extracted_text.txt"
    
    # 检查输入文件是否存在
    if not Path(input_file).exists():
        print(f"错误：输入文件不存在: {input_file}")
        sys.exit(1)
    
    # 生成输出文件名
    output_file = "SAA-C03.json"
    
    # 执行转换
    success = convert_pdf_text_to_json(input_file, output_file)
    
    if success:
        print(f"\n转换成功完成！")
        print(f"输出文件: {output_file}")
    else:
        print(f"\n转换失败！")
        sys.exit(1)


if __name__ == "__main__":
    main() 