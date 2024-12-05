import math
import cmath
from itertools import product
import random
import pickle
import gzip

# 1. array
def array(data, dtype=None):
    if dtype:
        return [dtype(item) for item in data]
    return list(data)

# 2. asarray
def asarray(data, dtype=None):
    if isinstance(data, (list, tuple)):
        if dtype:
            return [dtype(item) for item in data]
        return list(data)
    raise ValueError("Input must be a list or tuple")

# 3. zeros
def zeros(shape, dtype=float):
    if isinstance(shape, int):
        return [dtype(0) for _ in range(shape)]
    elif isinstance(shape, tuple):
        if len(shape) == 1:
            return [dtype(0) for _ in range(shape[0])]
        return [zeros(shape[1:], dtype) for _ in range(shape[0])]
    else:
        raise ValueError("Shape must be an int or tuple of ints")

# 4. ones
def ones(shape, dtype=float):
    if isinstance(shape, int):
        return [dtype(1) for _ in range(shape)]
    elif isinstance(shape, tuple):
        if len(shape) == 1:
            return [dtype(1) for _ in range(shape[0])]
        return [ones(shape[1:], dtype) for _ in range(shape[0])]
    else:
        raise ValueError("Shape must be an int or tuple of ints")

# 5. empty
def empty(shape, dtype=float):
    if isinstance(shape, int):
        return [None for _ in range(shape)]
    elif isinstance(shape, tuple):
        if len(shape) == 1:
            return [None for _ in range(shape[0])]
        return [empty(shape[1:], dtype) for _ in range(shape[0])]
    else:
        raise ValueError("Shape must be an int or tuple of ints")

# 6. full
def full(shape, fill_value, dtype=None):
    if dtype:
        fill_value = dtype(fill_value)
    if isinstance(shape, int):
        return [fill_value for _ in range(shape)]
    elif isinstance(shape, tuple):
        if len(shape) == 1:
            return [fill_value for _ in range(shape[0])]
        return [full(shape[1:], fill_value, dtype) for _ in range(shape[0])]
    else:
        raise ValueError("Shape must be an int or tuple of ints")

# 7. arange
def arange(start, stop=None, step=1, dtype=None):
    if stop is None:
        start, stop = 0, start
    result = []
    value = start
    while value < stop:
        result.append(value)
        value += step
    if dtype:
        result = [dtype(item) for item in result]
    return result

# 8. linspace
def linspace(start, stop, num=50, endpoint=True, dtype=None):
    step = (stop - start) / (num - 1 if endpoint else num)
    result = [start + step * i for i in range(num)]
    if dtype:
        result = [dtype(item) for item in result]
    return result

# 9. logspace
def logspace(start, stop, num=50, endpoint=True, base=10, dtype=None):
    lin = linspace(start, stop, num, endpoint)
    result = [base ** x for x in lin]
    if dtype:
        result = [dtype(item) for item in result]
    return result

# 10. meshgrid
def meshgrid(*arrays):
    grids = []
    for array in arrays:
        grids.append(array)
    return [list(map(list, zip(*p))) for p in product(*grids)]

# 11. eye
def eye(N, M=None, k=0, dtype=float):
    M = M if M is not None else N
    result = [[dtype(0) for _ in range(M)] for _ in range(N)]
    for i in range(N):
        j = i + k
        if 0 <= j < M:
            result[i][j] = dtype(1)
    return result

# 12. identity
def identity(n, dtype=float):
    return eye(n, n, dtype=dtype)

# 13. diag
def diag(array, k=0):
    if isinstance(array[0], list):  # 2D array
        return [array[i][i + k] for i in range(len(array)) if 0 <= i + k < len(array[i])]
    else:  # 1D array
        n = len(array)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i + k] = array[i]
        return result

# 14. frombuffer
def frombuffer(buffer, dtype=float, count=-1, offset=0):
    buffer = buffer[offset:]
    if count == -1:
        count = len(buffer)
    return [dtype(buffer[i]) for i in range(count)]

# 15. fromfile
def fromfile(filename, dtype=float):
    with open(filename, 'r') as file:
        data = file.read().split()
    return [dtype(item) for item in data]

# 16. fromfunction
def fromfunction(function, shape, dtype=float):
    return [[dtype(function(i, j)) for j in range(shape[1])] for i in range(shape[0])]

# 17. fromiter
def fromiter(iterable, dtype=float, count=-1):
    result = []
    for index, item in enumerate(iterable):
        if count != -1 and index >= count:
            break
        result.append(dtype(item))
    return result

# 18. fromstring
def fromstring(string, dtype=float, sep=' '):
    return [dtype(item) for item in string.split(sep)]

# 19. copy
def copy(array):
    return [item[:] if isinstance(item, list) else item for item in array]

# 20. reshape
def reshape(array, new_shape):
    flat = [item for sublist in array for item in sublist] if isinstance(array[0], list) else array[:]
    if len(flat) != new_shape[0] * new_shape[1]:
        raise ValueError("Total size of new array must be unchanged")
    return [[flat.pop(0) for _ in range(new_shape[1])] for _ in range(new_shape[0])]

# 21. ravel
def ravel(array):
    return [item for sublist in array for item in sublist] if isinstance(array[0], list) else array[:]

# 22. flatten
def flatten(array):
    return ravel(array)

# 23. transpose
def transpose(array):
    return [[array[j][i] for j in range(len(array))] for i in range(len(array[0]))]

# 24. swapaxes
def swapaxes(array, axis1, axis2):
    if axis1 != 0 or axis2 != 1:
        raise NotImplementedError("Only 2D arrays with axis1=0 and axis2=1 are supported")
    return transpose(array)

# 25. moveaxis
def moveaxis(array, source, destination):
    raise NotImplementedError("moveaxis is complex and beyond simple nested lists")

# 26. rollaxis
def rollaxis(array, axis, start=0):
    raise NotImplementedError("rollaxis is complex and beyond simple nested lists")

# 27. expand_dims
def expand_dims(array, axis):
    if axis == 0:
        return [array]
    elif axis == 1:
        return [[item] for item in array]
    else:
        raise ValueError("Axis out of range")

# 28. squeeze
def squeeze(array):
    if isinstance(array, list) and len(array) == 1:
        return array[0]
    if isinstance(array[0], list) and len(array[0]) == 1:
        return [item[0] for item in array]
    return array

# 29. concatenate
def concatenate(arrays, axis=0):
    if axis == 0:
        return [item for array in arrays for item in array]
    elif axis == 1:
        return [item for sublist in zip(*arrays) for item in sublist]
    else:
        raise ValueError("Axis out of range")

# 30. stack
def stack(arrays, axis=0):
    if axis == 0:
        return arrays
    elif axis == 1:
        return [[array[i] for array in arrays] for i in range(len(arrays[0]))]
    else:
        raise ValueError("Axis out of range")

# 31. vstack
def vstack(arrays):
    return concatenate(arrays, axis=0)

