# My LaTeX Lib

A simple Python library to generate LaTeX code for tables and images.

## Installation

```shell
pip install my_latex_lib
```

## Usage

```python
from my_latex_lib.latex_generator import generate_table, include_image

# Generate LaTeX code for a table
data = [
    # Your table data here
]
table_code = generate_table(data)

# Generate LaTeX code for an image
image_code = include_image('path/to/image.png', caption='An image', label='fig:image')
```
