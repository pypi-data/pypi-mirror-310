import base64

from openai import AsyncOpenAI
from src.config.settings import Settings

config = Settings()

async def analyze_image(image_path):
    client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
    
    try:
        with open(image_path, "rb") as image_file:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please analyze and describe this image in detail, focusing on the technical aspects such as flow diagrams, data flow, or system architecture. Identify key components, their relationships, and how information or processes move between them. Mention any labels, arrows, or symbols used in the diagram, and explain the overall functionality or workflow being represented."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=700,
            )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing image {image_path}: {str(e)}")
        return "Image analysis failed"