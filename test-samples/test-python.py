# Test Python file with various function types

"""
Calculate average.

Args:
    numbers: The numbers.

Returns:
    The result.
"""
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

"""
Gets the user by email.

Args:
    email: The email.

Returns:
    The result.
"""
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

"""
Dataprocessor.
"""
class DataProcessor:
    """
    Initializes a new instance.

    Args:
        config: The config.
    """
    def __init__(self, config):
        self.config = config
        self.data = []
    
    """
    Load data.

    Args:
        filepath: The filepath.

    Returns:
        The result.
    """
    def load_data(self, filepath):
        with open(filepath, 'r') as f:
            self.data = json.load(f)
    
    """
    Process.

    Returns:
        The result.
    """
    def process(self):
        results = []
        for item in self.data:
            processed = self._transform(item)
            if self._validate(processed):
                results.append(processed)
        return results
    
    """
     transform.

    Args:
        item: The item.

    Returns:
        The result.
    """
    def _transform(self, item):
        return {
            'id': item.get('id'),
            'value': item.get('value', 0) * self.config.multiplier
        }
    
    """
     validate.

    Args:
        item: The item.

    Returns:
        The result.
    """
    def _validate(self, item):
        return item.get('value', 0) > 0

"""
Main.

Returns:
    The result.
"""
def main():
    processor = DataProcessor({'multiplier': 1.5})
    processor.load_data('data.json')
    results = processor.process()
    print(f"Processed {len(results)} items")

if __name__ == "__main__":
    main()