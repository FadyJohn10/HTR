import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

with open('input.txt', 'r') as file:
    URLs = [line.strip() for line in file] 

for url in URLs:
    print(f"Scraping: {url}")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    parsed_url = urlparse(url)
    folder_name = parsed_url.netloc.replace('.', '_')
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    images = soup.find_all('img')

    for img in images:
        srcset = img.get('srcset')
        if srcset:
            img_url = srcset.split(",")[-1].split()[0] 
        else:
            img_url = img.get('data-large-src') or img.get('src')
        
        if img_url and img_url.startswith('/'):
            img_url = f"{parsed_url.scheme}://{parsed_url.netloc}{img_url}"
        
        try:
            img_response = requests.get(img_url)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            continue
        
        content_type = img_response.headers.get('Content-Type', '')
        if 'image' in content_type:
            if 'jpeg' in content_type:
                extension = '.jpg'
            elif 'png' in content_type:
                extension = '.png'
            elif 'gif' in content_type:
                extension = '.gif'
            else:
                extension = ''
            
            img_name = os.path.basename(img_url).split("?")[0]
            img_name = img_name if img_name.endswith(extension) else img_name + extension
            
            with open(os.path.join(folder_name, img_name), 'wb') as img_file:
                img_file.write(img_response.content)
                print(f"Saved {img_name} to {folder_name}")
        else:
            print(f"URL is not an image: {img_url}")
