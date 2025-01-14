import requests
from django.conf import settings


def generate_article_content(title):
    """
    Calls an external LLM service (e.g., OpenAI GPT-3) to generate article content.
    return a static content in case of error
    """
    content = "Generated article content using LLM"
    try:
        content = make_external_call(title) or content
    except Exception as e:
        print(e) # should be logged
    return content

def generate_tags(title):
    """
    Calls an external LLM service to generate tags based on the article content.
    return a static content in case of error
    """
    tags = "AI, Technology, LLM"
    try:
        tags = make_external_call(title, is_tag_prompt=True) or tags
    except Exception as e:
        print(e) # should be logged
    return tags

def make_external_call(title, is_tag_prompt=False):
    request_data = {
            'model': 'gpt-3.5-turbo',
            'prompt': f"Write a short blog post about: {title}",
            'max_tokens': 50
        }
    if is_tag_prompt:
        request_data['prompt'] = f"Suggest tags for this article: {title}",
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {settings.OPENAI_API_KEY}'},
        json=request_data
    )
    if response.status_code == 200:
        data = response.json()
        return data.get('choices', [{}])[0].get('text', '').strip()