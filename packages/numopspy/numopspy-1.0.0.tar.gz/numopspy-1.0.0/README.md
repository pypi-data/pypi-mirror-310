# numopspy

**numopspy** is a comprehensive Python library for numerical operations, mathematical computations, and array manipulations built with pure Python. It’s designed to be a robust alternative to popular libraries like NumPy, with added features and functionalities that simplify advanced numerical, statistical, geospatial, and time-series tasks.

## Introduction

While existing libraries like NumPy are excellent for numerical computations, **numopspy** bridges the gap by introducing unique functionalities and eliminating common dependencies. Designed with simplicity and versatility in mind, **numopspy** empowers users to perform operations traditionally split across multiple libraries — all within a lightweight, dependency-free package.

## Why Choose numopspy?

- **No External Dependencies**: Written entirely in pure Python.
- **Expanded Functionality**: Supports advanced features like geospatial operations, symbolic mathematics, dynamic arrays, and batch operations.
- **Categorized Functions**: A complete suite of 322 functions, categorized and easy to use.
- **Enhanced Array Handling**: Geospatial arrays, sparse arrays, hierarchical indexing, and more.
- **Advanced Time Series and Statistical Analysis**: Functions for rolling averages, seasonal decomposition, skewness, kurtosis, and other metrics.

---

## New Features in numopspy

1. **Sparse Matrix and Array Support**:
   - Sparse to dense conversion, density-based sparse creation, and more.
2. **Comprehensive Complex Number Handling**:
   - Polar/Cartesian transformations, FFT for complex arrays, and more.
3. **Geospatial Functions**:
   - Euclidean, Manhattan, and geodesic distance computations.
4. **Differentiation and Integration**:
   - Numerical derivatives, gradients, and cumulative integrals.
5. **Time Series Analysis**:
   - Autocorrelation, moving averages, and trend decomposition.
6. **Array Validation and Meta Information**:
   - Validate shape compatibility, symmetry, and retrieve comprehensive statistics.
7. **Batch Operations**:
   - Batch-wise addition, multiplication, and aggregation of arrays.

---

## Complete List of Functions (322)

Here’s the complete list of **Core Array Functions** categorized under **Array Creation**, with all functions detailed:

---

### **Array Creation Functions**
1. `zeros(shape)`: Create an array filled with zeros.
2. `ones(shape)`: Create an array filled with ones.
3. `full(shape, fill_value)`: Create an array filled with a specified value.
4. `empty(shape)`: Create an uninitialized array.
5. `arange(start, stop, step)`: Create an array with evenly spaced values.
6. `linspace(start, stop, num)`: Create an array with `num` evenly spaced points between `start` and `stop`.
7. `logspace(start, stop, num, base)`: Create an array with `num` logarithmically spaced points between `base**start` and `base**stop`.
8. `eye(n, m)`: Create a 2D array with ones on the diagonal and zeros elsewhere.
9. `identity(n)`: Create an identity matrix.
10. `diag(v, k=0)`: Create a diagonal matrix from a 1D array or extract a diagonal from a 2D array.
11. `from_iterable(iterable)`: Create an array from an iterable object.
12. `from_function(func, shape)`: Create an array by applying a function to each coordinate.
13. `meshgrid(*arrays)`: Generate coordinate matrices from coordinate vectors.
14. `empty_like(array)`: Create an uninitialized array with the same shape as a given array.
15. `zeros_like(array)`: Create an array of zeros with the same shape as a given array.
16. `ones_like(array)`: Create an array of ones with the same shape as a given array.
17. `full_like(array, fill_value)`: Create an array filled with a specified value with the same shape as a given array.
18. `mgrid[start:stop:step]`: Create a dense multi-dimensional grid.
19. `ogrid[start:stop:step]`: Create an open multi-dimensional grid.
20. `random(shape, seed=None)`: Create an array filled with random values between 0 and 1.

---

### **Array Manipulation Functions**

