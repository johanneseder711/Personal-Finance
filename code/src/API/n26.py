from n26.api import Api

def get_n26_balance():
	api_client = Api()
	total_balance = api_client.get_spaces()['totalBalance']
	total_balance = str(total_balance).replace('.',',')
	# display the string (which is the money amount) with a "." as a separator of thousands
	num_digits = len(total_balance.split(',')[0])
	# every 3 digits we need a seperator
	num_digits -= 3
	# only if the number has at least 4 digits
	while num_digits > 0:
		total_balance = total_balance[:num_digits] + '.' + total_balance[num_digits:]
		num_digits -= 3

	statements = api_client.get_transactions()
	last_transaction_found = False
	counter = 0
	# while the last transaction is not found
	while not last_transaction_found:
		# iterate over the dicctionary
		if 'Hawaii' in statements[counter]['partnerName']:
			counter += 1
		else:
			# is the dicct contains a key named partnerName -> this is not a valid income stream or payment
			last_transaction_found = True
			last_transaction_amount = statements[counter]['amount']

	last_transaction_amount = str(last_transaction_amount).replace('.',',')
	return (total_balance, last_transaction_amount)

