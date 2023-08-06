from typing import List

import os
import requests
from urllib.request import urlretrieve

import wid.file.utils
from wid.web.url import Url




__all__ = ['save_images', 'download_image']

             
def save_images(url_list: List[Url], path_to_dir: str) -> None:
    """
    Function saves a set of images from a list of URLs to a location on disk.
    Each image is saved using web.img.save.download_image() function. 
    If there are any missing directories on the path_to_dir, they are created
    using wid.file.utils.create_dir().
    
    
    Parameters
    -------------------------------------------------------------------------
        url_list : List[web.url.Url]
            list of URL references to images
        path_to_dir : str
            save file location for the images in url_list
            
    Returns
    -------------------------------------------------------------------------
        None
    """   
    wid.file.utils.create_dir(path_to_dir)
    
    for url in url_list:
        
        try:
            print('Downloading image from \'{}\'.'.format(url))
            download_image(url, path_to_dir)
        
        except Exception as e:
            raise e
            print('Could not retrieve image from \'{}\'.'.format(url))



def download_image(url: Url, path_to_dir: str = './') -> None:
    """
    Function downloads a single image pointed to by a URL and save it to a
    location on the disk. If a location is not provided by the path_to_dir
    parameter, then working directory './' is used by default.
    
    Name of the image file is the basename of the path portion of the URL.
    It is the string after last '/' symbol e.g.:
    https://duckduckgo.com/assets/icons/header/reddit.svg -> reddit.svg
    
    Parameters
    -------------------------------------------------------------------------
        url : web.url.Url
            URL reference to the image
        path_to_dir : str
            save file location for the image
            
    Returns
    -------------------------------------------------------------------------
        None
    """   
    if url is not None:
        img_path = url.path
        img_basename = os.path.basename(img_path)
        save_file_path = os.path.join(path_to_dir, img_basename) 
        
        try:
            urlretrieve(url, save_file_path)
        
        except Exception:
            with requests.get(url, stream=True) as r:
                with open(save_file_path, 'wb') as f:
                    f.write(r.content)
                

            