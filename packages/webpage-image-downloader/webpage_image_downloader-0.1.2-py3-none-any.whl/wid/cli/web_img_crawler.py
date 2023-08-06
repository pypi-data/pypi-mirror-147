import click
import pyperclip

from wid.web.url import Url
from wid.web.bot.webcrawler import WebCrawler
from wid.web.bot.instructions import Instructions

from wid.file.utils import import_module




@click.command()
@click.option('--url', '-u', default=None, help='Url of the starting website for the web crawler. Contents of the clipboard are used if none is provided.')
@click.option('--instructions', '-i', default=None, help='Implementation of Instructions abstract class used by the WebCrawler.')
@click.option('--target-dir', '-t', default=None, help='Target directory used to store images.')
def main(url, instructions, target_dir):
    
    """ Python web crawler for extracting and saving images from websites. """    

    url = pyperclip.paste() if url is None else url
    target_url = Url(url)
    target_dir = target_dir if target_dir is not None else './wid-images'
    
    if target_url is None or not target_url.is_valid():
        click.echo('Error: Target URL is invalid.')    
        click.echo(main.get_help(click.Context(main)))
        exit()
    
    try:
        instructions_module = import_module(instructions)
        webcrawler_instructions = instructions_module.__InstructionClass__()
        
    except Exception:
        raise ImportError('Failed to import and instantiate user-defined Instructions class from {}.'.format(instructions))

    start_crawler(webcrawler_instructions, target_url, target_dir)



def start_crawler(instructions: Instructions, starting_url: Url, target_dir: str) -> None:
    
    if not starting_url.is_valid():
        raise ValueError('ValueError: Invalid target URL: \'{}\'.'.format(starting_url))
    
    click.echo('Starting web crawler on page {}.'.format(starting_url))
    
    webcrawler = WebCrawler(instructions, starting_url, target_dir)
    webcrawler.crawl()

    click.echo('Done.')
    
    

if __name__ == "__main__":
    
    main()