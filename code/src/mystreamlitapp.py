import streamlit as st
import pandas as pd
from datetime import date

def render_web_data(total_flatex_value, absolute_profit, total_raiffeisen_giro_value, total_raiffeisen_creditcard_value, n26_balance, n26_last_transaction):
	# create page title
	st.title('Personal Finanz Tracker')
	st.header('Übersicht und Zusammenfassung von Vermögen')
	# display values via metrics
	l1_col1, l1_col2 = st.columns(2)
	l2_col1, l2_col2 = st.columns(2)
	l1_col1.metric(label="Flatex Total Value", value=total_flatex_value + " €", delta=absolute_profit + " €")
	l1_col2.metric(label='Raiffeisen Giro Total Value', value = total_raiffeisen_giro_value + " €")
	l2_col1.metric(label='Raiffeisen Creditcard Total Value', value = total_raiffeisen_creditcard_value + " €")
	l2_col2.metric(label='N26 Total Value', value=n26_balance + " €", delta=n26_last_transaction + " €")

def render_df(PATH_DATA):

	# read in data and extract date information
	df = pd.read_csv(PATH_DATA,sep=";",parse_dates=['Datum'])
	df['Betrag'] = df.Betrag + ' €'
	df['Tag'] = df.Datum.dt.day
	df['Monat'] = df.Datum.dt.month
	df['Jahr'] = df.Datum.dt.year
	# convert Datum from datetime64ns to date
	df['Datum'] = df.Datum.dt.date

	# define the two columns for the radio filter widgets
	filter_col1, filters_col2 = st.columns(2)

	# define filter to filter by accounts
	types_of_moneyflow = ['Alles anzeigen'] + list(df.Typ.unique())
	types_of_accounts = ['Alle Konten', 'N26', 'ING', 'Girokonto Raika', 'Kreditkarte Raika', 'Bargeldrücklage']

	# create a filter by datetime input
	input_date = (date.today().replace(day=1),date.today())
	selected_date_range = st.date_input( "Would you like to filter for a time period?", input_date)
	# filter the df
	df = df[(df['Datum'] >= selected_date_range[0]) & (df['Datum'] <= selected_date_range[1])]


	filter_money = filter_col1.radio('Nach welchen Typen soll gefiltert werden?',types_of_moneyflow)
	if filter_money != 'Alles anzeigen':
		df = df[df.Typ == filter_money]
	filter_konto = filters_col2.radio('Nach welchem Konto soll gefiltert werden?', types_of_accounts)
	if filter_konto != 'Alle Konten':
		df = df[df.Konto == filter_konto]

	num_elems = st.slider('Wie viele Zeilen sollen betrachtet werden', 0, len(df), len(df)//5 if len(df)>100 else len(df))
	st.dataframe(df.sort_values('Datum',ascending=False).iloc[:num_elems])

	df['Betrag'] = df.Betrag.str.replace('.','').str.replace(',','.').str.replace(' €','').astype('float')
	df_grouped = df.groupby(['Monat']).sum()
	st.line_chart(df_grouped.Betrag)


    #df_by_category = df.groupby('Kategorie').sum()
    #st.bar_chart(df_by_category.sort_values('Betrag',ascending=False)['Betrag'])
