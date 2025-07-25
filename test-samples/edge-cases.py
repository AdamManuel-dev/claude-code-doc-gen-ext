# Edge cases for Python

# Empty function
def empty_function():
    pass

# Function with existing docstring
def already_documented(x):
    """This function already has documentation."""
    return x * 2

# Nested function
def outer_function():
    def inner_function():
        return "nested"
    return inner_function()

# Function with type hints
def typed_function(name: str, age: int) -> str:
    return f"{name} is {age} years old"

# Function with *args and **kwargs
def variable_args(*args, **kwargs):
    return len(args) + len(kwargs)

# Lambda (should be ignored)
square = lambda x: x ** 2

# Empty class
class EmptyClass:
    pass

# Class with existing docstring
class DocumentedClass:
    """This class is already documented."""
    def method(self):
        return "method"

# Static and class methods
class SpecialMethods:
    @staticmethod
    def static_method():
        return "static"
    
    @classmethod
    def class_method(cls):
        return "class"

# Property decorator
class PropertyExample:
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val

# Async function
async def async_function():
    return "async"