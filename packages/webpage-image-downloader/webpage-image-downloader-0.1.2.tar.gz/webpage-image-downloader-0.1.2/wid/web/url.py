from __future__ import annotations

from typing import List

import re
import functools

import urllib.parse




__all__ = ['Url']


class Url(str):
    """ 
    Class Url represents the individual part of the URL accoring to the
    standard RFC_1808 (https://www.rfc-editor.org/rfc/rfc1808.html). 
    
    URL structure - <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    
    Attributes
    -------------------------------------------------------------------------
        scheme : str
            scheme name, as per Section 2.1 of RFC 1738
        netloc : str
            network location and login information, as per Section 3.1 of RFC 1738
        path : str
            URL path, as per Section 3.1 of RFC 1738
        params : str
            object parameters, e.g., ";type=a", as in Section 3.2.2 of RFC 1738
        query : str
            query information, as per Section 3.3 of RFC 1738
        fragment : str
            fragment identifier
        
    Methods
    -------------------------------------------------------------------------
        is_valid(self) -> bool
            returns True if the instance is a valid URL, False otherwise
        get_base_url(self) -> str
            returns the base name of the URL - scheme + netlock
        match(self, re.Pattern) -> bool
            returns True if the URL matches the structure of a URL, False otherwise
    
    Static Methods
    -------------------------------------------------------------------------
        filter_url_list(List[Url], str) -> List[Url]
            returns a subset of URLs from the input list that match given regex
    
    """
    
    
    _url_regex = ("((http|https|ftp)://)(www.)?" +
                "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                "{2,256}\\.[a-z]" +
                "{2,6}\\b([-a-zA-Z0-9@:%" +
                "._\\+~#?&//=]*)")
    
    _url_pattern = re.compile(_url_regex)

    

    def __init__(self, url_string: str, default_scheme: str='https://') -> None:
        """
        Constructs an instance of the class Url. Doesn't work for relative URIs.
        
        Uses urllib to parse the input url_string. This library requires the
        URL to have a scheme to function properly. Constructor automatically
        prepends default_scheme to the url_string if none is present.
        
        Parameters
        -------------------------------------------------------------------------
            url_string : str
                input url string
            default_scheme : str
                default scheme to be used if there is no scheme in the input url
        """
        
        self.url_string = url_string if '//' in url_string else default_scheme + url_string
                
        parsed_url = urllib.parse.urlparse(self.url_string)
        
        self.scheme = parsed_url.scheme
        self.netloc = parsed_url.netloc
        self.path = parsed_url.path
        self.params = parsed_url.params
        self.query = parsed_url.query
        self.fragment = parsed_url.fragment
        
            
    
    def is_valid(self) -> bool:  
        """
        Function checks the validity of the URL represented by an instance of the class.
        
        Returns
        -------------------------------------------------------------------------
            is_valid : bool
                True if the _url_pattern matches represented URL, False otherwise
        """
        if not self._url_pattern.match(self.__str__()):
            return False  
        
        else:
            return True
        
        
        
    def get_base_url(self) -> str:
        """
        Function returns the base name of the URL. Base name has the following form:
        
        <scheme>://<netloc>
        
        Returns
        -------------------------------------------------------------------------
            base_url : str
                string representing the base name of the URL
        """        
        if self.scheme is not None and self.scheme != '':
            return self.scheme + '://' + self.netloc
        
        else:
            return self.netloc
    
    
    
    def match(self, pattern: re.Pattern) -> bool:
        """
        Function checks if the URL represented by an instance of the class matches
        the provided pattern.
        
        Parameters
        -------------------------------------------------------------------------
            pattern : re.Pattern
                precompiled pattern from a regex expression used to match the URL
            
        Returns
        -------------------------------------------------------------------------
            is_match : bool
                True if URL matches the patter, False otherwise
        """   
        
        if pattern.match(self.url_string):
            return True
        
        else:
            return False
        
        
    
    def __eq__(self, __x: object) -> bool:
        
        return super().__eq__(__x)
        
     
        
    def __hash__(self) -> int:
        return super().__hash__()
    
    
        
    def __repr__(self) -> str:
        
        return self.__str__()
    
            
            
    def __str__(self) -> str:
        
        return urllib.parse.urlunparse((self.scheme,
                                        self.netloc,
                                        self.path,
                                        self.params,
                                        self.query,
                                        self.fragment))
            
    
    
    @functools.singledispatchmethod
    @classmethod
    def filter_url_list(cls, url_filter, url_list: List[Url]) -> List[Url]:
        """
        Function filters a list of instances of Url class.
        
        Parameters
        -------------------------------------------------------------------------
            url_filter : str or re.Pattern
                filter used on the list of URLs, can be a regex string or a re.Pattern instance
            
        Returns
        -------------------------------------------------------------------------
            list : List[Url]
                list of Url class instances that match the provided regex expression
        """     
        raise NotImplementedError('TypeError:Filter argument is not a supported type.')
              
    @filter_url_list.register(str)
    @classmethod
    def _(cls, url_filter, url_list: List[Url]) -> List[Url]:
        pattern = re.compile(url_filter)
        filter_func = lambda x: re.match(pattern, x)
        return list(filter(filter_func, url_list))
    
    @filter_url_list.register(re.Pattern)
    @classmethod
    def _(cls, url_filter, url_list: List[Url]) -> List[Url]:
        filter_func = lambda x: re.match(url_filter, x)
        return list(filter(filter_func, url_list))
    
    

