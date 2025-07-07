import re

def extract_section(text, section_name):
    pattern = rf"{section_name}.*?(?=\n[A-Z][a-z]|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(0).strip() if match else ""
