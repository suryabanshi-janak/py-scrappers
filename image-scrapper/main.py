from selectolax.parser import HTMLParser
from httpx import get

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

if __name__ == '__main__':
  img_nodes = get_img_tags_for('galaxy')
  relevant_imgs = [i for i in img_nodes if filter_out_img(i.attrs['src'], ['base64', 'plus', 'profile', 'premium'])]

  all_img_urls = [get_high_res_img_url(i) for i in relevant_imgs]
  print(all_img_urls)
  

  # for u in relevant_imgs:
  #   print(u)
    
  # print(len(relevant_imgs))