# 32. hstack
def hstack(arrays):
    return concatenate(arrays, axis=1)

# 33. dstack
def dstack(arrays):
    raise NotImplementedError("dstack is beyond simple nested lists")

# 34. column_stack
def column_stack(arrays):
    return hstack(arrays)

# 35. row_stack
def row_stack(arrays):
    return vstack(arrays)

# 36. split
def split(array, indices, axis=0):
    if axis == 0:
        return [array[start:end] for start, end in zip(indices[:-1], indices[1:])]
    elif axis == 1:
        return [list(zip(*array))[start:end] for start, end in zip(indices[:-1], indices[1:])]
    else:
        raise ValueError("Axis out of range")

# 37. array_split
def array_split(array, sections, axis=0):
    size = len(array) // sections
    return [array[i * size:(i + 1) * size] for i in range(sections)] + [array[sections * size:]]

# 38. hsplit
def hsplit(array, sections):
    return split(array, sections, axis=1)

# 39. vsplit
def vsplit(array, sections):
    return split(array, sections, axis=0)

# 40. dsplit
def dsplit(array, sections):
    raise NotImplementedError("dsplit is beyond simple nested lists")

# 41. append
def append(array, values, axis=None):
    if axis is None:
        return array + values
    elif axis == 0:
        return array + [values]
    elif axis == 1:
        return [row + [val] for row, val in zip(array, values)]
    else:
        raise ValueError("Axis out of range")

# 42. insert
def insert(array, index, values, axis=None):
    if axis is None:
        return array[:index] + [values] + array[index:]
    elif axis == 0:
        return array[:index] + [values] + array[index:]
    elif axis == 1:
        return [row[:index] + [values] + row[index:] for row in array]
    else:
        raise ValueError("Axis out of range")

# 43. delete
def delete(array, index, axis=None):
    if axis is None:
        return array[:index] + array[index + 1:]
    elif axis == 0:
        return array[:index] + array[index + 1:]
    elif axis == 1:
        return [row[:index] + row[index + 1:] for row in array]
    else:
        raise ValueError("Axis out of range")

# 44. unique
def unique(array):
    return list(set(array))

# 45. tile
def tile(array, reps):
    return array * reps if isinstance(reps, int) else [array * reps[1] for _ in range(reps[0])]

# 46. repeat
def repeat(array, repeats, axis=None):
    if axis is None:
        return [item for item in array for _ in range(repeats)]
    elif axis == 0:
        return [row for row in array for _ in range(repeats)]
    elif axis == 1:
        return [[item for item in row for _ in range(repeats)] for row in array]
    else:
        raise ValueError("Axis out of range")

# 47. add
def add(a, b):
    return a + b

# 48. subtract
def subtract(a, b):
    return a - b

# 49. multiply
def multiply(a, b):
    return a * b

# 50. divide
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

# 51. floor_divide
def floor_divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a // b

# 52. mod
def mod(a, b):
    return a % b

# 53. remainder
def remainder(a, b):
    return a % b

# 54. power
def power(a, b):
    return a ** b

# 55. sqrt
def sqrt(a):
    if a < 0:
        raise ValueError("math domain error")
    return math.sqrt(a)

# 56. square
def square(a):
    return a * a

# 57. absolute
def absolute(a):
    return abs(a)

# 58. fabs
def fabs(a):
    return math.fabs(a)

# 59. sign
def sign(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0

# 60. exp
def exp(a):
    return math.exp(a)

# 61. expm1
def expm1(a):
    return math.expm1(a)

# 62. log
def log(a, base=math.e):
    if a <= 0:
        raise ValueError("math domain error")
    return math.log(a, base)

# 63. log10
def log10(a):
    if a <= 0:
        raise ValueError("math domain error")
    return math.log10(a)

# 64. log2
def log2(a):
    if a <= 0:
        raise ValueError("math domain error")
    return math.log2(a)

# 65. log1p
def log1p(a):
    if a <= -1:
        raise ValueError("math domain error")
    return math.log1p(a)

# 66. sin
def sin(a):
    return math.sin(a)

# 67. cos
def cos(a):
    return math.cos(a)

# 68. tan
def tan(a):
    return math.tan(a)

# 69. arcsin
def arcsin(a):
    if a < -1 or a > 1:
        raise ValueError("math domain error")
    return math.asin(a)

# 70. arccos
def arccos(a):
    if a < -1 or a > 1:
        raise ValueError("math domain error")
    return math.acos(a)

# 71. arctan
def arctan(a):
    return math.atan(a)

# 72. arctan2
def arctan2(y, x):
    return math.atan2(y, x)

# 73. hypot
def hypot(x, y):
    return math.hypot(x, y)

# 74. sinh
def sinh(a):
    return math.sinh(a)

# 75. cosh
def cosh(a):
    return math.cosh(a)

# 76. tanh
def tanh(a):
    return math.tanh(a)

# 77. arcsinh
def arcsinh(a):
    return math.asinh(a)

# 78. arccosh
def arccosh(a):
    if a < 1:
        raise ValueError("math domain error")
    return math.acosh(a)

# 79. arctanh
def arctanh(a):
    if a <= -1 or a >= 1:
        raise ValueError("math domain error")
    return math.atanh(a)

# 80. deg2rad
def deg2rad(degrees):
    return math.radians(degrees)

# 81. rad2deg
def rad2deg(radians):
    return math.degrees(radians)

# 82. pi
def pi():
    return math.pi

# 83. sum
def sum(array):
    total = 0
    for item in array:
        total += item
    return total

# 84. prod
def prod(array):
    result = 1
    for item in array:
        result *= item
    return result

# 85. mean
def mean(array):
    return sum(array) / len(array)

# 86. std (standard deviation)
def std(array):
    mean_value = mean(array)
    return (sum((x - mean_value) ** 2 for x in array) / len(array)) ** 0.5

# 87. var (variance)
def var(array):
    mean_value = mean(array)
    return sum((x - mean_value) ** 2 for x in array) / len(array)

# 88. min
def min(array):
    minimum = array[0]
    for item in array:
        if item < minimum:
            minimum = item
    return minimum

# 89. max
def max(array):
    maximum = array[0]
    for item in array:
        if item > maximum:
            maximum = item
    return maximum

# 90. argmin
def argmin(array):
    minimum = array[0]
    index = 0
    for i, item in enumerate(array):
        if item < minimum:
            minimum = item
            index = i
    return index

# 91. argmax
def argmax(array):
    maximum = array[0]
    index = 0
    for i, item in enumerate(array):
        if item > maximum:
            maximum = item
            index = i
    return index

# 92. median
def median(array):
    sorted_array = sorted(array)
    n = len(sorted_array)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_array[mid - 1] + sorted_array[mid]) / 2
    else:
        return sorted_array[mid]

# 93. percentile
def percentile(array, p):
    sorted_array = sorted(array)
    index = (len(sorted_array) - 1) * (p / 100)
    lower = int(index)
    upper = lower + 1
    if upper >= len(sorted_array):
        return sorted_array[lower]
    weight = index - lower
    return sorted_array[lower] * (1 - weight) + sorted_array[upper] * weight

