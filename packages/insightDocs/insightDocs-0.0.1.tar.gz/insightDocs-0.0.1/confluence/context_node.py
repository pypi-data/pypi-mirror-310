from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ContentNode:
    id: str
    title: str
    content: str
    parent_id: Optional[str]
    children: List['ContentNode']
    metadata: Dict[str, Any]
