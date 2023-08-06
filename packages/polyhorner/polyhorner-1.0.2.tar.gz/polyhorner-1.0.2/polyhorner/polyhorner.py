import numpy as np
from numba import njit

# https://people.sc.fsu.edu/~jburkardt/py_src/monomial/mono_upto_enum.py
@njit
def _mono_up_to(D:int,M:int):
    value = _i4_choose(D+M,M)
    return value

# https://people.sc.fsu.edu/~jburkardt/py_src/monomial/i4_choose.py
@njit
def _i4_choose(n:int,k:int):
    mn = min(k, n-k)
    mx = max(k, n-k)

    if mn<0:
        value=0
    elif mn==0:
        value=1
    else:
        value = mx + 1
        for i in range (2, mn+1):
            value = (value*(mx+i))/i

    return int(value)


# https://people.sc.fsu.edu/~jburkardt/py_src/monomial/mono_unrank_grlex.py
@njit
def _mono_unrank_grlex(m:int,rank:int):

    if m<1:
        result = {'error':True, 'errormsg':'mono_unrank_grlex - Fatal error!   M < 1'}

    if rank<1:
        result = {'error':True, 'errormsg':'mono_unrank_grlex - Fatal error!   rank < 1'}

    x = np.zeros(m,dtype=np.int32)

    if m==1:
        x[0] = rank - 1
        return x
    #
    #  Determine the appropriate value of NM.
    #  Do this by adding up the number of compositions of sum 0, 1, 2, 
    #  ..., without exceeding RANK.  Moreover, RANK - this sum essentially
    #  gives you the rank of the composition within the set of compositions
    #  of sum NM.  And that's the number you need in order to do the
    #  unranking.
    #
    rank1 = 1
    nm = -1
    while ( True ):
        nm = nm + 1
        r = _i4_choose(nm+m-1,nm)
        if rank<rank1+r:
            break
        rank1 = rank1 + r

    rank2 = rank - rank1
    #
    #  Convert to KSUBSET format.
    #  Apology: an unranking algorithm was available for KSUBSETS,
    #  but not immediately for compositions.  One day we will come back
    #  and simplify all this.
    #
    ks = m - 1
    ns = nm + m - 1
    xs = np.zeros( ks, dtype = np.int32 )

    nksub = _i4_choose( ns, ks )

    j = 1

    for i in range ( 1, ks + 1 ):
        r = _i4_choose( ns - j, ks - i )

        while ( r <= rank2 and 0 < r ):
            rank2 = rank2 - r
            j = j + 1
            r = _i4_choose( ns - j, ks - i )

        xs[i-1] = j
        j = j + 1
    #
    #  Convert from KSUBSET format to COMP format.
    #
    x[0] = xs[0] - 1
    for i in range ( 2, m ):
        x[i-1] = xs[i-1] - xs[i-2] - 1
    x[m-1] = ns - xs[ks-1]

    return x


@njit
def _Dim1PolyHornerBuild(Xhere:np.array, N:int, M:int):
    # implements the simple Horner method for univariate polynomials
    X = np.ones((N,M+1))
    X[:,1] = Xhere.flatten()
    for n in range(2,M+1):
        X[:,n] = np.multiply(X[:,n-1], X[:,1])
    
    return X


@njit
def _DimNPolyHornerBuild(Xhere, N, M, D, expo):
    # We simply loop for each variables to get them to their respective power, and stack them up.
    # This follow Horner's method and is most efficient.
    Xi = [None] * D
    for iX in range(D):
        Xi[iX] = np.zeros((N,(M[iX,0])))
        Xi[iX][:,0] = Xhere[:,iX]
        for n in range(1,M[iX,0]):
            Xi[iX][:,n] = np.multiply(Xi[iX][:,n-1], Xi[iX][:,0])

    Nterms = np.size(expo,0)

    # We stack the columns according to the exponent recipe we have
    X = np.zeros((N,Nterms), dtype=float)
    for iT in range(Nterms):
        ThisX = np.ones((N,D), dtype=float)
        for iD in range(D):
            if expo[iT,iD]>0:
                ThisX[:,iD] = Xi[iD][:,expo[iT,iD]-1]
        X[:,iT] = np.prod(ThisX, axis=1)
    
    return X

