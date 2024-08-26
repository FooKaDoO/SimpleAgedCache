## The exercise

The exercise - get the tests to pass!

- Explore using an inner class `ExpirableEntry`
- Try not using built in collection classes; Lists, Maps, or Sets.

```python
import time

class SimpleAgedCache:
    def __init__(self, clock=None):
        self.clock = clock

    def put(self, key, value, retention_in_millis):
        pass

    def is_empty(self):
        return False

    def size(self):
        return 0

    def get(self, key):
        return None

```

## Installation

1. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

2. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

3. Install the required packages using `requirements.txt`:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the tests:
   
   ```sh
   pytest
   ```
