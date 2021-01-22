# Geodesic Taxicab Path in The Generalisations of The Sierpinski Carpet
A Python 3 implementation of the algorithm described in the paper of the same title by Ethan Berkove, Elene Karangozishvili, and Derek Smith.

## Usage

### Install

```python
pip3 install fractalpaths
```
You will also need the fraction package so you can construct the start and end points, which are the inputs of the shortest path function.

```python
pip3 install fractions
```

### Import classes

```python
from fractalpaths import Fractal
from fractions import Fraction
```

### Functions

First, initiate a fractal:

```python
f = Fractal(dimension, tunnel_number, gap_size, precision)
```

 It takes 4 inputs, one of them being optional:

- `dimension = ` positive integer that specifies the dimension of the fractal.
- `tunnel_number = ` positive integer between 1 and `dimension` that spacifies the amount of solid in the fractal.
- `gap_size = ` positive odd number that spacifies the size of the gaps in the fractal.
- `precision = ` (optional) positive integer that specifies how precise the fractal is. If not specified, this variable is set to be 10.

The function `find_shortest_taxicab_path` is part of the `Fractal` class. It can be called only if `tunnel_number` is greater than 1. Otherwise the fractal is totally disconnected and there is no path to be found.

```python
f.find_shortest_taxicab_path(start_point, end_point)
```
 This function takes two inputs:

- `start_point = ` a list of numbers of type Fraction. The size of the list must be the `dimension` of the fractal. This point must be in the fractal.
- `end_point = ` a list of numbers of type Fraction. The size of the list must be the `dimension` of the fractal. This point must be in the fractal.

In the current version, each coordinate of `start_point` must be less than or equal to the corresponding coordinate of `end_point` (`start_point[i] <= end_point[i]`). There will not be this restriction in the next version.

The output of this function is the shortest path from `start_point` to `end_point` that stays in the fractal:

- `path =` a list of points. Each point is distinct only in one coordinate from the previous point. The points are lists of fractions.

 The length of the shortest taxicab path is stored inside the class Fractal and can be accessed  with `f.shortest_taxicab_path_length`. This value is `None` before calling `find_shortest_taxicab_path`, and becomes the correct value after calling it.

### Example
Suppose our fractal is 9 dimentional, with tunnel number 4, and the gap size 3. Let's keep the default value of the precision. Then we initialise the fractal: 

```python
fractal = Fractal(9, 4, 3)
```

Let's pick the start point and the end point to be:

```python
start_point = [Fraction(0,1), Fraction(1,3), Fraction(1,3), Fraction(29,81), Fraction(31,81), Fraction(148,243), Fraction(67,81), Fraction(33,162), Fraction(193,243)]

end_point = [Fraction(1,1), Fraction(2,3), Fraction(1,3), Fraction(33,81), Fraction(32,81), Fraction(148,243), Fraction(68,81), Fraction(33,162), Fraction(194,243)]
```

To find the shortest taxicab path between these points, we call the function:

```python
 path = fractal.find_shortest_taxicab_path(start_point, end_point)
 ```

 The output is the list of points, where each point is the list of `dimension` number of fractions. Note that if you print path: `print(path)`, the output will be list of objects that look like this: `Fraction(67, 81)`. It means that the value is `67/81`.

 In our example, the path is:

```python
[[0,  1/3,  1/3,  29/81,  31/81,  148/243,  67/81,  11/54,  193/243], 
[0,  1/3,  1/3,  29/81,  31/81,  148/243,  67/81,  11/54,  64/81], 
[0,  1/3,  1/3,  29/81,  31/81,  148/243,  67/81,  11/54,  7/9],   
[0,  1/3,  1/3,  29/81,  11/27,  148/243,  67/81,  11/54,  7/9],   
[0,  1/3,  1/3,  1/3,  11/27,  148/243,  67/81,  11/54,  7/9],   
[0,  1/3,  1/3,  1/3,  11/27,  148/243,  67/81,  11/54,  7/9],   
[0,  1/3,  1/3,  1/3,  11/27,  148/243,  67/81,  11/54,  7/9],   
[0,  1/3,  1/3,  1/3,  11/27,  148/243,  67/81,  11/54,  7/9],   
[1,  1/3,  1/3,  1/3,  11/27,  148/243,  67/81,  11/54,  7/9],   
[1,  2/3,  1/3,  1/3,  11/27,  148/243,  67/81,  11/54,  7/9],   
[1,  2/3,  1/3,  1/3,  11/27,  148/243,  68/81,  11/54,  7/9],   
[1,  2/3,  1/3,  1/3,  11/27,  148/243,  68/81,  11/54,  7/9],   
[1,  2/3,  1/3,  11/27,  11/27,  148/243,  68/81,  11/54,  7/9],   
[1,  2/3,  1/3,  11/27,  11/27,  148/243,  68/81,  11/54,  7/9],     
[1,  2/3,  1/3,  11/27,  32/81,  148/243,  68/81,  11/54,  7/9],   
[1,  2/3,  1/3,  11/27,  32/81,  148/243,  68/81,  11/54,  64/81],   
[1,  2/3,  1/3,  11/27,  32/81,  148/243,  68/81,  11/54,  194/243]] 
```

Notice that at each step only one coordinate is changing. That is why the path is txicab. This path is iside the fractal.