1. `reshape(array, new_shape)`: Reshape an array without changing data.
2. `ravel(array)`: Flatten an array into 1D.
3. `flatten(array)`: Return a copy of the array collapsed into 1D.
4. `expand_dims(array, axis)`: Expand the shape of an array by adding a new axis.
5. `squeeze(array, axis=None)`: Remove single-dimensional entries from the shape of an array.
6. `concatenate(arrays, axis)`: Join arrays along a specified axis.
7. `stack(arrays, axis)`: Stack arrays along a new dimension.
8. `vstack(arrays)`: Stack arrays vertically (row-wise).
9. `hstack(arrays)`: Stack arrays horizontally (column-wise).
10. `dstack(arrays)`: Stack arrays along the depth (third dimension).
11. `column_stack(arrays)`: Stack 1D arrays as columns into a 2D array.
12. `row_stack(arrays)`: Stack 1D arrays as rows into a 2D array.
13. `split(array, indices, axis)`: Split an array into multiple sub-arrays along a specified axis.
14. `array_split(array, sections, axis)`: Split an array into unequal parts along a specified axis.
15. `hsplit(array, sections)`: Split an array horizontally (column-wise).
16. `vsplit(array, sections)`: Split an array vertically (row-wise).
17. `dsplit(array, sections)`: Split an array along the depth (third dimension).
18. `roll(array, shift, axis)`: Roll array elements along a specified axis.
19. `flip(array, axis)`: Reverse the order of elements along a specified axis.
20. `rot90(array, k, axes)`: Rotate an array by 90 degrees `k` times.
21. `transpose(array, axes)`: Permute the dimensions of an array.
22. `swapaxes(array, axis1, axis2)`: Interchange two axes of an array.
23. `moveaxis(array, source, destination)`: Move specified axes to new positions.
24. `pad(array, pad_width, mode)`: Pad an array with specified values.
25. `repeat(array, repeats, axis)`: Repeat elements of an array along a specified axis.
26. `tile(array, reps)`: Construct an array by repeating `array` the number of times given by `reps`.
27. `resize(array, new_shape)`: Resize an array, trimming or padding with zeros as necessary.
28. `append(array, values, axis)`: Append values to an array along a specified axis.
29. `insert(array, index, values, axis)`: Insert values along a specified axis at a given index.
30. `delete(array, index, axis)`: Delete elements from an array along a specified axis.
31. `where(condition, x, y)`: Return elements chosen from `x` or `y` depending on `condition`.
32. `nonzero(array)`: Return the indices of non-zero elements.
33. `argwhere(array)`: Return the indices where the condition is `True`.
34. `flatnonzero(array)`: Return the indices of non-zero elements in the flattened array.
35. `diag(array, k=0)`: Extract or construct a diagonal matrix.
36. `tril(array, k=0)`: Lower triangle of an array.
37. `triu(array, k=0)`: Upper triangle of an array.
38. `indices(dimensions)`: Return a grid of indices for a given shape.
39. `broadcast(array1, array2)`: Broadcast two arrays to a common shape.
40. `broadcast_to(array, shape)`: Broadcast an array to a new shape.
41. `ix_(*arrays)`: Construct index arrays for advanced broadcasting.

---

### **Mathematical Functions**
- ### **Arithmetic Operations**

1. `add_elementwise(array1, array2)`: Perform element-wise addition.
2. `subtract_elementwise(array1, array2)`: Perform element-wise subtraction.
3. `multiply_elementwise(array1, array2)`: Perform element-wise multiplication.
4. `divide_elementwise(array1, array2)`: Perform element-wise division.
5. `modulus(array1, array2)`: Compute the element-wise modulus.
6. `power(array, exponent)`: Raise each element of the array to the specified power.
7. `sqrt(array)`: Compute the square root of each element.
8. `absolute(array)`: Compute the absolute value of each element.
9. `reciprocal(array)`: Compute the reciprocal of each element.
10. `negate(array)`: Negate each element in the array.
11. `sign(array)`: Return the sign of each element (`1` for positive, `-1` for negative, and `0` for zero).
12. `floor(array)`: Compute the floor of each element.
13. `ceil(array)`: Compute the ceiling of each element.
14. `round(array, decimals)`: Round each element to the specified number of decimals.
15. `clip(array, min_val, max_val)`: Clip values in the array to a specified range.
16. `exp(array)`: Compute the exponential of each element.
17. `log(array)`: Compute the natural logarithm of each element.
18. `log10(array)`: Compute the base-10 logarithm of each element.
19. `log2(array)`: Compute the base-2 logarithm of each element.
20. `sin(array)`: Compute the sine of each element.
21. `cos(array)`: Compute the cosine of each element.
22. `tan(array)`: Compute the tangent of each element.
23. `arcsin(array)`: Compute the inverse sine of each element.
24. `arccos(array)`: Compute the inverse cosine of each element.
25. `arctan(array)`: Compute the inverse tangent of each element.
26. `arctan2(y, x)`: Compute the element-wise arc tangent of `y/x` considering the quadrant.
27. `sinh(array)`: Compute the hyperbolic sine of each element.
28. `cosh(array)`: Compute the hyperbolic cosine of each element.
29. `tanh(array)`: Compute the hyperbolic tangent of each element.
30. `deg2rad(array)`: Convert degrees to radians for each element.
31. `rad2deg(array)`: Convert radians to degrees for each element.

