from typing import List

import abc

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from wid.web.url import Url




__all__ = ['Instructions']


class Instructions(abc.ABC):
    
    @abc.abstractmethod
    def validate(self, webdriver: WebDriver, url: Url) -> bool:
        """
        (Optional) Function that instructs webdriver how to pass validation for web page
        given by the url. User implemented instructions on how to bybass age validation,
        login, captcha etc. It's necessary to first load the URL and then take steps
        necessary to pass validation.
        
        Parameters
        -------------------------------------------------------------------------
            webdriver : WebDriver
                initiated Selenium webdriver instance
            urk : Url
                starting URL where the WebCrawler need to pass validation
            
        Returns
        -------------------------------------------------------------------------
            success : bool
                return true of the validation succeeded, false otherwise
        """    
        raise NotImplementedError
    
    @abc.abstractmethod
    def next_step(self, webdriver: WebDriver) -> List[Url]:
        """
        Function that parses the webdriver.current_url and finds a list of URLs that are
        to by added to WebCrawler's URL queue. URLs are processed in FIFO order.
        
        Parameters
        -------------------------------------------------------------------------
            webdriver : WebDriver
                initiated Selenium webdriver instance with current_url loaded

        Returns
        -------------------------------------------------------------------------
            urls : List[Url]
                list of URLs found on webdriver.curren_url
        """            
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_image_elements(self, webdriver: WebDriver) -> List[WebElement]:
        """
        Function that parses the webdriver.current_url and finds a list of image
        elements with source URLs that are to be downloaded by the WebCrawler.
        
        Parameters
        -------------------------------------------------------------------------
            webdriver : WebDriver
                initiated Selenium webdriver instance with current_url loaded

        Returns
        -------------------------------------------------------------------------
            image_elements : List[WebElement]
                list of WebElements containing desired images and their source URLs
        """   
        raise NotImplementedError
    
    
""" 
User-defined constant with the class name of the user's subclass of Instructions.
Used to dynamically import and instantiate the subclass of Instructions.

Must be defined by the user e.g. __InstructionClass__ = MyWebcrawlerInstructions
"""
__InstructionClass__ = Instructions
    