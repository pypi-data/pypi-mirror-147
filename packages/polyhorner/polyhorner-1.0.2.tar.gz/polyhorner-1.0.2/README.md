# polyhorner
This package will:
- build univariate polynomials using an optimized Horner's method and fast numba loops
- build multivariate polynomials using a somewhat optimized Horner's method and fast numba loops

## univariate polynomial example
Suppose you have x, and y data, and you want to model y = a0 + a1 x + a2 x^2 + a3 x^3 + a4 x^4
Let Mat be a numpy matrix of size (N,1), where N is the number of data points.
X = polyhorner.horner(Mat, 4) will build your X matrix ready for the regression (optimized using Horner's method)

## multivaraite polynomial example
Suppose you have x, y, and z data, and you want to model using apolynomial of order 3 in x, and 2 in y, with cross-products
z = a0 + a1 x + a2 x^2 + a3 x^3 + a4 y + a5 y^2 + a6 xy + a7 x^2y + a8 x^3y + a9 xy^2 + a10 x^2y^2 + a11 x^3y^2
let Mat be a numpy matrix of size (N,2), where N is the number of data points.
let Expo be a numpy matrix of size (2,1) = (3,2)
X = polyhorner.horner(Mat, Expo) will build your X matrix ready for the regression (semi-optimized using Horner's method)



I use some functions distributed under the GNU LGPL license from 
https://people.sc.fsu.edu/~jburkardt/py_src/monomial


Thanks to Pssolanki for helping fix issues
