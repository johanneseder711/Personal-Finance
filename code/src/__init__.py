import streamlit as st
from WebScraping.raiffeisen import get_raiffaisen_balance
from WebScraping.flatex import get_flatex_balance
from mystreamlitapp import render_web_data, render_df

def main():
	# call functions
	total_flatex_value,absolute_profit = get_flatex_balance()
	total_raiffeisen_giro_value,total_raiffeisen_creditcard_value = get_raiffaisen_balance()

	render_web_data(total_flatex_value,absolute_profit,total_raiffeisen_giro_value,total_raiffeisen_creditcard_value)
	render_df('../../data/MoneyControl/MoneyControl-CSVExport_2021-12-29.csv')


# execute main function
if __name__ == "__main__":
	main()