# 94. quantile
def quantile(array, q):
    return percentile(array, q * 100)

# 95. average
def average(array, weights=None):
    if weights is None:
        return mean(array)
    total_weight = sum(weights)
    return sum(x * w for x, w in zip(array, weights)) / total_weight

# 96. cumsum (cumulative sum)
def cumsum(array):
    result = []
    total = 0
    for item in array:
        total += item
        result.append(total)
    return result

# 97. cumprod (cumulative product)
def cumprod(array):
    result = []
    total = 1
    for item in array:
        total *= item
        result.append(total)
    return result

# 98. ptp (peak-to-peak, range)
def ptp(array):
    return max(array) - min(array)

# 99. dot (dot product for vectors or matrix multiplication)
def dot(a, b):
    if isinstance(a[0], list):  # Matrix multiplication
        return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]
    else:  # Vector dot product
        return sum(x * y for x, y in zip(a, b))

# 100. vdot (vector dot product)
def vdot(a, b):
    return sum(x * y for x, y in zip(a, b))

# 101. inner (inner product for vectors or sum of element-wise multiplication for arrays)
def inner(a, b):
    if isinstance(a[0], list):  # Matrix inner product
        return sum(dot(a_row, b_row) for a_row, b_row in zip(a, b))
    else:  # Vector inner product
        return sum(x * y for x, y in zip(a, b))

# 102. outer (outer product of two vectors)
def outer(a, b):
    return [[x * y for y in b] for x in a]

# 103. matmul (matrix multiplication, alias for dot)
def matmul(a, b):
    return dot(a, b)

# 104. tensordot (generalized dot product along specified axes)
def tensordot(a, b, axes=2):
    raise NotImplementedError("Tensordot is highly complex and beyond simple lists")

# 105. einsum (Einstein summation)
def einsum(equation, *operands):
    raise NotImplementedError("Einsum requires symbolic manipulation and is very complex")

# 106. linalg.det (determinant of a square matrix)
def determinant(matrix):
    # Base case for 2x2 matrix
    if len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    # Recursive case for larger matrices
    det = 0
    for c in range(len(matrix)):
        det += ((-1) ** c) * matrix[0][c] * determinant(minor(matrix, 0, c))
    return det

def minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

# 107. linalg.eig (eigenvalues and eigenvectors)
def eig(matrix):
    raise NotImplementedError("Eigenvalue decomposition requires advanced algorithms")

# 108. linalg.eigh (eigenvalues for Hermitian matrices)
def eigh(matrix):
    raise NotImplementedError("Eigh requires specialized linear algebra libraries")

# 109. linalg.eigvals (only eigenvalues of a matrix)
def eigvals(matrix):
    raise NotImplementedError("Eigenvalue computation requires advanced algorithms")

# 110. linalg.inv (inverse of a square matrix)
def inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is singular and cannot be inverted")
    size = len(matrix)
    cofactors = [[((-1) ** (i + j)) * determinant(minor(matrix, i, j)) for j in range(size)] for i in range(size)]
    adjugate = transpose(cofactors)
    return [[adjugate[i][j] / det for j in range(size)] for i in range(size)]

# 111. linalg.norm (matrix or vector norm)
def norm(matrix, ord=2):
    if isinstance(matrix[0], list):  # Matrix norm
        return max(sum(abs(x) ** ord for x in row) ** (1/ord) for row in matrix)
    else:  # Vector norm
        return sum(abs(x) ** ord for x in matrix) ** (1/ord)

# 112. linalg.qr (QR decomposition)
def qr(matrix):
    raise NotImplementedError("QR decomposition requires advanced linear algebra algorithms")

# 113. linalg.svd (singular value decomposition)
def svd(matrix):
    raise NotImplementedError("SVD requires advanced algorithms")

# 114. linalg.solve (solving linear systems)
def solve(a, b):
    inv_a = inverse(a)
    return matmul(inv_a, b)

# 115. linalg.lstsq (least squares solution)
def lstsq(a, b):
    raise NotImplementedError("Least squares requires advanced optimization algorithms")

# 116. linalg.cholesky (Cholesky decomposition)
def cholesky(matrix):
    raise NotImplementedError("Cholesky decomposition requires specialized algorithms")

# 117. linalg.matrix_rank (rank of a matrix)
def matrix_rank(matrix):
    raise NotImplementedError("Matrix rank requires row-reduction algorithms")

# 118. linalg.pinv (pseudoinverse of a matrix)
def pinv(matrix):
    raise NotImplementedError("Pseudoinverse requires SVD computation")

# 119. linalg.tensorinv (inverse of a tensor)
def tensorinv(matrix):
    raise NotImplementedError("Tensor inverse requires advanced symbolic algorithms")

# 120. linalg.tensorsolve (solve a tensor equation)
def tensorsolve(matrix, rhs):
    raise NotImplementedError("Tensor solve requires advanced symbolic algorithms")

# 121. random.rand (uniform random numbers in [0, 1))
def rand(*shape):
    size = math.prod(shape) if shape else 1
    result = [random.random() for _ in range(size)]
    if shape:
        return reshape(result, shape)
    return result[0]

# 122. random.randn (standard normal distribution)
def randn(*shape):
    size = math.prod(shape) if shape else 1
    result = [random.gauss(0, 1) for _ in range(size)]
    if shape:
        return reshape(result, shape)
    return result[0]

# 123. random.randint (random integers in [low, high))
def randint(low, high=None, size=1):
    if high is None:
        high = low
        low = 0
    return [random.randint(low, high - 1) for _ in range(size)] if size > 1 else random.randint(low, high - 1)

# 124. random.choice (random element from a sequence)
def choice(seq, size=None):
    if size is None:
        return random.choice(seq)
    return [random.choice(seq) for _ in range(size)]

# 125. random.shuffle (shuffle a sequence in place)
def shuffle(seq):
    random.shuffle(seq)
    return seq

# 126. random.permutation (permuted sequence or array)
def permutation(seq):
    return random.sample(seq, len(seq))

# 127. random.beta (Beta distribution)
def beta(a, b, size=1):
    return [random.betavariate(a, b) for _ in range(size)]

# 128. random.binomial (Binomial distribution)
def binomial(n, p, size=1):
    return [sum(1 if random.random() < p else 0 for _ in range(n)) for _ in range(size)]

# 129. random.chisquare (Chi-squared distribution)
def chisquare(df, size=1):
    return [sum(random.gauss(0, 1) ** 2 for _ in range(df)) for _ in range(size)]

# 130. random.exponential (Exponential distribution)
def exponential(scale=1, size=1):
    return [-scale * math.log(1 - random.random()) for _ in range(size)]

# 131. random.f (F-distribution)
def f(dfn, dfd, size=1):
    return [(chisquare(dfn)[0] / dfn) / (chisquare(dfd)[0] / dfd) for _ in range(size)]

