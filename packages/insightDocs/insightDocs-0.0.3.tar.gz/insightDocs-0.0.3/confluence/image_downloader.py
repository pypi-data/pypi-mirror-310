import os
import uuid
import aiohttp
import logging
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageDownloader:
    ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg')
    ALLOWED_MIME_TYPES = ('image/png', 'image/jpeg')

    def __init__(self, base_url: str, username: str, api_token: str, save_path: str):
        self.base_url = base_url
        self.username = username
        self.api_token = api_token
        self.save_path = save_path
        
        # Ensure save directory exists
        Path(save_path).mkdir(parents=True, exist_ok=True)

    def _get_file_extension(self, url: str, content_type: Optional[str] = None) -> Optional[str]:
        """
        Determine file extension from URL and content type.
        Returns None if extension is not allowed.
        """
        path = urlparse(url).path.lower()
        url_ext = os.path.splitext(path)[1]
        
        if url_ext in self.ALLOWED_EXTENSIONS:
            return url_ext

        if content_type:
            if content_type == 'image/jpeg':
                return '.jpg'
            elif content_type == 'image/png':
                return '.png'
            
        return None

    def _prepare_url(self, url: str) -> str:
        """Prepare URL by adding base URL if needed."""
        if not url.startswith(('http://', 'https://')):
            return f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        return url

    async def download_image(self, url: str) -> Optional[str]:
        """
        Download image from URL and save it with a unique filename.
        Returns the filename if successful, None otherwise.
        """
        try:
            url = self._prepare_url(url)
            logger.info(f"Attempting to download image from: {url}")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    auth=aiohttp.BasicAuth(self.username, self.api_token),
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status != 200:
                        logger.error(f"Failed to download image. Status: {response.status}")
                        return None

                    content_type = response.headers.get('content-type', '').lower()
                    if content_type not in self.ALLOWED_MIME_TYPES:
                        logger.warning(f"Unsupported content type: {content_type}")
                        return None

                    extension = self._get_file_extension(url, content_type)
                    if not extension:
                        logger.warning("Could not determine valid file extension")
                        return None

                    filename = f"{uuid.uuid4()}{extension}"
                    filepath = os.path.join(self.save_path, filename)

                    try:
                        with open(filepath, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                        
                        logger.info(f"Successfully downloaded image: {filename}")
                        return filename

                    except IOError as e:
                        logger.error(f"Failed to save image: {e}")

                        if os.path.exists(filepath):
                            os.remove(filepath)
                        return None

        except aiohttp.ClientError as e:
            logger.error(f"Network error while downloading image: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while downloading image: {e}")
            return None
