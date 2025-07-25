#!/usr/bin/env python3
import json
import re

def fix_answers_format():
    # 读取JSON文件
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 修复每个问题的answers字段
    for question in data:
        if 'answers' in question and question['answers']:
            answers = question['answers']
            
            # 使用正则表达式来修复格式
            # 保留选项分隔符 (\nB., \nC., \nD., \nE.)，但将其他换行符替换为空格
            fixed_answers = re.sub(r'\n(?!B\.|C\.|D\.|E\.)', ' ', answers)
            
            # 更新answers字段
            question['answers'] = fixed_answers
    
    # 写回文件
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Answers format has been fixed!")

if __name__ == "__main__":
    fix_answers_format() 