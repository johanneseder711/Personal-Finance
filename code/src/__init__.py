import streamlit as st
from WebScraping.raiffeisen import get_raiffaisen_balance
from WebScraping.flatex import get_flatex_balance
from WebScraping.bitpanda import get_bitpanda_balance
from WebScraping.bank99 import get_bank99_balance
from WebScraping.dvag import get_dvag_balance
from mystreamlitapp import render_web_data, render_df
from API.n26 import get_n26_balance

def main():
	# call functions
	total_flatex_value,absolute_delta_day_before = get_flatex_balance()
	total_raiffeisen_giro_value,total_raiffeisen_creditcard_value = get_raiffaisen_balance()

	n26_balance, n26_last_transaction = get_n26_balance()

	total_bank99_balance = get_bank99_balance()

	total_dvag_value = get_dvag_balance()

	get_bitpanda_balance()


	# render overview of account balances
	render_web_data(total_flatex_value=total_flatex_value,absolute_delta_day_before=absolute_delta_day_before,total_raiffeisen_giro_value = total_raiffeisen_giro_value,total_raiffeisen_creditcard_value=total_raiffeisen_creditcard_value,n26_balance=n26_balance,n26_last_transaction=n26_last_transaction, total_bank99_balance=total_bank99_balance, total_dvag_value=total_dvag_value)

	# render dataframe from money control
	render_df('../../data/MoneyControl/MoneyControl-CSVExport_2022-01-03.csv')


# execute main function
if __name__ == "__main__":
	main()
