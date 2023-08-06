import os

import click
import pyperclip

from wid.web.url import Url

import wid.web.img.save
import wid.web.img.scrape

import wid.file.utils




@click.command()
@click.option('--url', '-u', default=None, help='Url of the website containing desired images. Contents of the clipboard are used if none is provided.')
@click.option('--target-dir', '-t', default=None, help='Target directory used to store images.')
@click.option('--img-regex', '-r', default=None, help='Regex for finding specific subset of images on the website.')

@click.option('--img-info', '-i', is_flag=True, help='Option to find and print all image URLs on the website.')
@click.option('--page-source', '-p', is_flag=True, help='Option to get the source code of target website and print it (save it).')
def main(url: str, target_dir: str, img_regex: str, img_info: bool, page_source: bool) -> None:
    
    """ Python script for extracting and saving images from websites. """
        
    url_string = pyperclip.paste() if url is None else url
    target_url = Url(url_string)
    
    if target_url is None or not target_url.is_valid():
        click.echo('Error: Target URL is invalid.')    
        click.echo(main.get_help(click.Context(main)))
        exit()
    
    if img_info:
        get_img_info(target_url, img_regex)
        
    if page_source:
        target_dir = target_dir if target_dir is not None else './wid-page-source'
        get_page_source(target_url, target_dir)
       
    if not img_info and not page_source:
        target_dir = target_dir if target_dir is not None else './wid-images'
        download_images(target_url, target_dir, img_regex)
        


def get_img_info(target_url: Url, img_regex: str) -> None:

    click.echo('Starting to parse {}...'.format(target_url))

    try:
        # Find URLs for all images on target website   
        image_urls = wid.web.img.scrape.find_image_urls(target_url)
        
        # Filter image links
        if img_regex is not None:
            image_urls = Url.filter_url_list(img_regex, image_urls)

        # Print the URLs of images 
        print('Images found:')
        for url in image_urls:
            if url is not None:
                print(url)
            
    except Exception as e:
        click.echo('Failed.')        
        raise e
        
    else:
        click.echo('Done.')
        
        
        
def get_page_source(target_url: Url, target_dir: str) -> None:

    click.echo('Attempting to open {}...'.format(target_url))

    try:
        # Load the page and get its source code
        page_src = wid.web.img.scrape.get_page_source(target_url)
            
        # Save the source code to a file (implement in save.py)
        file_name = target_url.netloc + '.txt'
        save_file_path = os.path.join(target_dir, file_name).replace('\\', '/')
        wid.file.utils.create_dir(target_dir)

        with open(save_file_path, 'w', encoding='utf8') as f:
            f.write(page_src)
            
    except Exception:
        click.echo('Failed.')        
        
    else:
        click.echo('Page source code saved.')
        
        

def download_images(target_url: Url, target_dir: str, img_regex: str) -> None:
    
    click.echo('Starting to parse {}...'.format(target_url))
        
    try:
        # Find URLs for all images on target website   
        image_urls = wid.web.img.scrape.find_image_urls(target_url)
        
        # Filter images
        if img_regex is not None:
            image_urls = Url.filter_url_list(img_regex, image_urls)
        
        # Store images in target location
        wid.web.img.save.save_images(image_urls, target_dir)    
    
    except Exception:
        click.echo('Failed.')        
    
    else:
        click.echo('Done.')
        


if __name__ == "__main__":
    
    main()