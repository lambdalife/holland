import math


def get_uniform_weighting_function():
	"""
	Returns a function that returns a constant, regardless of input; see :ref:`selection-strategy`


	:returns: a function that returns a constant
	"""
	return lambda x: 1


def get_linear_weighting_function(slope=1):
	"""
	Returns a function that weights its input linearly according to ``slope``; see :ref:`selection-strategy`

	:param slope: the multiplier for input
	:type slope: int/float


	:returns: a linear function
	"""
	return lambda x: slope*x


def get_polynomial_weighting_function(power=2):
	"""
	Returns a function that weights its input by raising the input to the ``power`` specified; see :ref:`selection-strategy`
	
	:param power: the power to raise the input to
	:type power: int/float


	:returns: a polynomial function
	"""
	return lambda x: x**power


def get_exponential_weighting_function(base=math.e):
	"""
	Returns a function that weights its input by raising the ``base`` to the power of the input; see :ref:`selection-strategy`

	:param base: the base to raise to the power of the input
	:type base: int/float


	:returns: a exponential function
	"""
	return lambda x: base**x


def get_logarithmic_weighting_function(base=math.e):
	"""
	Returns a function that weights its input getting the logarithm (with specified ``base``) of the input; see :ref:`selection-strategy`
	
	:param base: the base to calculate the logarithm of the input for
	:type base: int/float
	

	:returns: a logarithmic function

	
	.. note:: This fitness weighting function will throw an error for fitness scores less than or equal to 0.
	"""
	return lambda x: math.log(x, base)


def get_reciprocal_weighting_function():
	"""
	Returns a function that weights its input by raising the input to the -1 power; see :ref:`selection-strategy`

	The reciprocal weighting function is useful in cases where fitness should be minimized as the function results in granting higher selection probabilities to individuals with lower scores


	:returns: a function that returns ``1/input``


	.. note:: This fitness weighting function will throw an error for fitness scores equal to 0.
	"""
	return lambda x: 1/x