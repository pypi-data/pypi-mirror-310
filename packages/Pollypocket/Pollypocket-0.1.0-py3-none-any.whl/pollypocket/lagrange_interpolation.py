import sympy as sp

# Simplifies the expression using sympy
def simplify_expression_sp(expression):

    # Replaces operations and characters to be compatible with sympy format
    expression = expression.replace("(", " ( ").replace(")", " ) ")

    # Evaluates the symbolic expression
    symbolic_expression = sp.sympify(expression)

    # Simplifies the expression
    simplified_expression = sp.simplify(symbolic_expression)

    return str(simplified_expression)

# Lagrange Basis Polynomial
def lagrange_basis_polynomial(points, x, i):
    result = "1"
    for j in range(len(points)):
        if j != i:
            term = f"({x}-{points[j][0]})/({points[i][0]}-{points[j][0]})"
            result = f"({result})*({term})"
    return result

# Lagrange Interpolation Polynomial
def lagrange_polynomial(points):

    # Defines x as a string
    x = "x"

    n = len(points)
    interpolation_result = "0"

    for i in range(n):

        # Calculates Li(x) as a string
        li_x = lagrange_basis_polynomial(points, x, i)

        # Multiplies L_i(x),  y_i times
        term = f"({points[i][1]}) * ({li_x})"

        # Add the term to the polynomial
        if interpolation_result == "0":
            interpolation_result = term
        else:
            interpolation_result = f"({interpolation_result}) + ({term})"

    interpolation_result = interpolation_result.replace("--", "+")
    interpolation_result = simplify_expression_sp(interpolation_result)

    return interpolation_result

# Evaluates the value in the polynomial expression
def evaluate_polynomial(expression, x_value):

    # Replaces x with the value
    expression_with_value = expression.replace("x", "(x)").replace("x", str(x_value))

    try:
        result = eval(expression_with_value)
        return result

    except Exception as e:
        print("Error:", e)
        return None
