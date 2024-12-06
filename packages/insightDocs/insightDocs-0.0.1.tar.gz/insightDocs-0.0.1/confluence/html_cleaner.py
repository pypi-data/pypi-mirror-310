import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re
import json
from bs4 import BeautifulSoup

from confluence.context_node import ContentNode


class MarkdownContentProcessor:
    """Processes content into a Markdown format optimized for RAG systems."""
    
    def __init__(self):
        self.hierarchy_markers = {
            'h1': '#',
            'h2': '##',
            'h3': '###',
            'h4': '####',
            'h5': '#####',
            'h6': '######'
        }
    
    def process_content(self, confluence_data: Dict[str, Any], image_descriptions: Dict[str, str]) -> ContentNode:
        """Process content while preserving hierarchical relationships in Markdown."""
        
        content_id = confluence_data.get('id', '')
        title = confluence_data.get('title', '')
        parent_id = confluence_data.get('parentId')
        
        body_html = confluence_data.get('body', {}).get('view', {}).get('value', '')
        processed_content = self._convert_to_markdown(body_html)
        
        content_link = None
        if '_links' in confluence_data:
            base = confluence_data['_links'].get('base')
            webui = confluence_data['_links'].get('webui')
            if base and webui:
                content_link = base + webui

        if image_descriptions:
            processed_content += "\n\n## Image Descriptions\n"
            for image_key, desc in image_descriptions.items():
                processed_content += f"- {image_key}: {desc}\n"

        if content_link is None:
            file_path = f"{content_id}_confluence_data.json"
            with open(file_path, 'w') as file:
                json.dump(confluence_data, file, indent=4)
            content_link = f"file://{os.path.abspath(file_path)}"
            print(f"No content link found. Saved data to {file_path}.")

        metadata = {
            'content_link': content_link,
            'sourceTemplateEntityId': confluence_data.get('sourceTemplateEntityId', ''),
            'spaceId': confluence_data.get('spaceId', ''),
            'version': confluence_data.get('version', {}),
            'hierarchical_path': self._generate_hierarchical_path(confluence_data),
            'content_type': self._determine_content_type(confluence_data)
        }
        
        return ContentNode(
            id=content_id,
            title=title,
            content=processed_content,
            parent_id=parent_id,
            children=[],
            metadata=metadata
        )
    
    def _convert_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to Markdown while preserving structure."""
        soup = BeautifulSoup(html_content, 'html.parser')
        markdown_chunks = []
        
        # Process headers
        for level in range(1, 7):
            for header in soup.find_all(f'h{level}'):
                header.replace_with(f"\n{self.hierarchy_markers[f'h{level}']} {header.get_text().strip()}\n")
        
        # Process lists
        for ul in soup.find_all('ul'):
            for i, li in enumerate(ul.find_all('li', recursive=False)):
                indent = len(list(li.parents)) - 1
                li.replace_with(f"{'  ' * indent}- {li.get_text().strip()}\n")
        
        for ol in soup.find_all('ol'):
            for i, li in enumerate(ol.find_all('li', recursive=False)):
                indent = len(list(li.parents)) - 1
                li.replace_with(f"{'  ' * indent}{i+1}. {li.get_text().strip()}\n")
        
        # Process tables
        for table in soup.find_all('table'):
            markdown_table = self._convert_table_to_markdown(table)
            table.replace_with(f"\n{markdown_table}\n")
        
        # Process links
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text().strip()
            link.replace_with(f"[{text}]({href})")
        
        # Process emphasis
        for em in soup.find_all(['em', 'i']):
            em.replace_with(f"*{em.get_text().strip()}*")
        for strong in soup.find_all(['strong', 'b']):
            strong.replace_with(f"**{strong.get_text().strip()}**")
        
        # Process code blocks
        for code in soup.find_all('code'):
            code.replace_with(f"`{code.get_text().strip()}`")
        
        for pre in soup.find_all('pre'):
            pre.replace_with(f"```\n{pre.get_text().strip()}\n```")
        
        return soup.get_text()
    
    def _convert_table_to_markdown(self, table: BeautifulSoup) -> str:
        """Convert HTML table to Markdown format."""
        markdown_rows = []
        
        # Process headers
        headers = []
        for th in table.find_all('th'):
            headers.append(th.get_text().strip())
        
        if headers:
            markdown_rows.append('| ' + ' | '.join(headers) + ' |')
            markdown_rows.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
        
        # Process rows
        for tr in table.find_all('tr'):
            cells = []
            for td in tr.find_all('td'):
                cells.append(td.get_text().strip())
            if cells:
                markdown_rows.append('| ' + ' | '.join(cells) + ' |')
        
        return '\n'.join(markdown_rows)
    
    def _generate_hierarchical_path(self, data: Dict[str, Any]) -> str:
        """Generate a hierarchical path in Markdown format."""
        path_components = []
        
        if 'spaceId' in data:
            path_components.append(f"`space:{data['spaceId']}`")
        
        if 'parentId' in data and data['parentId']:
            path_components.append(f"`parent:{data['parentId']}`")
            
        path_components.append(f"`page:{data['id']}`")
        
        return ' > '.join(path_components)
    
    def _determine_content_type(self, data: Dict[str, Any]) -> str:
        """Determine the content type."""
        template_id = data.get('sourceTemplateEntityId', '')
        
        if 'projectplan-blueprint' in template_id:
            return 'project_plan'
        elif 'requirements-blueprint' in template_id:
            return 'requirements'
        elif 'meeting-notes' in template_id:
            return 'meeting_notes'
        return 'general_page'
    
    def format_for_embedding(self, node: ContentNode) -> str:
        """Format content for embedding in Markdown format."""
        formatted_parts = [
            f"# {node.title}",
            f"**Type:** {node.metadata['content_type']}",
            f"**Path:** {node.metadata['hierarchical_path']}",
            "",
            "## Content",
            node.content
        ]
        
        # Add children information if present
        if node.children:
            formatted_parts.extend([
                "",
                "## Child Pages",
                *[f"- {child.title}" for child in node.children]
            ])
        
        return "\n".join(formatted_parts)

def create_document_for_chroma(node: ContentNode, filepath: str) -> Dict[str, Any]:
    """Create a document format suitable for Chroma DB."""
    processor = MarkdownContentProcessor()
    formatted_content = processor.format_for_embedding(node)
    
    return {
        'id': node.id,
        'text': formatted_content,
        'metadata': {
            **node.metadata,
            'filepath': filepath,
            'title': node.title,
            'parent_id': node.parent_id
        }
    }