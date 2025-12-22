import re
from typing import List, Dict, Any
import html
import unicodedata

def clean_text(text: str) -> str:
    """
    Clean text by removing unwanted characters, normalizing, and preparing for embedding
    
    Args:
        text: Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove HTML entities
    text = html.unescape(text)
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove extra whitespaces while preserving sentence structure
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation relevant for meaning
    # This preserves alphanumeric characters, basic punctuation, and common symbols
    text = re.sub(r'[^\w\s\-\.\,\!\?\;\:\(\)\[\]\{\}\'\"\/\n\r\t]', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def sanitize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize metadata dictionary to ensure it's safe for storage
    
    Args:
        metadata: Input metadata dictionary
        
    Returns:
        Dict: Sanitized metadata dictionary
    """
    if not metadata:
        return {}
    
    sanitized = {}
    for key, value in metadata.items():
        # Clean the key
        clean_key = str(key)[:100]  # Limit key length
        clean_key = re.sub(r'[^\w\-_\.]', '_', clean_key)
        
        # Clean the value based on type
        if isinstance(value, str):
            sanitized[clean_key] = clean_text(value)
        elif isinstance(value, (int, float)):
            sanitized[clean_key] = value
        elif isinstance(value, bool):
            sanitized[clean_key] = value
        elif isinstance(value, list):
            # Recursively clean list items if they're strings
            cleaned_list = []
            for item in value:
                if isinstance(item, str):
                    cleaned_list.append(clean_text(item))
                else:
                    cleaned_list.append(item)
            sanitized[clean_key] = cleaned_list
        else:
            # Convert other types to string and clean them
            sanitized[clean_key] = str(value)
    
    return sanitized

def truncate_content(content: str, max_length: int = 10000) -> str:
    """
    Truncate content to a maximum length while preserving sentence boundaries
    
    Args:
        content: Input content to truncate
        max_length: Maximum length allowed (default 10000 chars)
        
    Returns:
        str: Truncated content
    """
    if not content:
        return ""
    
    if len(content) <= max_length:
        return content
    
    # Find sentence boundary before max_length
    truncated = content[:max_length]
    
    # Look for the last sentence ending before max_length
    last_sentence_end = max(
        truncated.rfind('.'),
        truncated.rfind('!'),
        truncated.rfind('?'),
        truncated.rfind('\n'),
        truncated.rfind(' ')
    )
    
    # If we found a reasonable place to break, truncate there
    if last_sentence_end > max_length * 0.8:  # At least 80% of max_length
        return truncated[:last_sentence_end+1]
    
    # Otherwise, just truncate at max_length
    return truncated

def extract_sections(text: str, section_headers: List[str] = None) -> List[Dict[str, str]]:
    """
    Extract sections from text based on headers
    
    Args:
        text: Input text
        section_headers: List of possible section headers
        
    Returns:
        List of dictionaries containing section title and content
    """
    if not text:
        return []
    
    if section_headers is None:
        section_headers = [
            r'^#+\s+(.*)$',  # Markdown headers
            r'^\*\*(.+?)\*\*$',  # Bold text as headers
            r'^##(.*)$',  # H2 headers
            r'^###(.*)$',  # H3 headers
        ]
    
    sections = []
    
    # Split text by potential section breaks
    lines = text.split('\n')
    
    current_section_title = "Introduction"
    current_section_content = []
    
    for line in lines:
        is_header = False
        header_match = re.match(r'^#+\s+(.*)$', line.strip())
        
        if header_match:
            # Save previous section
            if current_section_content:
                sections.append({
                    "title": current_section_title,
                    "content": "\n".join(current_section_content).strip()
                })
            
            # Start new section
            current_section_title = header_match.group(1).strip()
            current_section_content = []
            is_header = True
        
        if not is_header:
            current_section_content.append(line)
    
    # Add the last section
    if current_section_content:
        sections.append({
            "title": current_section_title,
            "content": "\n".join(current_section_content).strip()
        })
    
    return sections

def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text while preserving paragraph structure
    
    Args:
        text: Input text
        
    Returns:
        str: Text with normalized whitespace
    """
    if not text:
        return ""
    
    # Split by double newlines to preserve paragraphs
    paragraphs = text.split('\n\n')
    
    normalized_paragraphs = []
    for paragraph in paragraphs:
        # Normalize single spaces within a paragraph
        sentences = paragraph.split('\n')
        normalized_sentences = []
        for sentence in sentences:
            # Replace multiple spaces with single space
            normalized_sentence = re.sub(r'\s+', ' ', sentence)
            normalized_sentences.append(normalized_sentence.strip())
        
        normalized_paragraph = '\n'.join(normalized_sentences)
        if normalized_paragraph.strip():
            normalized_paragraphs.append(normalized_paragraph)
    
    return '\n\n'.join(normalized_paragraphs)

def clean_document(text: str, max_length: int = 10000) -> str:
    """
    Complete cleaning pipeline for a document
    
    Args:
        text: Input document text
        max_length: Maximum length for the output (default 10000 chars)
        
    Returns:
        str: Cleaned and processed document text
    """
    # Apply cleaning steps in sequence
    text = clean_text(text)
    text = normalize_whitespace(text)
    text = truncate_content(text, max_length)
    
    return text