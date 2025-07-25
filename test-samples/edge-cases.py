# Edge cases for Python

# Empty function
def empty_function():
    """
    Empty function.

    Returns:
        The result.
    """
    pass

# Function with existing docstring
def already_documented(x):
    """This function already has documentation."""
    return x * 2

# Nested function
def outer_function():
    """
    Outer function.

    Returns:
        The result.
    """
    def inner_function():
        """
        Inner function.

        Returns:
            The result.
        """
        return "nested"
    return inner_function()

# Function with type hints
def typed_function(name: str, age: int) -> str:
    return f"{name} is {age} years old"

# Function with *args and **kwargs
def variable_args(*args, **kwargs):
    """
    Variable args.

    Args:
        *args: The *args.
        **kwargs: The **kwargs.

    Returns:
        The result.
    """
    return len(args) + len(kwargs)

# Lambda (should be ignored)
square = lambda x: x ** 2

# Empty class
class EmptyClass:
    """
    Emptyclass.
    """
    pass

# Class with existing docstring
class DocumentedClass:
    """This class is already documented."""
    def method(self):
        """
        Method.

        Returns:
            The result.
        """
        return "method"

# Static and class methods
class SpecialMethods:
    """
    Specialmethods.
    """
    @staticmethod
    def static_method():
        """
        Static method.

        Returns:
            The result.
        """
        return "static"
    
    @classmethod
    def class_method(cls):
        """
        Class method.

        Args:
            cls: The cls.

        Returns:
            The result.
        """
        return "class"

# Property decorator
class PropertyExample:
    """
    Propertyexample.
    """
    @property
    def value(self):
        """
        Value.

        Returns:
            The result.
        """
        return self._value
    
    @value.setter
    def value(self, val):
        """
        Value.

        Args:
            val: The val.

        Returns:
            The result.
        """
        self._value = val

# Async function
async def async_function():
    return "async"