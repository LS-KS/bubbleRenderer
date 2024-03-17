# Renderer for bubble charts

This repository was created because of my frustration over missing color gradients in matplotlib. 

## Installation
This is not a package. 
The whole functionality is in the file `bubbleRenderer.py`.

## Dependency
This package depends on the following packages beside python standard library:

- circlify for packing algorithm
- drawSvg for creating svg file
- PySide6 to rendering svg file to png

## Usage

### import

```python
from bubbleRenderer import BubbleRenderer
```

### Create an instance

```python
br = BubbleRenderer()
```
### Add settings

All arguments are passed as keyword arguments.

- size: tuple (width, height) in pixels
- data: list
- labels: list
- cmap: list of two colors in hex format used for color gradient
- gradient_stops: list of four floats between 0 and 100
- packing: 'circle' or 'planets'
- background_color: color in hex format or 'transparent'
- file: str, file name for png file
- png: bool, create png file
- text_size: int, font size of labels
- text_color: color in hex format or svg color name
- text_anchor: 'start', 'middle', 'end'
- stroke: bool, draw stroke around a bubble
- stroke_color: color in hex format or svg color name
- stroke_width: int, width of stroke

### render the chart

The render method returns a svg file which can be handled in any ways, for example
saving as svg file.
If the png argument is set to True, the method also renders the svg data to png file with given filename.

```python
img = br.render()
```


