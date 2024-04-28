import os
from selectolax.parser import HTMLParser
from httpx import get
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_img_tags_for(term):
  if not term:
    raise Exception('No search term provided')
  
  url = f"https://unsplash.com/s/photos/{term}"
  resp = get(url)

  if resp.status_code != 200:
    raise Exception('Error getting response')

  tree = HTMLParser(resp.text)
  imgs = tree.css('figure a img')
  return imgs

def filter_out_img(url: str, keywords: list) -> bool:
  return not any(x in url for x in keywords)

def get_high_res_img_url(img_node):
  srcset = img_node.attrs['srcset']
  srcset_list = srcset.split(', ')

  url_res = srcset_list[0].split('?')[0]

  return url_res

def save_images(img_urls, dest_dir='images', tag=''):
  for url in img_urls:
    resp = get(url)
    logging.info(f"Downloading {url}...")

    file_name = url.split('/')[-1]

    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir)
    
    with open(f"{dest_dir}/{tag}{file_name}.jpeg", "wb") as f:
      f.write(resp.content)
      logging.info(f"Saved {file_name}, with size {round(len(resp.content)/1024/1024,2)} MB.")

if __name__ == '__main__':
  search_tag = "cat"
  dest_dir = "images"

  img_nodes = get_img_tags_for(search_tag)
  relevant_imgs = [i for i in img_nodes if filter_out_img(i.attrs['src'], ['base64', 'plus', 'profile', 'premium'])]

  all_img_urls = [get_high_res_img_url(i) for i in relevant_imgs]
  
  save_images(all_img_urls[:3], dest_dir, search_tag)