- ### **Special Functions**

1. `gamma_function(array)`: Compute the gamma function for each element.
2. `beta_function(array1, array2)`: Compute the beta function element-wise.
3. `factorial(array)`: Compute the factorial for each integer in the array.
4. `digamma(array)`: Compute the digamma function for each element.
5. `erf(array)`: Compute the error function for each element.
6. `erfc(array)`: Compute the complementary error function for each element.
7. `zeta(array, q)`: Compute the Riemann zeta function for each element.
8. `lambertw(array)`: Compute the Lambert W function for each element.
9. `heaviside(array, value)`: Compute the Heaviside step function for each element.
10. `binomial_coefficient(n, k)`: Compute the binomial coefficient element-wise.
11. `legendre_polynomial(n, x)`: Compute the Legendre polynomial of degree `n` at `x`.
12. `hermite_polynomial(n, x)`: Compute the Hermite polynomial of degree `n` at `x`.
13. `laguerre_polynomial(n, x)`: Compute the Laguerre polynomial of degree `n` at `x`.

---

### **Statistical Operations**
- ### **Descriptive Statistics**

1. `array_summary(array)`: Retrieve comprehensive statistics for an array.
2. `mean(array)`: Compute the mean.
3. `median(array)`: Compute the median.
4. `variance(array)`: Compute the variance.
5. `std(array)`: Compute the standard deviation.
6. `skewness(array)`: Compute the skewness.
7. `kurtosis(array)`: Compute the kurtosis.
8. `range(array)`: Compute the range of the array.
9. `min(array)`: Compute the minimum value in the array.
10. `max(array)`: Compute the maximum value in the array.
11. `percentile(array, q)`: Compute the q-th percentile of the array.
12. `quantiles(array, num_quantiles)`: Compute specified quantiles of the array.
13. `iqr(array)`: Compute the interquartile range.
14. `geometric_mean(array)`: Compute the geometric mean.
15. `harmonic_mean(array)`: Compute the harmonic mean.
16. `mode(array)`: Compute the mode of the array.

- ### **Correlation and Covariance**

1. `correlation_coefficient(array1, array2)`: Compute Pearson’s correlation coefficient.
2. `covariance(array1, array2)`: Compute the covariance between two arrays.
3. `spearman_rank_correlation(array1, array2)`: Compute Spearman’s rank correlation coefficient.
4. `kendall_tau(array1, array2)`: Compute Kendall’s Tau correlation coefficient.
5. `auto_correlation(array, lag)`: Compute the autocorrelation of an array for a given lag.
6. `partial_correlation(array1, array2, control)`: Compute the partial correlation between two arrays while controlling for a third.
7. `cross_correlation(array1, array2)`: Compute the cross-correlation between two arrays.
8. `distance_correlation(array1, array2)`: Compute the distance correlation between two arrays.
9. `correlation_matrix(matrix)`: Compute the correlation matrix for a set of variables.
10. `covariance_matrix(matrix)`: Compute the covariance matrix for a set of variables.

---

### **Linear Algebra**
- ### **Matrix Operations**

