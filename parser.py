import re
from typing import List, Dict, Any

def parse_questions_from_chunk(text: str) -> List[Dict[str, Any]]:
    """
    Helper to extract questions from a text chunk.
    """
    questions = []
    
    # Regex to find the START of a question (e.g., "1.", "Q1.")
    # We look for:
    # - Start of line
    # - Optional "Q" or "Question"
    # - Number
    # - Separator (dot, bracket, dash)
    question_start_pattern = re.compile(r"(?:^|\n)\s*(?:Q|Question)?\s*(\d+)[\.\)\-]", re.IGNORECASE)
    
    matches = list(question_start_pattern.finditer(text))
    
    for i, match in enumerate(matches):
        q_num = match.group(1)
        start_pos = match.end()
        
        if i + 1 < len(matches):
            end_pos = matches[i+1].start()
        else:
            end_pos = len(text)
            
        q_text = text[start_pos:end_pos].strip()
        
        # Clean up text
        q_text = re.sub(r'\n{2,}', '\n', q_text)
        q_text = re.sub(r'\n', ' ', q_text)
        q_text = " ".join(q_text.split())
        
        if len(q_text) > 0:
            questions.append({
                "number": q_num,
                "question": q_text
            })
            
    return questions

def parse_text(text: str) -> Dict[str, Any]:
    """
    Parse extracted text to find Sections and their Questions.
    """
    data = {
        "sections": [],
        "raw_text": text
    }

    # Find all Section headers (e.g. "Section 1", "Part 2")
    # We look for "Section" (or typos like "Seclion", "Sec") or "Part" followed by a NUMBER
    # Regex:
    # (?:^|\n) -> Start of line
    # \s* -> Whitespace
    # (?:Sec\w*|Part) -> "Sec" followed by any word chars (matches Section, Seclion, Sec) OR "Part"
    # \s*[:\-]?\s* -> Optional separator
    # (\d+) -> The number
    section_pattern = re.compile(r"(?:^|\n)\s*(?:Sec\w*|Part)\s*[:\-]?\s*(\d+)", re.IGNORECASE)
    
    matches = list(section_pattern.finditer(text))
    
    # If no sections found, treat whole text as one default section
    if not matches:
        questions = parse_questions_from_chunk(text)
        if questions:
            data["sections"].append({
                "name": "Default",
                "questions": questions
            })
        return data

    # Process sections
    # 1. Text before first section (if any)
    if matches[0].start() > 0:
        pre_text = text[:matches[0].start()]
        questions = parse_questions_from_chunk(pre_text)
        if questions:
             data["sections"].append({
                "name": "Introduction/Header",
                "questions": questions
            })

    # 2. Process each section
    for i, match in enumerate(matches):
        section_name = f"Section {match.group(1)}"
        start_pos = match.end()
        
        if i + 1 < len(matches):
            end_pos = matches[i+1].start()
        else:
            end_pos = len(text)
            
        section_text = text[start_pos:end_pos]
        questions = parse_questions_from_chunk(section_text)
        
        data["sections"].append({
            "name": section_name,
            "questions": questions
        })

    return data
