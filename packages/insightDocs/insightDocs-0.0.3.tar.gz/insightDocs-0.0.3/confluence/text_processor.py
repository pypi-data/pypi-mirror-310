import os
from pathlib import Path

from confluence.context_node import ContentNode
from confluence.html_cleaner import MarkdownContentProcessor

def save_processed_content(node: ContentNode, base_dir: str = "data/text_files") -> str:
    """
    Save the processed content to a file in the specified directory.
    
    Args:
        node: The processed ContentNode
        base_dir: Base directory for saving files (default: "data/text_files")
        
    Returns:
        str: Path to the saved file
    """
    # Create directory if it doesn't exist
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    # Create a safe filename from the title
    safe_filename = "".join(c for c in node.title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_filename = safe_filename.replace(' ', '_') + '.md'
    
    # Create full file path
    file_path = os.path.join(base_dir, safe_filename)
    
    # Get the formatted content
    processor = MarkdownContentProcessor()
    formatted_content = processor.format_for_embedding(node)
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    
    return file_path