1. `linalg_det(matrix)`: Compute the determinant of a matrix.
2. `linalg_inv(matrix)`: Compute the inverse of a matrix.
3. `transpose(matrix)`: Transpose a matrix.
4. `matrix_power(matrix, n)`: Raise a matrix to the power `n`.
5. `kronecker_product(matrix1, matrix2)`: Compute the Kronecker product of two matrices.
6. `hadamard_product(matrix1, matrix2)`: Compute the Hadamard (element-wise) product of two matrices.
7. `dot(matrix1, matrix2)`: Compute the dot product of two matrices.
8. `vdot(matrix1, matrix2)`: Compute the vector dot product.
9. `inner_product(matrix1, matrix2)`: Compute the inner product of two matrices.
10. `outer_product(matrix1, matrix2)`: Compute the outer product of two matrices.
11. `tensordot(matrix1, matrix2, axes)`: Compute the tensor dot product along specified axes.
12. `cholesky_decomposition(matrix)`: Compute the Cholesky decomposition of a matrix.
13. `qr_decomposition(matrix)`: Compute the QR decomposition of a matrix.
14. `svd(matrix)`: Compute the Singular Value Decomposition (SVD) of a matrix.
15. `eigenvalues(matrix)`: Compute the eigenvalues of a matrix.
16. `eigenvectors(matrix)`: Compute the eigenvectors of a matrix.
17. `matrix_rank(matrix)`: Compute the rank of a matrix.
18. `pinv(matrix)`: Compute the pseudo-inverse of a matrix.
19. `trace(matrix)`: Compute the trace (sum of diagonal elements) of a matrix.
20. `norm(matrix, ord)`: Compute the matrix norm with a specified order.
21. `frobenius_norm(matrix)`: Compute the Frobenius norm of a matrix.

---

### **Geospatial Operations**
- ### **Geospatial Calculations**

1. `euclidean_distance(coord1, coord2)`: Compute the Euclidean distance between two points.
2. `manhattan_distance(coord1, coord2)`: Compute the Manhattan distance between two points.
3. `geodesic_distance(coord1, coord2)`: Compute the geodesic distance (great-circle distance) between two points on the Earth's surface.
4. `rotate_coordinates(coords, angle, center)`: Rotate a set of coordinates around a specified center by a given angle.
5. `translate_coordinates(coords, vector)`: Translate a set of coordinates by a specified vector.
6. `midpoint(coord1, coord2)`: Compute the midpoint between two coordinates.
7. `bearing(coord1, coord2)`: Calculate the initial bearing (azimuth) between two points.
8. `bounding_box(coords)`: Compute the bounding box for a set of coordinates.
9. `polygon_area(vertices)`: Calculate the area of a polygon defined by its vertices.
10. `haversine_distance(coord1, coord2)`: Compute the Haversine distance between two geographical points.

---

### **Random Sampling**
- ### **Random Generators**

1. `random_rand(n)`: Generate `n` random numbers between 0 and 1.
2. `random_normal(mean, std, size)`: Generate samples from a normal distribution.
3. `random_uniform(low, high, size)`: Generate samples from a uniform distribution.
4. `random_choice(array, size)`: Randomly sample elements from an array.
5. `random_randint(low, high, size)`: Generate random integers within a specified range.
6. `random_beta(alpha, beta, size)`: Generate samples from a Beta distribution.
7. `random_binomial(n, p, size)`: Generate samples from a Binomial distribution.
8. `random_chisquare(df, size)`: Generate samples from a Chi-square distribution.
9. `random_exponential(scale, size)`: Generate samples from an Exponential distribution.
10. `random_f(dfnum, dfden, size)`: Generate samples from an F-distribution.
11. `random_gamma(shape, scale, size)`: Generate samples from a Gamma distribution.
12. `random_geometric(p, size)`: Generate samples from a Geometric distribution.
13. `random_gumbel(loc, scale, size)`: Generate samples from a Gumbel distribution.
14. `random_hypergeometric(ngood, nbad, nsample, size)`: Generate samples from a Hypergeometric distribution.
15. `random_laplace(loc, scale, size)`: Generate samples from a Laplace distribution.
16. `random_logistic(loc, scale, size)`: Generate samples from a Logistic distribution.
17. `random_lognormal(mean, sigma, size)`: Generate samples from a Log-Normal distribution.
18. `random_multinomial(n, pvals, size)`: Generate samples from a Multinomial distribution.
19. `random_multivariate_normal(mean, cov, size)`: Generate samples from a Multivariate Normal distribution.
20. `random_negative_binomial(n, p, size)`: Generate samples from a Negative Binomial distribution.
21. `random_noncentral_chisquare(df, nonc, size)`: Generate samples from a Noncentral Chi-square distribution.
22. `random_pareto(a, size)`: Generate samples from a Pareto distribution.
23. `random_poisson(lam, size)`: Generate samples from a Poisson distribution.
24. `random_power(a, size)`: Generate samples from a Power distribution.
25. `random_rayleigh(scale, size)`: Generate samples from a Rayleigh distribution.
26. `random_standard_cauchy(size)`: Generate samples from a Standard Cauchy distribution.
27. `random_standard_exponential(size)`: Generate samples from a Standard Exponential distribution.
28. `random_standard_normal(size)`: Generate samples from a Standard Normal distribution.
29. `random_standard_t(df, size)`: Generate samples from a Standard T-distribution.
30. `random_triangular(left, mode, right, size)`: Generate samples from a Triangular distribution.
31. `random_vonmises(mu, kappa, size)`: Generate samples from a Von Mises distribution.
32. `random_wald(mean, scale, size)`: Generate samples from a Wald distribution.
33. `random_weibull(a, size)`: Generate samples from a Weibull distribution.
34. `random_zipf(a, size)`: Generate samples from a Zipf distribution.
35. `random_seed(seed)`: Set the random seed for reproducibility.