def BuildPolynomial(D:int,M:np.ndarray):
    # Generates all exponents possible
    if isinstance(M,int):
        maxM = M
    else:
        maxM = int(max(M))

    Nterms = _mono_up_to(maxM, D)
    Exponents = np.zeros((Nterms,D), dtype=int)
    
    for i in range(1,Nterms+1):
        checkexp = _mono_unrank_grlex(D,i)
        if isinstance(checkexp,dict):
            return checkexp
        Exponents[i-1,:] = checkexp

    if isinstance(M,int):
        return Exponents, np.size(Exponents,0)
    else:
        for i in range(D):
            Exponents = Exponents[Exponents[:,i] <= M[i] , : ]
        return Exponents, np.size(Exponents,0)


def horner(Xin:np.array,  M:np.array, N:int=0, D:int=0, Scale=True)-> np.array:
    # Xin Needs to be of size (N,D), where N is the number of data points, and D the number of dimensions in the X matrix
    # M should either be a single interger, of an array of size (D,1).
    # Passing N and D manually will work only if they are the right size [I consider removing this later]
    # Scale=True will scale the data by the std.dev. to mitigate the problem of rounding error causing issues in higher order polynomial regressions
    
    # TODO, right now, the polynomial order is required to be a vector with the same dimension has the number of variables.
    # however, we only treat the M[0] polynomial in all directions.
    # I need to discard the monomials that do not fit the multivariate polynomial

    # TODO, allow to identify columns in Xin that should get cross multiplied

    # TODO, allow to simply pass the exponent matrix

    # Check Dimensions
    if (N==0) or (D==0):
        if isinstance(Xin, np.ndarray):
            try:
                D = np.size(Xin,1)
            except IndexError:
                # The array is one dimensional, we need to 
                D = 1  
            N = np.size(Xin,0)
            Xin = np.reshape(Xin,(N,D))
        else:
            HornerDict = {'error':True, 'errormsg':'Make sure you send a numpy array for your matrix of independent variables.'}
            return HornerDict

    # Check how to deal with the polynomial order that can be integer, of ndarray
    if isinstance(M,int):
        M = M*np.ones((D,1), dtype=int)
    elif isinstance(M, np.ndarray):
        if np.size(M,0)==D:
            try:
                np.size(M,1)
            except IndexError:
                M = M.reshape(D,1)
            pass
        elif np.size(M,0)==1:
            M = int(M[0])*np.ones((D,1), dtype=int)
        else:
            HornerDict = {'error':True, 'errormsg':'Provide a polynomial order for each independent variable, or a single integer. Is your Xin matrix is of size (N,D)?'}
            return HornerDict
            
    else:
        HornerDict = {'error':True, 'errormsg':'Provide a polynomial order for each independent variable, or a single integer.'}
        return HornerDict

    if D == np.size(M,0):
        pass
    else:
        HornerDict = {'error':True, 'errormsg':'Wrong input format to PolyHorner. The polynomial order must be a column vector the same size has the number of columns in Xin.'}
        return HornerDict

    # Scale data if we need to
    Xhere = Xin.copy()

    if Scale:
        scalingX = np.zeros((D,1))
        for i in range(D):
            scalingX[i,0] = np.std(Xin[:,i])
            if scalingX[i,0]==0:
                HornerDict = {'error':True, 'errormsg':'One of the X data vector is constant. Do you even know how to do a regression?'}
                return HornerDict
            Xhere[:,i] = Xin[:,i] / scalingX[i,0]

    if D==1:
        # Univariate polynomials, are easy
        if M>0:
            X = _Dim1PolyHornerBuild(Xhere, N, int(M[0]))
            expo = np.arange(0,M[0]+1,1)
            expo = np.reshape(expo,(expo.shape[0],1))
        Nterms = X.shape[1]
    else:
        # Exponents will be a matrix

        # we create a list with an entry for each variable
        maxM = int(max(M))
        # Nterms = _mono_up_to(maxM, D)
        expo, Nterms = BuildPolynomial(D,M)
        if isinstance(expo,dict):
            # we got an error
            return expo

        X = _DimNPolyHornerBuild(Xhere, N, M, D, expo)


    if Scale:
        # if Invert:
        #     Nterms = (Nterms-1)*2+1
        scalingfactors  = np.ones((Nterms,1))
        for i in range(Nterms):
            for j in range(D):
                scalingfactors[i,0] = scalingfactors[i,0] / (scalingX[j,0]**expo[i,j])
    else:
        scalingfactors = False


    HornerDict = {'X': X, 'exponents': expo, 'scalingfactors':scalingfactors, 'Nterms':Nterms, 'Dim':D, 'error':False}

    return HornerDict
