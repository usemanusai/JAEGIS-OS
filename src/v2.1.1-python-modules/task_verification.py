#!/usr/bin/env python3
"""
Task Verification Script
Extracts and compares task names from original file and current task list
"""

import re
import sys

def extract_original_tasks(file_path):
    """Extract all task names from the original file"""
    tasks = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match NAME: followed by task name until DESCRIPTION:
        pattern = r'NAME:([^D]+?)DESCRIPTION:'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            # Clean up the task name
            task_name = match.strip()
            if task_name:
                tasks.append(task_name)
        
        return tasks
    except Exception as e:
        print(f"Error reading original file: {e}")
        return []

def extract_current_tasks(task_list_content):
    """Extract all task names from current task list"""
    tasks = []
    lines = task_list_content.split('\n')
    
    for line in lines:
        # Look for lines with UUID and NAME:
        if 'UUID:' in line and 'NAME:' in line:
            # Extract the name part
            name_match = re.search(r'NAME:([^D]+?)DESCRIPTION:', line)
            if name_match:
                task_name = name_match.group(1).strip()
                if task_name:
                    tasks.append(task_name)
    
    return tasks

def compare_tasks(original_tasks, current_tasks):
    """Compare original and current task lists"""
    print(f"Original file tasks: {len(original_tasks)}")
    print(f"Current task list tasks: {len(current_tasks)}")
    
    # Convert to sets for comparison
    original_set = set(original_tasks)
    current_set = set(current_tasks)
    
    # Find missing tasks
    missing_tasks = original_set - current_set
    extra_tasks = current_set - original_set
    
    print(f"\nMissing tasks: {len(missing_tasks)}")
    if missing_tasks:
        print("Missing tasks:")
        for task in sorted(missing_tasks):
            print(f"  - {task}")
    
    print(f"\nExtra tasks: {len(extra_tasks)}")
    if extra_tasks:
        print("Extra tasks:")
        for task in sorted(extra_tasks):
            print(f"  + {task}")
    
    return len(missing_tasks) == 0 and len(extra_tasks) == 0

if __name__ == "__main__":
    # This will be run manually with the file paths
    print("Task Verification Script Ready")