# 132. random.gamma (Gamma distribution)
def gamma(shape, scale=1, size=1):
    return [random.gammavariate(shape, scale) for _ in range(size)]

# 133. random.geometric (Geometric distribution)
def geometric(p, size=1):
    return [math.ceil(math.log(1 - random.random()) / math.log(1 - p)) for _ in range(size)]

# 134. random.gumbel (Gumbel distribution)
def gumbel(loc=0, scale=1, size=1):
    return [loc - scale * math.log(-math.log(random.random())) for _ in range(size)]

# 135. random.hypergeometric (Hypergeometric distribution)
def hypergeometric(ngood, nbad, nsample, size=1):
    return [sum(1 if random.random() < (ngood - i) / (ngood + nbad - i) else 0 for i in range(nsample)) for _ in range(size)]

# 136. random.laplace (Laplace distribution)
def laplace(loc=0, scale=1, size=1):
    return [loc + scale * (math.log(1 - random.random()) if random.random() < 0.5 else -math.log(random.random())) for _ in range(size)]

# 137. random.logistic (Logistic distribution)
def logistic(loc=0, scale=1, size=1):
    return [loc + scale * math.log(random.random() / (1 - random.random())) for _ in range(size)]

# 138. random.lognormal (Log-normal distribution)
def lognormal(mean=0, sigma=1, size=1):
    return [math.exp(random.gauss(mean, sigma)) for _ in range(size)]

# 139. random.multinomial (Multinomial distribution)
def multinomial(n, pvals, size=1):
    return [[sum(1 if random.random() < sum(pvals[:k+1]) else 0 for _ in range(n)) for k in range(len(pvals))] for _ in range(size)]

# 140. random.multivariate_normal (Multivariate normal distribution)
def multivariate_normal(mean, cov, size=1):
    raise NotImplementedError("Multivariate normal requires matrix decomposition.")

# 141. random.negative_binomial (Negative Binomial distribution)
def negative_binomial(n, p, size=1):
    return [sum(geometric(p, n)) for _ in range(size)]

# 142. random.noncentral_chisquare (Non-central chi-squared distribution)
def noncentral_chisquare(df, nonc, size=1):
    raise NotImplementedError("Non-central chi-squared is complex.")

# 143. random.normal (Normal distribution)
def normal(mean=0, std=1, size=1):
    return [random.gauss(mean, std) for _ in range(size)]

# 144. random.pareto (Pareto distribution)
def pareto(alpha, size=1):
    return [(1 - random.random()) ** (-1 / alpha) for _ in range(size)]

# 145. random.poisson (Poisson distribution)
def poisson(lam, size=1):
    return [sum(1 if random.random() < lam / k else 0 for k in range(1, int(10 * lam))) for _ in range(size)]

# 146. random.power (Power distribution)
def power(a, size=1):
    return [(1 - random.random()) ** (1 / a) for _ in range(size)]

# 147. random.rayleigh (Rayleigh distribution)
def rayleigh(scale=1, size=1):
    return [scale * math.sqrt(-2 * math.log(1 - random.random())) for _ in range(size)]

# 148. random.standard_cauchy (Standard Cauchy distribution)
def standard_cauchy(size=1):
    return [math.tan(math.pi * (random.random() - 0.5)) for _ in range(size)]

# 149. random.standard_exponential (Standard Exponential)
def standard_exponential(size=1):
    return exponential(1, size)

# 150. random.standard_normal (Standard Normal)
def standard_normal(size=1):
    return randn(size)

# 151. random.standard_t (Student's t-distribution)
def standard_t(df, size=1):
    return [random.gauss(0, 1) / math.sqrt(chisquare(df)[0] / df) for _ in range(size)]

# 152. random.triangular (Triangular distribution)
def triangular(left, mode, right, size=1):
    return [random.triangular(left, mode, right) for _ in range(size)]

# 153. random.uniform (Uniform distribution)
def uniform(low=0, high=1, size=1):
    return [random.uniform(low, high) for _ in range(size)]

# 154. random.vonmises (Von Mises distribution)
def vonmises(mu, kappa, size=1):
    return [random.vonmisesvariate(mu, kappa) for _ in range(size)]

# 155. random.wald (Wald distribution)
def wald(mean, scale, size=1):
    raise NotImplementedError("Wald distribution requires advanced sampling techniques.")

# 156. random.weibull (Weibull distribution)
def weibull(alpha, size=1):
    return [(1 - random.random()) ** (1 / alpha) for _ in range(size)]

# 157. random.zipf (Zipf distribution)
def zipf(alpha, size=1):
    return [int(random.paretovariate(alpha) - 1) for _ in range(size)]

# 158. random.seed (Set seed)
def seed(value):
    random.seed(value)

# 159. random.get_state (Get random state)
def get_state():
    return random.getstate()

# 160. random.set_state (Set random state)
def set_state(state):
    random.setstate(state)

# 161. bitwise_and
def bitwise_and(a, b):
    return a & b

# 162. bitwise_or
def bitwise_or(a, b):
    return a | b

# 163. bitwise_xor
def bitwise_xor(a, b):
    return a ^ b

# 164. invert
def invert(a):
    return ~a

# 165. left_shift
def left_shift(a, shift):
    return a << shift

# 166. right_shift
def right_shift(a, shift):
    return a >> shift

# 167. logical_and
def logical_and(a, b):
    return a and b

# 168. logical_or
def logical_or(a, b):
    return a or b

# 169. logical_xor
def logical_xor(a, b):
    return bool(a) ^ bool(b)

# 170. logical_not
def logical_not(a):
    return not a

# 171. greater
def greater(a, b):
    return a > b

# 172. greater_equal
def greater_equal(a, b):
    return a >= b

# 173. less
def less(a, b):
    return a < b

# 174. less_equal
def less_equal(a, b):
    return a <= b

# 175. equal
def equal(a, b):
    return a == b

# 176. not_equal
def not_equal(a, b):
    return a != b

# 177. all (check if all elements in a list are True)
def all(iterable):
    for item in iterable:
        if not item:
            return False
    return True

# 178. any (check if any element in a list is True)
def any(iterable):
    for item in iterable:
        if item:
            return True
    return False

# 179. isnan (check if a number is NaN)
def isnan(value):
    return value != value

# 180. isinf (check if a number is infinite)
def isinf(value):
    return value == float('inf') or value == -float('inf')

# 181. isfinite (check if a number is finite)
def isfinite(value):
    return not isnan(value) and not isinf(value)

# Helper function: DFT
def dft(input_array):
    n = len(input_array)
    result = []
    for k in range(n):
        sum_val = 0
        for t in range(n):
            angle = -2j * math.pi * t * k / n
            sum_val += input_array[t] * cmath.exp(angle)
        result.append(sum_val)
    return result

# Helper function: IDFT
def idft(input_array):
    n = len(input_array)
    result = []
    for t in range(n):
        sum_val = 0
        for k in range(n):
            angle = 2j * math.pi * t * k / n
            sum_val += input_array[k] * cmath.exp(angle)
        result.append(sum_val / n)
    return result

