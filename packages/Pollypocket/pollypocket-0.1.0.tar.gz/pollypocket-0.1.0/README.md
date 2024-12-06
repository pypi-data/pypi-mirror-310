# Pollypocket
## Description
Pollypocket is a Python library for calculate and solve lagrange interpolation polynomials.

## Dependencies
- [Sympy](https://www.sympy.org/en/index.html): A Python library for symbolic mathematics.

## Installation and Usage
Install the library using the terminal:
```bash
pip install pollypocket
```

Then, import it in your python project:
```python
import pollypocket as pyp
```

#### Lagrange Polynomial Interpolation
Parameters
- `points`: A list of tuples, where each tuple contains a point in the form $(x_i, y_i).
```python
>>> import pollypocket as pyp
>>> points = [[1, 3], [2, 1], [3, 5]]
>>> lagrange_polynomial = pyp.lagrange_polynomial(points)
>>> print(lagrange_polynomial)
3*x**2 - 11*x + 11
```

#### Evaluate Polynomial
Parameters
- `expression`: The polynomial expression in string format. This is created using the lagrange_interpolation function.
- `x`: The value at which the polynomial is to be evaluated.
```python
>>> import pollypocket as pyp
>>> points = [[1, 3], [2, 1], [3, 5]]
>>> lagrange_polynomial = pyp.lagrange_polynomial(points)
>>> value = pyp.evaluate_polynomial(lagrange_polynomial, 2)
>>> print(value)
1.0
```

## How to contribute
Feel free to contribute to this project by forking the repository and creating a pull request. You can also create an issue if you find any bugs or want to suggest a new feature 😄.
