from typing import List, Callable

import os
from collections import deque

from selenium.common.exceptions import WebDriverException

import wid.web.img.save
import wid.web.img.scrape

from wid.web.url import Url
from wid.web.bot.instructions import Instructions


# TODO: URL normalization / canonicalization
# E.g. example.com/, example.com, example.com/index.html, example.com/index.php -> one single URL
# => Use url-normalize library for Python?


__all__  = ['WebCrawler']


class WebCrawler():
    """ 
    Class WebCrawler is used to parse URLs, find and save desired images and
    search for next set of URLs to explore. WebCrawler will continue to function
    while there are URLs in it's url_queue.
    
    Attributes
    -------------------------------------------------------------------------
        webdriver : selenium.webdriver.remote.webdriver.WebDriver
            instance of Selenium's Chrome webdriver 
        instructions : web.bot.Instructions
            instance of user-defined subclass of web crawler Instructions
        url_queue : deque[Url]
            FIFO queue of URLs that are explored by the web crawler
        url_visited : set[Url]
            set of URLs already visited by the web crawler
        target_dir : str
            directory path for saving image files
        
    Methods
    -------------------------------------------------------------------------
        crawl(self) -> None
            starts the WebCrawler, navigates and scrapes web pages and downloads image files
            until there are no URLs left in url_queue.
        _navigate_url(self, target_url: Url) -> None
            uses WebDriver to load target_url and adds it to url_visited set
        _get_next_url_list(self, current_url: Url, step_function: Callable[[Url], List[Url]]=None) -> List[Url]
            uses Instructions.next_step() or step_function() to get a set of not-visited URLs
        _find_image_urls(self, visited_page_url: Url) -> List[Url]
            finds src of desired image elements using Instructions.find_image_elements() on the currently loaded web page
        _download_images(self, image_urls: List[Url]) -> None
            downloads a list of images and saves them in location self.target_dir        
    """    
    def __init__(self, instructions: Instructions, starting_url: Url, target_dir: str='./wid-images') -> None:

        if not starting_url.is_valid():
            print('ValueError: Invalid target URL: \'{}\'.'.format(starting_url))
            raise ValueError
        
        self.webdriver = None
        self.instructions = instructions
        
        self.url_queue = deque([starting_url])
        self.url_visited = set()

        self.target_dir = target_dir

                
  
    def crawl(self) -> None:
        
        self.webdriver = wid.web.img.scrape.initialize_webdriver()
        self.instructions.validate(self.webdriver, self.url_queue[0])
        
        while len(self.url_queue) > 0:
            target_url = self.url_queue.popleft()
            print('Parsing web page \'{}\'.'.format(target_url))
            
            try:
                self._navigate_url(target_url)
                image_urls = self._find_image_urls(target_url)
                self._download_images(image_urls)

                next_urls = self._get_next_url_list()
                self.url_queue.extend(next_urls)
                   
            except WebDriverException:
                # Failed to load next web page -> continue with next in queue 
                continue
            
        self.webdriver.quit()            
            
            
            
    def _navigate_url(self, target_url: Url) -> None:
        # Add both target_url and url loaded by the webdriver in case of inconsistencies
        # -> avoid endless loop of navigation
        if self.webdriver is None:
            raise ValueError('WebDriver is not initialized in WebCrawler.')        
        
        self.webdriver.get(target_url)
        self.url_visited.add(target_url)
        self.url_visited.add(self.webdriver.current_url)
        
        
        
    def _get_next_url_list(self, step_function: Callable[[Url], List[Url]]=None) -> List[Url]:
        
        if step_function is None:
            next_url_list = self.instructions.next_step(self.webdriver)
        else:
            step_function(self.webdriver)

        valid_url_list = [url for url in next_url_list if url.is_valid()]
        return [url for url in valid_url_list if url not in self.url_visited]

    
    
    def _find_image_urls(self, visited_page_url: Url) -> List[Url]:
        if self.webdriver is None:
            raise ValueError('WebDriver is not initialized in WebCrawler.')    
        
        image_elements = self.instructions.find_image_elements(self.webdriver)
        return [wid.web.img.scrape.get_element_src(e, visited_page_url) for e in image_elements]
    
    
    
    def _download_images(self, image_urls: List[Url]) -> None:
        if self.webdriver is None:
            raise ValueError('WebDriver is not initialized in WebCrawler.') 

        url_dir_name = self.webdriver.current_url.split('/')[-2]
        dir_path = os.path.join(self.target_dir, url_dir_name)
        wid.web.img.save.save_images(image_urls, dir_path)
        
        

    