# 182. fft.fft (1D Fourier Transform)
def fft(input_array):
    return dft(input_array)

# 183. fft.ifft (1D Inverse Fourier Transform)
def ifft(input_array):
    return idft(input_array)

# 184. fft.fft2 (2D Fourier Transform)
def fft2(input_matrix):
    intermediate = [fft(row) for row in input_matrix]  # FFT on rows
    return [fft(col) for col in zip(*intermediate)]  # FFT on columns

# 185. fft.ifft2 (2D Inverse Fourier Transform)
def ifft2(input_matrix):
    intermediate = [ifft(row) for row in input_matrix]  # IFFT on rows
    return [ifft(col) for col in zip(*intermediate)]  # IFFT on columns

# 186. fft.fftn (N-dimensional Fourier Transform)
def fftn(input_array):
    if isinstance(input_array[0], list):  # Handle multi-dimensional input
        return [fftn(subarray) for subarray in input_array]
    return fft(input_array)

# 187. fft.ifftn (N-dimensional Inverse Fourier Transform)
def ifftn(input_array):
    if isinstance(input_array[0], list):  # Handle multi-dimensional input
        return [ifftn(subarray) for subarray in input_array]
    return ifft(input_array)

# 194. fft.fftshift (Shift zero-frequency component to center)
def fftshift(input_array):
    n = len(input_array)
    mid = n // 2
    return input_array[mid:] + input_array[:mid]

# 195. fft.ifftshift (Inverse of fftshift)
def ifftshift(input_array):
    n = len(input_array)
    mid = n // 2
    return input_array[mid:] + input_array[:mid]

# 196. fft.fftfreq (DFT sample frequencies)
def fftfreq(n, d=1.0):
    freq = []
    for k in range(n):
        if k <= n // 2:
            freq.append(k / (n * d))
        else:
            freq.append((k - n) / (n * d))
    return freq