---

### **Fourier Transforms**
- ### **1D and Multi-Dimensional FFT**

1. `fft(array)`: Perform a 1D Fast Fourier Transform.
2. `ifft(array)`: Perform a 1D Inverse Fast Fourier Transform.
3. `fft2(array)`: Perform a 2D Fast Fourier Transform.
4. `ifft2(array)`: Perform a 2D Inverse Fast Fourier Transform.
5. `fftn(array, axes)`: Perform an n-dimensional Fast Fourier Transform along specified axes.
6. `ifftn(array, axes)`: Perform an n-dimensional Inverse Fast Fourier Transform along specified axes.
7. `rfft(array)`: Perform a 1D real-input Fast Fourier Transform.
8. `irfft(array)`: Perform a 1D Inverse Fast Fourier Transform on real input.
9. `rfft2(array)`: Perform a 2D real-input Fast Fourier Transform.
10. `irfft2(array)`: Perform a 2D Inverse Fast Fourier Transform on real input.
11. `rfftn(array, axes)`: Perform an n-dimensional real-input Fast Fourier Transform.
12. `irfftn(array, axes)`: Perform an n-dimensional Inverse Fast Fourier Transform on real input.
13. `fftshift(array)`: Shift the zero-frequency component to the center of the spectrum.
14. `ifftshift(array)`: Undo the shift applied by `fftshift`.
15. `fftfreq(n, d)`: Return the Discrete Fourier Transform sample frequencies.
16. `rfftfreq(n, d)`: Return the sample frequencies for a real-input FFT.

---

### **Differentiation and Integration**
- ### **Numerical Differentiation**

1. `finite_difference(array, dx)`: Compute numerical derivatives using finite differences.
2. `gradient(array, spacing)`: Compute the gradient of an array.
3. `jacobian_matrix(func, array)`: Compute the Jacobian matrix for a vector function.
4. `hessian_matrix(func, array)`: Compute the Hessian matrix for a scalar function.
5. `central_difference(array, dx)`: Compute numerical derivatives using the central difference method.
6. `forward_difference(array, dx)`: Compute numerical derivatives using the forward difference method.
7. `backward_difference(array, dx)`: Compute numerical derivatives using the backward difference method.
8. `partial_derivative(func, array, index, dx)`: Compute the partial derivative of a function with respect to a specific variable.

- ### **Numerical Integration**

1. `trapezoidal_integral(array, dx)`: Approximate the integral using the trapezoidal rule.
2. `simpsons_integral(array, dx)`: Approximate the integral using Simpson’s rule.
3. `cumulative_integral(array)`: Compute the cumulative integral of the array.
4. `midpoint_integral(func, a, b, n)`: Approximate the integral using the midpoint rule.
5. `monte_carlo_integral(func, bounds, samples)`: Approximate the integral using the Monte Carlo method.
6. `romberg_integral(func, a, b, tol)`: Approximate the integral using Romberg's method.
7. `gauss_quadrature(func, n, a, b)`: Approximate the integral using Gauss-Legendre quadrature.
8. `adaptive_quadrature(func, a, b, tol)`: Approximate the integral using adaptive quadrature.