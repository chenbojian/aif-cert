#!/usr/bin/env python3
"""
MLS-C01 to SAA-C03 JSON Converter

This script converts MLS-C01 format JSON files to SAA-C03 format.
It reads all JSON files from MLS-C01 directory and merges them into a single SAA-C03 format file.
"""

import json
import os
import glob
from typing import List, Dict, Any
import re

def extract_explanation_from_discussion(discussion: List[Dict]) -> str:
    """
    Extract explanation from discussion by finding the highest upvoted comment
    """
    if not discussion:
        return ""
    
    # Find the comment with highest upvote count
    best_comment = max(discussion, key=lambda x: int(x.get('upvote_count', 0)))
    
    # Extract the content and clean it up
    content = best_comment.get('content', '')
    
    # Remove "Selected Answer: X" prefix if present
    content = re.sub(r'^Selected Answer:\s*[A-Z]+\s*', '', content, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    content = re.sub(r'\s+', ' ', content).strip()
    
    return content

def convert_choices_to_answers(choices: Dict[str, str]) -> str:
    """
    Convert choices dictionary to formatted answers string
    """
    if not choices:
        return ""
    
    # Sort choices by key (A, B, C, D, E, F, etc.)
    sorted_choices = sorted(choices.items(), key=lambda x: x[0])
    
    # Format each choice
    formatted_choices = []
    for key, value in sorted_choices:
        # Clean up the choice text - replace newlines with spaces and strip whitespace
        cleaned_value = value.replace('\n', ' ').strip()
        formatted_choices.append(f"{key}. {cleaned_value}")
    
    return "\n".join(formatted_choices)

def get_correct_answer(question_data: Dict[str, Any]) -> str:
    """
    Get the correct answer, prioritizing answer_ET over answer
    """
    # Priority: answer_ET > answer
    correct_answer = question_data.get('answer_ET', '')
    if not correct_answer:
        correct_answer = question_data.get('answer', '')
    
    return correct_answer

def convert_mls_c01_question_to_saa_c03(question_data: Dict[str, Any], question_number: int) -> Dict[str, Any]:
    """
    Convert a single MLS-C01 question to SAA-C03 format
    """
    # Extract basic fields
    question_text = question_data.get('question_text', '')
    choices = question_data.get('choices', {})
    correct_answer = get_correct_answer(question_data)
    discussion = question_data.get('discussion', [])
    url = question_data.get('url', '')
    
    # Add URL to question text if available
    if url:
        question_text_with_url = f"{question_text}\n\nSource: {url}"
    else:
        question_text_with_url = question_text
    
    # Convert to SAA-C03 format
    converted_question = {
        "id": f"Question {question_number}",
        "question": question_text_with_url,
        "answers": convert_choices_to_answers(choices),
        "correct_answer": correct_answer,
        "explanation": extract_explanation_from_discussion(discussion)
    }
    
    return converted_question

def load_mls_c01_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Load and parse a MLS-C01 JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract questions from the nested structure
        questions = data.get('pageProps', {}).get('questions', [])
        return questions
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return []

def convert_all_mls_c01_files(input_dir: str, output_file: str):
    """
    Convert all MLS-C01 JSON files to SAA-C03 format
    """
    # Get all JSON files in the input directory
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    json_files.sort()  # Sort to ensure consistent ordering
    
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files to convert")
    
    all_questions = []
    question_number = 1
    
    for file_path in json_files:
        print(f"Processing {os.path.basename(file_path)}...")
        
        # Load questions from this file
        questions = load_mls_c01_file(file_path)
        
        # Convert each question
        for question_data in questions:
            try:
                converted_question = convert_mls_c01_question_to_saa_c03(question_data, question_number)
                all_questions.append(converted_question)
                question_number += 1
            except Exception as e:
                print(f"Error converting question in {file_path}: {e}")
                continue
    
    # Write the converted data to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully converted {len(all_questions)} questions to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

def main():
    """
    Main function
    """
    input_directory = "MLS-C01"
    output_file = "MLS-C01.json"
    
    # Check if input directory exists
    if not os.path.exists(input_directory):
        print(f"Input directory '{input_directory}' does not exist")
        return
    
    print(f"Converting MLS-C01 files from '{input_directory}' to '{output_file}'")
    
    # Perform the conversion
    convert_all_mls_c01_files(input_directory, output_file)
    
    print("Conversion completed!")

if __name__ == "__main__":
    main()