# 197. fft.rfftfreq (DFT sample frequencies for real input)
def rfftfreq(n, d=1.0):
    return [k / (n * d) for k in range(n // 2 + 1)]

# 198. unwrap (unwrap phase angles)
def unwrap(angles):
    unwrapped = [angles[0]]
    for i in range(1, len(angles)):
        delta = angles[i] - unwrapped[-1]
        while delta > math.pi:
            delta -= 2 * math.pi
        while delta < -math.pi:
            delta += 2 * math.pi
        unwrapped.append(unwrapped[-1] + delta)
    return unwrapped

# 199. angle (compute the angle of a complex number or array of complex numbers)
def angle(values, deg=False):
    if isinstance(values, list):
        angles = [cmath.phase(val) for val in values]
    else:
        angles = cmath.phase(values)
    return [math.degrees(a) if deg else a for a in angles] if isinstance(angles, list) else (math.degrees(angles) if deg else angles)

# 200. real (extract real part of complex numbers)
def real(values):
    if isinstance(values, list):
        return [val.real for val in values]
    return values.real

# 201. imag (extract imaginary part of complex numbers)
def imag(values):
    if isinstance(values, list):
        return [val.imag for val in values]
    return values.imag

# 202. unique
def unique(array):
    return list(set(array))

# 203. intersect1d
def intersect1d(array1, array2):
    return list(set(array1) & set(array2))

# 204. setdiff1d
def setdiff1d(array1, array2):
    return list(set(array1) - set(array2))

# 205. union1d
def union1d(array1, array2):
    return list(set(array1) | set(array2))

# 206. setxor1d
def setxor1d(array1, array2):
    return list(set(array1) ^ set(array2))

# 207. in1d (check if elements of one array are in another)
def in1d(array1, array2):
    return [item in array2 for item in array1]

# 208. isin (similar to in1d but supports arrays directly)
def isin(array1, array2):
    return in1d(array1, array2)

# 209. save (save an object to a file)
def save(filename, array):
    with open(filename, 'wb') as file:
        pickle.dump(array, file)

# 210. load (load an object from a file)
def load(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# 211. savez (save multiple arrays to a single file)
def savez(filename, **arrays):
    with open(filename, 'wb') as file:
        pickle.dump(arrays, file)

# 212. savez_compressed (save multiple arrays to a single compressed file)
def savez_compressed(filename, **arrays):
    with gzip.open(filename, 'wb') as file:
        pickle.dump(arrays, file)

# 213. genfromtxt (load data from a text file, handling missing values)
def genfromtxt(filename, delimiter=',', dtype=float, skip_header=0):
    with open(filename, 'r') as file:
        lines = file.readlines()[skip_header:]
        data = [[dtype(value.strip()) if value.strip() else None for value in line.split(delimiter)] for line in lines]
    return data

# 214. loadtxt (load data from a text file)
def loadtxt(filename, delimiter=',', dtype=float, skip_header=0):
    with open(filename, 'r') as file:
        lines = file.readlines()[skip_header:]
        return [[dtype(value.strip()) for value in line.split(delimiter)] for line in lines]

# 215. savetxt (save data to a text file)
def savetxt(filename, array, delimiter=',', fmt="%s"):
    with open(filename, 'w') as file:
        for row in array:
            file.write(delimiter.join(fmt % value for value in row) + '\n')

# 216. meshgrid
def meshgrid(*arrays):
    shape = [len(a) for a in arrays]
    grids = []
    for i, array in enumerate(arrays):
        grid = [array] * math.prod(shape[:i]) + [array] * math.prod(shape[i+1:])
        grids.append(grid)
    return grids

# 217. ogrid
def ogrid(*args):
    grids = []
    for start, stop, step in args:
        grids.append([x for x in range(start, stop, step)])
    return grids

# 218. mgrid
def mgrid(*args):
    grids = []
    for start, stop, step in args:
        grids.append([x * steps])

def ix_(*args):
    result = []
    for arg in args:
        if isinstance(arg, list):
            result.append([[x] for x in arg])
        else:
            raise ValueError("All inputs must be 1-dimensional sequences.")
    return result

def nditer(array):
    for item in (x for sublist in array for x in sublist):
        yield item

def ndenumerate(array):
    for i, row in enumerate(array):
        for j, val in enumerate(row):
            yield (i, j), val

def ndindex(shape):
    return product(*[range(s) for s in shape])

def broadcast(*arrays):
    shape = [max(len(a) for a in arrays) for _ in arrays]
    return [a * (len(shape) // len(a)) for a in arrays]

def broadcast(*arrays):
    shape = [max(len(a) for a in arrays) for _ in arrays]
    return [a * (len(shape) // len(a)) for a in arrays]

def roll(array, shift, axis=None):
    if axis is None:
        flat = sum(array, [])
        n = len(flat)
        shift %= n
        return flat[-shift:] + flat[:-shift]
    else:
        return array[-shift:] + array[:-shift]

def flip(array, axis=None):
    if axis is None:
        return array[::-1]
    else:
        return [row[::-1] if axis == 1 else row for row in array]

def rot90(array, k=1):
    for _ in range(k % 4):
        array = list(zip(*array[::-1]))
    return array

def around(array, decimals=0):
    return [[round(x, decimals) for x in row] for row in array]

def round_(array, decimals=0):
    return around(array, decimals)

def fix(array):
    return [[math.floor(x) if x < 0 else math.ceil(x) for x in row] for row in array]

def clip(array, min_val, max_val):
    return [[min(max(x, min_val), max_val) for x in row] for row in array]

def where(condition, x=None, y=None):
    if x is None or y is None:
        return [(i, j) for i, row in enumerate(condition) for j, val in enumerate(row) if val]
    else:
        return [[x if cond else y for cond in row] for row in condition]

def argwhere(array):
    return [(i, j) for i, row in enumerate(array) for j, val in enumerate(row) if val]

def nonzero(array):
    return [[i for i, val in enumerate(row) if val != 0] for row in array]

def flatnonzero(array):
    return [i for i, val in enumerate(sum(array, [])) if val != 0]

def diag_indices(n):
    return [(i, i) for i in range(n)]

def tril_indices(n, k=0):
    return [(i, j) for i in range(n) for j in range(i + k + 1)]

def triu_indices(n, k=0):
    return [(i, j) for i in range(n) for j in range(i + k, n)]

def indices(dimensions):
    return [list(range(d)) for d in dimensions]

def full_like(array, fill_value):
    return [[fill_value for _ in row] for row in array]

def zeros_like(array):
    return full_like(array, 0)

def ones_like(array):
    return full_like(array, 1)

def empty_like(array):
    return full_like(array, None)

def allclose(array1, array2, rtol=1e-5, atol=1e-8):
    return all(abs(a - b) <= (atol + rtol * abs(b)) for a, b in zip(sum(array1, []), sum(array2, [])))

def isclose(array1, array2, rtol=1e-5, atol=1e-8):
    if len(array1) != len(array2):
        raise ValueError("Arrays must have the same shape.")
    if isinstance(array1[0], list):  # 2D arrays
        return [[abs(a - b) <= (atol + rtol * abs(b)) for a, b in zip(row1, row2)]
                for row1, row2 in zip(array1, array2)]
    else:  # 1D arrays
        return [abs(a - b) <= (atol + rtol * abs(b)) for a, b in zip(array1, array2)]

def array_equal(array1, array2):
    if len(array1) != len(array2):
        return False
    if isinstance(array1[0], list):  # 2D arrays
        return all(all(a == b for a, b in zip(row1, row2)) for row1, row2 in zip(array1, array2))
    else:  # 1D arrays
        return all(a == b for a, b in zip(array1, array2))

def array_equiv(array1, array2):
    def flatten(array):
        return [item for sublist in array for item in sublist] if isinstance(array[0], list) else array

    flat1 = flatten(array1)
    flat2 = flatten(array2)

    if len(flat1) != len(flat2):
        return False
    return all(a == b for a, b in zip(flat1, flat2))

def sparse_array(data, shape, density):
    """
    Creates a sparse array representation.
    Parameters:
    - data: List of non-zero values.
    - shape: Tuple representing the array dimensions.
    - density: Fraction of non-zero values (0 to 1).
    Returns:
    - Dictionary representing sparse array: {index: value}.
    """
    sparse = {}
    num_elements = int(shape[0] * shape[1] * density)
    for _ in range(num_elements):
        i, j = random.randint(0, shape[0] - 1), randint(0, shape[1] - 1)
        sparse[(i, j)] = data[randint(0, len(data) - 1)]
    return sparse

def is_sparse(array):
    """
    Checks if an array is sparse.
    Parameters:
    - array: Dictionary representing a sparse array.
    Returns:
    - Boolean indicating if the array is sparse.
    """
    return isinstance(array, dict)

def sparse_to_dense(array, shape):
    """
    Converts a sparse array to a dense array.
    Parameters:
    - array: Dictionary representing a sparse array.
    - shape: Tuple representing the array dimensions.
    Returns:
    - Dense list of lists.
    """
    dense = [[0 for _ in range(shape[1])] for _ in range(shape[0])]
    for (i, j), val in array.items():
        dense[i][j] = val
    return dense

def dense_to_sparse(array):
    """
    Converts a dense array to a sparse array.
    Parameters:
    - array: List of lists representing a dense array.
    Returns:
    - Dictionary representing a sparse array.
    """
    sparse = {}
    for i, row in enumerate(array):
        for j, val in enumerate(row):
            if val != 0:
                sparse[(i, j)] = val
    return sparse

def resize_dynamic(array, new_shape):
    """
    Dynamically resizes an array, retaining existing data where possible.
    Parameters:
    - array: Original array (list of lists).
    - new_shape: Tuple representing the new dimensions.
    Returns:
    - Resized array.
    """
    flat = [item for row in array for item in row]
    result = [[0 for _ in range(new_shape[1])] for _ in range(new_shape[0])]
    for i in range(new_shape[0]):
        for j in range(new_shape[1]):
            if flat:
                result[i][j] = flat.pop(0)
    return result

def append_dynamic(array, values, axis):
    """
    Appends values to an array along the specified axis.
    Parameters:
    - array: Original array (list of lists).
    - values: Values to append.
    - axis: Axis along which to append (0 or 1).
    Returns:
    - Modified array.
    """
    if axis == 0:
        array.extend(values)
    elif axis == 1:
        for row, val in zip(array, values):
            row.append(val)
    else:
        raise ValueError("Axis must be 0 or 1")
    return array

def trim_dynamic(array, axis, size):
    """
    Trims the array dynamically along a specified axis.
    Parameters:
    - array: Original array (list of lists).
    - axis: Axis to trim (0 or 1).
    - size: Number of elements to keep.
    Returns:
    - Trimmed array.
    """
    if axis == 0:
        return array[:size]
    elif axis == 1:
        return [row[:size] for row in array]
    else:
        raise ValueError("Axis must be 0 or 1")

def data_array(data, labels=None):
    """
    Creates labeled arrays with metadata.
    Parameters:
    - data: List of lists representing the data.
    - labels: Optional list of labels for rows or columns.
    Returns:
    - Dictionary with labels and data.
    """
    if labels:
        return {label: row for label, row in zip(labels, data)}
    return {"data": data}

def hierarchical_array(data, levels):
    """
    Creates arrays with hierarchical indexing.
    Parameters:
    - data: List of lists representing the data.
    - levels: List of labels for each hierarchy level.
    Returns:
    - Nested dictionary representing the hierarchical array.
    """
    result = {}
    for level, rows in zip(levels, data):
        result[level] = rows
    return result

def block_matrix(blocks):
    """
    Constructs a block matrix from smaller arrays.
    Parameters:
    - blocks: List of lists representing blocks.
    Returns:
    - Combined block matrix.
    """
    rows = []
    for row_blocks in blocks:
        combined_rows = [sum(row, []) for row in zip(*row_blocks)]
        rows.extend(combined_rows)
    return rows

def polar_to_cartesian(magnitude, angle):
    """
    Converts polar coordinates to Cartesian coordinates.
    Parameters:
    - magnitude: Radius (r).
    - angle: Angle in radians (theta).
    Returns:
    - Tuple (x, y).
    """
    x = magnitude * math.cos(angle)
    y = magnitude * math.sin(angle)
    return x, y

def cartesian_to_polar(x, y):
    """
    Converts Cartesian coordinates to polar coordinates.
    Parameters:
    - x: X-coordinate.
    - y: Y-coordinate.
    Returns:
    - Tuple (magnitude, angle in radians).
    """
    magnitude = math.sqrt(x**2 + y**2)
    angle = math.atan2(y, x)
    return magnitude, angle

def complex_fft(array):
    """
    Performs FFT optimized for complex arrays.
    Parameters:
    - array: List of complex numbers.
    Returns:
    - FFT result.
    """
    return fft(array)  # Use the previously implemented FFT function

def complex_conjugate(array):
    """
    Returns the complex conjugate of an array.
    Parameters:
    - array: List of complex numbers.
    Returns:
    - List of complex conjugates.
    """
    return [complex(x.real, -x.imag) for x in array]

def symbolic_array(data):
    """
    Converts a numeric array into symbolic form.
    Parameters:
    - data: List of numbers.
    Returns:
    - List of symbolic strings.
    """
    return [f"x{i}" for i, _ in enumerate(data)]

def simplify(array):
    """
    Simplifies symbolic expressions in an array.
    Parameters:
    - array: List of symbolic expressions.
    Returns:
    - Simplified array.
    """
    return array  # Simplification is symbolic; not implemented fully

def add_elementwise(array1, array2):
    return [[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def subtract_elementwise(array1, array2):
    return [[a - b for a, b in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def multiply_elementwise(array1, array2):
    return [[a * b for a, b in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def divide_elementwise(array1, array2):
    return [[a / b for a, b in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def modulus(array1, array2):
    return [[a % b for a, b in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def elementwise_power(array, power):
    return [[a**power for a in row] for row in array]

def root(array, degree):
    return [[a**(1/degree) for a in row] for row in array]

def exponent(array):
    return [[math.exp(a) for a in row] for row in array]

def logarithm_base(array, base):
    return [[math.log(a, base) for a in row] for row in array]

def reciprocal(array):
    return [[1 / a for a in row] for row in array]

def gamma_function(array):
    return [[math.gamma(a) for a in row] for row in array]

def beta_function(array1, array2):
    return [[math.gamma(a) * math.gamma(b) / math.gamma(a + b) for a, b in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def factorial(array):
    return [[math.factorial(int(a)) for a in row] for row in array]

def kronecker_product(matrix1, matrix2):
    return [[a * b for a in row1 for b in row2] for row1 in matrix1 for row2 in matrix2]

def hadamard_product(matrix1, matrix2):
    return [[a * b for a, b in zip(row1, row2)] for row1, row2 in zip(matrix1, matrix2)]

def matrix_power(matrix, n):
    result = matrix
    for _ in range(n - 1):
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*result)] for row in result]
    return result

def linear_interpolation(array, x_values, new_x):
    result = []
    for x in new_x:
        for i in range(len(x_values) - 1):
            if x_values[i] <= x <= x_values[i + 1]:
                slope = (array[i + 1] - array[i]) / (x_values[i + 1] - x_values[i])
                result.append(array[i] + slope * (x - x_values[i]))
                break
    return result

def cubic_interpolation(array, x_values, new_x):
    raise NotImplementedError("Cubic interpolation requires more complex algorithms.")

def range(array):
    return max(array) - min(array)

def variance(array, ddof=0):
    m = sum(array) / len(array)
    return sum((x - m) ** 2 for x in array) / (len(array) - ddof)

def skewness(array):
    m = sum(array) / len(array)
    std_dev = (variance(array)) ** 0.5
    return sum(((x - m) / std_dev) ** 3 for x in array) / len(array)

def kurtosis(array):
    m = sum(array) / len(array)
    std_dev = (variance(array)) ** 0.5
    return sum(((x - m) / std_dev) ** 4 for x in array) / len(array) - 3

def geometric_mean(array):
    product = 1
    for x in array:
        product *= x
    return product ** (1 / len(array))

def harmonic_mean(array):
    return len(array) / sum(1 / x for x in array)

def covariance(array1, array2):
    m1 = sum(array1) / len(array1)
    m2 = sum(array2) / len(array2)
    return sum((x - m1) * (y - m2) for x, y in zip(array1, array2)) / len(array1)

def correlation_coefficient(array1, array2):
    cov = covariance(array1, array2)
    std1 = (variance(array1)) ** 0.5
    std2 = (variance(array2)) ** 0.5
    return cov / (std1 * std2)

def spearman_rank_correlation(array1, array2):
    def rankdata(array):
        sorted_indices = sorted(range(len(array)), key=lambda i: array[i])
        ranks = [0] * len(array)
        for i, idx in enumerate(sorted_indices):
            ranks[idx] = i + 1
        return ranks
    
    rank1 = rankdata(array1)
    rank2 = rankdata(array2)
    return correlation_coefficient(rank1, rank2)

def kendall_tau(array1, array2):
    n = len(array1)
    concordant, discordant = 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            concordant += (array1[i] - array1[j]) * (array2[i] - array2[j]) > 0
            discordant += (array1[i] - array1[j]) * (array2[i] - array2[j]) < 0
    return (concordant - discordant) / (n * (n - 1) / 2)

def percentile_rank(array, value):
    below = sum(1 for x in array if x < value)
    equal = sum(1 for x in array if x == value)
    return (below + 0.5 * equal) / len(array) * 100

def quantiles(array, q_values):
    sorted_array = sorted(array)
    n = len(sorted_array)
    return [sorted_array[int(q * (n - 1))] for q in q_values]

def rolling_mean(array, window):
    return [sum(array[i:i + window]) / window for i in range(len(array) - window + 1)]

def rolling_std(array, window):
    def window_variance(window_array):
        m = sum(window_array) / len(window_array)
        return sum((x - m) ** 2 for x in window_array) / len(window_array)
    
    return [(window_variance(array[i:i + window])) ** 0.5 for i in range(len(array) - window + 1)]

def rolling_median(array, window):
    return [sorted(array[i:i + window])[window // 2] for i in range(len(array) - window + 1)]

def finite_difference(array, dx):
    return [(array[i+1] - array[i]) / dx for i in range(len(array) - 1)]

def gradient(array, spacing):
    grad = []
    n = len(array)
    for i in range(n):
        if i == 0:  # Forward difference
            grad.append((array[i+1] - array[i]) / spacing)
        elif i == n - 1:  # Backward difference
            grad.append((array[i] - array[i-1]) / spacing)
        else:  # Central difference
            grad.append((array[i+1] - array[i-1]) / (2 * spacing))
    return grad

def jacobian_matrix(func, array):
    epsilon = 1e-5
    jacobian = []
    for i in range(len(array)):
        perturb = [0] * len(array)
        perturb[i] = epsilon
        f_plus = func([x + p for x, p in zip(array, perturb)])
        f_minus = func([x - p for x, p in zip(array, perturb)])
        derivative = [(fp - fm) / (2 * epsilon) for fp, fm in zip(f_plus, f_minus)]
        jacobian.append(derivative)
    return jacobian

def trapezoidal_integral(array, dx):
    return sum((array[i] + array[i+1]) * dx / 2 for i in range(len(array) - 1))

def simpsons_integral(array, dx):
    n = len(array)
    if n % 2 == 0:
        raise ValueError("Array length must be odd for Simpson's rule.")
    integral = array[0] + array[-1]
    for i in range(1, n - 1):
        integral += 4 * array[i] if i % 2 != 0 else 2 * array[i]
    return integral * dx / 3

def cumulative_integral(array):
    cumulative = []
    total = 0
    for i in range(1, len(array)):
        total += (array[i-1] + array[i]) / 2
        cumulative.append(total)
    return cumulative

def time_series(data, time_index):
    return dict(zip(time_index, data))

def autocorrelation(array, lag):
    mean = sum(array) / len(array)
    numerator = sum((array[i] - mean) * (array[i+lag] - mean) for i in range(len(array) - lag))
    denominator = sum((x - mean) ** 2 for x in array)
    return numerator / denominator

def moving_average(array, window):
    return [sum(array[i:i+window]) / window for i in range(len(array) - window + 1)]

def seasonal_decomposition(array, period):
    trend = [sum(array[i:i+period]) / period for i in range(len(array) - period + 1)]
    seasonal = [array[i] - trend[i % period] for i in range(len(array))]
    residual = [array[i] - trend[i % period] - seasonal[i % period] for i in range(len(array))]
    return {"trend": trend, "seasonal": seasonal, "residual": residual}

def time_lagged_cross_correlation(array1, array2, lag):
    n = len(array1)
    if lag < 0:
        array1, array2 = array2[-lag:], array1[:n+lag]
    elif lag > 0:
        array1, array2 = array1[lag:], array2[:n-lag]
    else:
        array1, array2 = array1, array2
    mean1, mean2 = sum(array1) / len(array1), sum(array2) / len(array2)
    numerator = sum((x - mean1) * (y - mean2) for x, y in zip(array1, array2))
    denominator = (sum((x - mean1) ** 2 for x in array1) * sum((y - mean2) ** 2 for y in array2)) ** 0.5
    return numerator / denominator

def geospatial_array(data, coordinates):
    return [{"data": d, "coordinates": coord} for d, coord in zip(data, coordinates)]

def euclidean_distance(coord1, coord2):
    return sum((c1 - c2) ** 2 for c1, c2 in zip(coord1, coord2)) ** 0.5

def manhattan_distance(coord1, coord2):
    return sum(abs(c1 - c2) for c1, c2 in zip(coord1, coord2))

def geodesic_distance(coord1, coord2):
    R = 6371.0  # Earth's radius in kilometers
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(sqrt(a), math.sqrt(1 - a))

    return R * c

def rotate_coordinates(coords, angle, center=(0, 0)):
    angle = math.radians(angle)
    cx, cy = center
    rotated_coords = []
    for x, y in coords:
        translated_x = x - cx
        translated_y = y - cy

        rotated_x = translated_x * math.cos(angle) - translated_y * math.sin(angle)
        rotated_y = translated_x * math.sin(angle) + translated_y * math.cos(angle)

        final_x = rotated_x + cx
        final_y = rotated_y + cy
        rotated_coords.append((final_x, final_y))
    return rotated_coords

def translate_coordinates(coords, vector):
    translated_coords = [(x + vector[0], y + vector[1]) for x, y in coords]
    return translated_coords

def is_symmetric(matrix):
    return all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix)))

def is_positive_definite(matrix):
    n = len(matrix)
    for i in range(1, n + 1):
        sub_matrix = [row[:i] for row in matrix[:i]]
        determinant = sum(sub_matrix[k][k] for k in range(len(sub_matrix)))
        if determinant <= 0:
            return False
    return True

def validate_shape(array1, array2):
    return len(array1) == len(array2) and all(len(row1) == len(row2) for row1, row2 in zip(array1, array2))

def array_summary(array):
    flat = [item for row in array for item in row]
    mean_val = sum(flat) / len(flat)
    variance_val = sum((x - mean_val) ** 2 for x in flat) / len(flat)
    std_dev = variance_val ** 0.5
    median_val = sorted(flat)[len(flat) // 2] if len(flat) % 2 != 0 else (
        sorted(flat)[len(flat) // 2 - 1] + sorted(flat)[len(flat) // 2]) / 2
    geometric_mean = (1 if all(x > 0 for x in flat) else 0) * (pow(sum(flat), 1 / len(flat)))
    harmonic_mean = len(flat) / sum(1 / x for x in flat) if all(flat) else 0
    q25 = sorted(flat)[int(len(flat) * 0.25)]
    q75 = sorted(flat)[int(len(flat) * 0.75)]

    return {
        "count": len(flat),
        "sum": sum(flat),
        "mean": mean_val,
        "variance": variance_val,
        "std_dev": std_dev,
        "median": median_val,
        "min": min(flat),
        "max": max(flat),
        "range": max(flat) - min(flat),
        "geometric_mean": geometric_mean,
        "harmonic_mean": harmonic_mean,
        "q25": q25,
        "q75": q75,
        "iqr": q75 - q25,
        "skewness": sum(((x - mean_val) / std_dev) ** 3 for x in flat) / len(flat) if std_dev else 0,
        "kurtosis": sum(((x - mean_val) / std_dev) ** 4 for x in flat) / len(flat) - 3 if std_dev else 0,
    }

def memory_usage(array):
    flat = [item for row in array for item in row]
    return len(flat) * 8  # Assuming 8 bytes per element (float64)

def batch_add(arrays):
    result = arrays[0]
    for array in arrays[1:]:
        result = [[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(result, array)]
    return result

def batch_multiply(arrays):
    result = arrays[0]
    for array in arrays[1:]:
        result = [[a * b for a, b in zip(row1, row2)] for row1, row2 in zip(result, array)]
    return result

def batch_mean(arrays):
    total = batch_add(arrays)
    n = len(arrays)
    return [[val / n for val in row] for row in total]

def batch_std(arrays):
    mean_array = batch_mean(arrays)
    deviations = [[[abs(val - mean_val) ** 2 for val, mean_val in zip(row1, row2)]
                   for row1, row2 in zip(array, mean_array)] for array in arrays]
    mean_deviation = batch_mean(deviations)
    return [[val ** 0.5 for val in row] for row in mean_deviation]