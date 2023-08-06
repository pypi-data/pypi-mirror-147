from types import ModuleType

import os
import sys
import importlib




__all__ = ['create_dir', 'import_module']


def create_dir(path_to_dir: str) -> None:
    """
    Function creates all nonexistent directories on the path_to_dir file path.
    
    Parameters
    -------------------------------------------------------------------------
        path_to_dir : str
            save file location for the image
            
    Returns
    -------------------------------------------------------------------------
        None
    """  
    if not os.path.isdir(path_to_dir):
        
        try:
            os.makedirs(path_to_dir)
        
        except Exception:
            print('Error: Failed to create target_dir \'{}\'.'.format(path_to_dir))
            
            
            
def import_module(path_to_file: str) -> ModuleType:
    """
    Function dynamically imports a Python module from source file located in path_to_file. 
    The new module is added into sys.modules dictionary. Name of the module is the basename
    of the path_to_file.
    
    Parameters
    -------------------------------------------------------------------------
        path_to_dir : str
            location of the module's source file
            
    Returns
    -------------------------------------------------------------------------
        module : ModuleType
            instance of a Python module class
    """      
    if not os.path.exists(path_to_file):
        raise FileNotFoundError('Error: File not found at location {}.'.format(path_to_file))
    
    module_name = os.path.basename(path_to_file)
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, path_to_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module
    
    except Exception:
        raise ImportError('Failed to import module {} from {}.'.format(module_name, path_to_file))
    