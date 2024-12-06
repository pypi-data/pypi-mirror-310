import os
from typing import List, Dict, Any, Tuple
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

from confluence.html_cleaner import MarkdownContentProcessor, create_document_for_chroma
from confluence.image_analyze import analyze_image
from confluence.text_processor import save_processed_content
from confluence.image_downloader import ImageDownloader

class ConfluenceClient:
    def __init__(self, base_url: str, username: str, api_token: str, markdown_filepath: str, images_filepath: str):
        authO = (username, api_token)
        self.base_url = base_url
        self.markdown_filepath = markdown_filepath
        self.images_filepath = images_filepath
        self.auth = aiohttp.BasicAuth(*authO)
        self.html_cleaner = MarkdownContentProcessor()
        self.image_downloader = ImageDownloader(base_url, username, api_token, images_filepath)
        
    async def get_spaces(self) -> List[str]:
        """
        Fetch all available Confluence spaces with pagination support.
        """
        spaces = []
        url = f"{self.base_url}/api/v2/spaces"
        params = {'limit': 250}  
        
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(url, params=params, auth=self.auth) as response:
                        response.raise_for_status()
                        data = await response.json()
                        
                        current_spaces = data.get('results', [])
                        spaces.extend([space['id'] for space in current_spaces])
                        
                        print(f"Fetched {len(current_spaces)} spaces") 
                        
                        links = data.get('_links', {})
                        next_link = links.get('next')
                        
                        if not next_link or not next_link.startswith('/'):
                            print("No more spaces to fetch")
                            break
                        
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(next_link)
                        query_params = parse_qs(parsed.query)
                        cursor = query_params.get('cursor', [None])[0]
                        
                        if not cursor:
                            print("No cursor found in next link")
                            break
                        
                        params['cursor'] = cursor
                        print(f"Moving to next page with cursor: {cursor[:30]}...") 
                        
                except Exception as e:
                    print(f"Error fetching spaces: {str(e)}")
                    break
        
        return spaces
    
    async def fetch_content(self, spaces: List[str]) -> List[Dict[str, Any]]:
        """Fetch content from specified spaces with proper structuring."""
        documents = []
        
        for space_key in spaces:
            base_path = f"{self.base_url}/api/v2/spaces/{space_key}/pages"
            params = {'limit': 250}
            has_more = True
            
            while has_more:
                async with aiohttp.ClientSession() as session:
                    async with session.get(base_path, params=params, auth=self.auth) as response:
                        response.raise_for_status()
                        data = await response.json()
                        content_items = data.get('results', [])
                        
                        for item in content_items:
                            content, images = await self._fetch_page_content(item['id'])

                            doc = {
                                'content': content['text'],  
                                'metadata': {
                                    **content['metadata'],  
                                    'space_key': space_key,  
                                    'source': 'confluence',
                                }
                            }
                            documents.append(doc)
                        
                        links = data.get('_links', {})
                        next_link = links.get('next')
                        
                        if next_link and next_link.startswith('/'):
                            parsed = urlparse(next_link)
                            query_params = parse_qs(parsed.query)
                            cursor = query_params.get('cursor', [None])[0]
                            
                            if cursor:
                                params['cursor'] = cursor
                            else:
                                has_more = False
                        else:
                            has_more = False
                            
        return documents
    
    async def process_images(self, images: List[str]) -> Dict[str, str]:
        """Process multiple images and return their descriptions."""
        image_descriptions = {}
        for image_path in images:
            img_path = os.path.join(self.images_filepath, image_path)
            if os.path.exists(img_path):
                description = await analyze_image(img_path)
                image_descriptions[os.path.basename(img_path)] = description
        return image_descriptions

    async def _fetch_page_content(self, page_id: str) -> Tuple[Dict[str, Any], List[str]]:
        """Fetch and process individual page content."""
        url = f"{self.base_url}/api/v2/pages/{page_id}"
        params = {'body-format': 'view'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, auth=self.auth) as response:
                response.raise_for_status()
                content_json = await response.json()
                
                images = await self._extract_images(content_json)

                image_descriptions = await self.process_images(images)

                processed_node = self.html_cleaner.process_content(content_json, image_descriptions)

                file_path = save_processed_content(processed_node, self.markdown_filepath)
                print(f"Content saved to: {file_path}")

                chroma_doc = create_document_for_chroma(processed_node, file_path)
                
                return chroma_doc, images
    
    async def _extract_images(self, content_json: Dict[str, Any]) -> List[str]:
        """Extract images from content while maintaining context."""
        html_content = content_json.get('body', {}).get('view', {}).get('value', '')
        soup = BeautifulSoup(html_content, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                image_filename = await self.image_downloader.download_image(src)
                if image_filename:
                    images.append(image_filename)
                    img.replace_with(BeautifulSoup(f"\n[Image: {image_filename}]\n", 'html.parser'))
                
        return images