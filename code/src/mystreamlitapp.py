import streamlit as st
import pandas as pd
from datetime import date
from WebScraping.dvag import input_tan

def render_web_data(**kwargs):
	# create page title
	st.title('Personal Finanz Tracker')
	st.header('Summe Vermögen')

	placeholder = st.empty()
	print(kwargs)

	barvermögen = placeholder.number_input('Bitte Barvermögen eingeben',value=0)
	if barvermögen != 0:
		placeholder.empty()

	total = float(barvermögen)

	for key in kwargs:
		if 'absolute' not in key.lower():
			total = total + float(str(kwargs[key]).replace('.','').replace(',','.'))
	
	total_str_front = str(total).split('.')[0]
	num_digits = len(total_str_front)
	rest = str(total).split('.')[1]
	# every 3 digits we need a seperator
	num_digits -= 3
	# only if the number has at least 4 digits
	while num_digits > 0:
		total_str_front = total_str_front[:num_digits] + '.' + total_str_front[num_digits:]
		num_digits -= 3
	
	total_str = total_str_front + ',' + rest


	st.markdown('# <center><font color="gold"> %s €</font></center>'%total_str,unsafe_allow_html=True)

	st.subheader('Aufgliederung nach Vermögenswerten')
	# display values via metrics
	l1_col1, l1_col2 = st.columns(2)
	l2_col1, l2_col2 = st.columns(2)
	l3_col1, l3_col2 = st.columns(2)

	st.metric(label='Barvermögen Total Value', value = str(barvermögen) + ' €')

	l1_col1.metric(label="Flatex Total Value", value=kwargs['total_flatex_value'] + " €", delta=kwargs['absolute_profit'] + " €")
	l1_col2.metric(label='Raiffeisen Giro Total Value', value = kwargs['total_raiffeisen_giro_value'] + " €")
	l2_col1.metric(label='Raiffeisen Creditcard Total Value', value = kwargs['total_raiffeisen_creditcard_value'] + " €")
	l2_col2.metric(label='N26 Total Value', value=kwargs['n26_balance'] + " €", delta=kwargs['n26_last_transaction'] + " €")

	l3_col1.metric(label='Bank99 Total Value', value=kwargs['total_bank99_balance'] + " €")
	l3_col2.metric(label='DVAG Total Value', value=str(kwargs['total_dvag_value']) + " €")



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
