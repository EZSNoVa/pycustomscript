"""
This module is responsible providing decorators for an easier way to interact with magic methods
"""
from functools import cache

def Derive(*decorators, property_name: str = None):
    """
    Decorator that applies multiple decorators to a class

    ### Parameters:
    - `decorators`: The decorators to be applied to the class
    - `property_name`: The name of the property that will be used to apply the decorators (Note: It will be apply to all decorators)

    ### Example:
    ```py
    @Derive(Iter, Get, property_name="items")
    class MyClass:
        def __init__(self, items):
            self.items = items
    """

    def decorator(cls):
        for decorator in decorators:
            if property_name:
                cls = decorator(property_name)(cls)
            else:
                cls = decorator(cls)

        return cls

    return decorator

def Iter(property_name: str):
    """
    Decorator that adds the `__iter__` and `__next__` methods to a class

    ### Parameters:
    - `property_name`: The name of the property that will be used to iterate over the class

    ### Example:
    ```py
    @Iter('items') # make sure that a property named 'items' exists within the class
    class MyClass:
        def __init__(self, items):
            self.items = items 
            ...

    my_class = MyClass([1, 2, 3])
    for item in my_class:
        print(item)
    ```    
    """
    def decorator(cls):
        # Define the __iter__ method
        @cache
        def __iter__(self):
            return iter(getattr(self, property_name))

        # Define the __next__ method
        @cache
        def __next__(self):
            return next(iter(getattr(self, property_name)))

        # Add the __iter__ and __next__ methods to the class
        cls.__iter__ = __iter__
        cls.__next__ = __next__

        return cls

    return decorator


def Get(property_name: str, default=None):
    """
    Decorator that adds the `__getitem__` method to a class

    ### Parameters:
    - `property_name`: The name of the property that will be used to get items from the class
    - `default`: The default value to return if the item is not found, if is set to `"error"` and the item is not found, a `KeyError` will be raised

    ### Example:
    ```py
    @Get('items', default="error") # make sure that a property named 'items' exists within the class
    class MyClass:
        def __init__(self, items):
            self.items = items

    my_class = MyClass([1, 2, 3])
    print(my_class[0]) # 1
    """

    def decorator(cls):
        # Define the __getitem__ method
        @cache
        def __getitem__(self, key):
            if default == "error":
                return getattr(self, property_name)[key]
            return getattr(self, property_name).get(key, default)                
            

        # Add the __getitem__ method to the class
        cls.__getitem__ = __getitem__

        return cls

    return decorator

def Set(property_name: str, create_if_not_exists: bool = False):
    """
    Decorator that adds the `__setitem__` method to a class

    ### Parameters:
    - `property_name`: The name of the property that will be used to set items from the class
    - `create_if_not_exists`: If `True` the property will be created if it doesn't exists (Default: `False`)
    """

    def decorator(cls):
        # Define the __setitem__ method
        @cache
        def __setitem__(self, key, value):
            if not getattr(self, property_name).get(key):
                if create_if_not_exists:
                    getattr(self, property_name)[key] = value
                else:
                    raise KeyError(f"Key '{key}' not found in '{property_name}'")
                
            else:
                getattr(self, property_name)[key] = value

        # Add the __setitem__ method to the class
        cls.__setitem__ = __setitem__

        return cls

    return decorator

