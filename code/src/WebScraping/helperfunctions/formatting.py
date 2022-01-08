def format_string(number):
	"""
		INPUT: a number with "," as thousand delimiter and "." as deciaml delimiter.
		OUTPUT: a string number with "." as thousand delimiter and "," as decimal delimiter. 
	"""
	# convert to string
	number = str(number)
	# split the number into integer and decimal parts
	splitted = number.split(".")
	# geth the integer number part
	ints = splitted[0]
	# get the len of the integer part
	num_digits = len(ints)
	# check if the number was given as integer
	# if not we have a decimal part and we can extract that deciaml number
	if len(splitted) == 2:
		# get the decimal number part
		decimals = splitted[1]
	# else we expect the deciaml part to be only 00
	else:
		decimals = "00"
	num_digits -= 3
	# only if the number has at least 4 digits we need a formatting of the thousand delimiters
	while num_digits > 0:
		ints = ints[:num_digits] + '.' + ints[num_digits:]
		num_digits -= 3
	return ints + "," + decimals


