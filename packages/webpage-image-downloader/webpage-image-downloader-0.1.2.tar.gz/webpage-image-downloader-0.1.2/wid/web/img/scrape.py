from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.common.exceptions import WebDriverException

from webdriver_manager.chrome import ChromeDriverManager

from wid.web.url import Url




__all__ = ['initialize_webdriver', 'find_image_urls', 'get_element_src', 'get_page_source']


def initialize_webdriver() -> WebDriver:
    """
    Function initialized a headless Chrome webdriver instance with suppressed
    warnings/errors.
    
    Returns
    -------------------------------------------------------------------------
        driver : selenium.remote.webdriver.WebDriver
           webdriver instance
    """           
    chrome_driver_path = ChromeDriverManager().install()

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--log-level=3')
    
    return webdriver.Chrome(chrome_driver_path,
                            chrome_options=chrome_options)
    
    

def find_image_urls(target_url: Url) -> List[Url]:
    """
    Function searches the web page referenced by target_url for images. The function
    looks through the DOM tree structure for 'img' elements and return a list of URLs
    referencing each image.
    
    Parameters
    -------------------------------------------------------------------------
        target_url : web.url.Url
            url of the target website
    Returns
    -------------------------------------------------------------------------
        image_list : List[web.url.Url]
           list of URLs to images found on the website
    """      
    if not target_url.is_valid():
        print('ValueError: Invalid target URL: \'{}\'.'.format(target_url))
        raise ValueError
    
    driver = initialize_webdriver()
    
    try:
        driver.get(target_url)
      
        image_elements = driver.find_elements_by_tag_name('img')
        image_urls = [get_element_src(e, target_url) for e in image_elements]

        driver.close()

    except WebDriverException as e:
        print('Error: Could not resolve site \'{}\'.'.format(target_url))
        raise e

    finally:
        driver.quit()

    return image_urls



def get_element_src(element: WebElement, url: Url) -> Url:
    """
    Function returns the source URL for given element. If the source URL is
    relative then the function takes base_name from the provided URL and prepends
    it to the relative URL.
    
    Parameters
    -------------------------------------------------------------------------
        element : selenium.webdriver.remote.webelement.WebElement
            HTML element
        url : web.url.Url
            url of the web page where the element is located
            
    Returns
    -------------------------------------------------------------------------
        url : web.url.Url
           source URL of given element
    """     
    # Elements with absolute URLs
    if element.get_attribute('src'):
        url_string = element.get_attribute('src')
        return Url(url_string)
        
    # Elements relative URLs -> prepend base address if needed
    elif element.get_attribute('data-src'):
        
        url_string = element.get_attribute('data-src').strip()
        src = Url(url_string)

        if src.is_valid(): 
            return src
        
        else:
            url_string = url.get_base_url().strip() + element.get_attribute('data-src')
            return Url(url_string)
    
    # Element has neither attribute -> missing a link?
    else:
        return None
    
    

def get_page_source(target_url: Url) -> str:
    """
    Function returns the full HTML source code of the web page referenced by
    target_url.
    
    Parameters
    -------------------------------------------------------------------------
        url : web.url.Url
            url of a web page
            
    Returns
    -------------------------------------------------------------------------
        page_source : str
           string containing the source code of given web page
    """   
    if not target_url.is_valid():
        print('ValueError: Invalid target URL: \'{}\'.'.format(target_url))
        raise ValueError        
    
    driver = initialize_webdriver()
    
    try:
        driver.get(target_url)
        
        page_source = driver.page_source
        
        driver.close()
                
    except WebDriverException as e:
        print('Error: Could not resolve site \'{}\'.'.format(target_url))
        raise e
    
    finally:
        driver.quit()
        
    return page_source
