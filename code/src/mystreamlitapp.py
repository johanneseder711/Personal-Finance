import streamlit as st
import pandas as pd
from datetime import date
from WebScraping.dvag import input_tan
from WebScraping.helperfunctions.formatting import format_string
import matplotlib.pyplot as plt

def render_web_data(**kwargs):
	# create page title
	st.title('Personal Finanz Tracker')
	st.header('Summe Vermögen')

	placeholder = st.empty()

	barvermögen = placeholder.number_input('Bitte Barvermögen eingeben',value=0)
	if barvermögen != 0:
		placeholder.empty()

	total = float(barvermögen)

	for key in kwargs:
		if 'absolute' not in key.lower():
			total = total + float(str(kwargs[key]).replace('.','').replace(',','.'))
	
	# convert to corretly formatted strings for display
	total_str = format_string(total)
	barvermögen_str = format_string(barvermögen)

	# display total balance green if > 0 else red
	st.markdown('# <center><font color="green"> %s €</font></center>'%total_str,unsafe_allow_html=True) if total > 0 else st.markdown('# <center><font color="red"> %s €</font></center>'%total_str,unsafe_allow_html=True)

	st.subheader('Aufgliederung nach Vermögenswerten')
	# display values via metrics
	l1_col1, l1_col2 = st.columns(2)
	l2_col1, l2_col2 = st.columns(2)
	l3_col1, l3_col2 = st.columns(2)

	st.metric(label='Barvermögen Total Value', value = str(barvermögen_str) + ' €')

	l1_col1.metric(label="Flatex Total Value", value=kwargs['total_flatex_value'] + " €", delta=kwargs['absolute_delta_day_before'] + " €")
	l1_col2.metric(label='Raiffeisen Giro Total Value', value = kwargs['total_raiffeisen_giro_value'] + " €")
	l2_col1.metric(label='Raiffeisen Creditcard Total Value', value = kwargs['total_raiffeisen_creditcard_value'] + " €")
	l2_col2.metric(label='N26 Total Value', value=kwargs['n26_balance'] + " €", delta=kwargs['n26_last_transaction'] + " €")

	l3_col1.metric(label='Bank99 Total Value', value=kwargs['total_bank99_balance'] + " €")
	l3_col2.metric(label='DVAG Total Value', value=str(kwargs['total_dvag_value']) + " €")



def render_df(PATH_DATA):

	# read in data and extract date information
	df = pd.read_csv(PATH_DATA,sep=";",parse_dates=['Datum'])
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

	# create filter options
	############## Einnahmen - Ausgaben Filter ##############
	filter_money = filter_col1.radio('Nach welchen Typen soll gefiltert werden?',types_of_moneyflow)
	if filter_money != 'Alles anzeigen':
		df = df[df.Typ == filter_money]
	############## Konto Filter ##############
	filter_konto = filters_col2.radio('Nach welchem Konto soll gefiltert werden?', types_of_accounts)
	if filter_konto != 'Alle Konten':
		df = df[df.Konto == filter_konto]

	df_copy = df.copy()
	df_copy.Betrag = df_copy.Betrag.str.replace('.','').str.replace(',','.').astype('float')

	num_categories = st.number_input('Wie viele Katogrien sollen angezeigt werden?',min_value=1,max_value=len(df_copy.Kategorie.unique()),value=len(df_copy.Kategorie.unique())//2)

	df_grouped_by_categories = df_copy.groupby(['Kategorie']).sum().sort_values('Betrag',ascending=False).iloc[:num_categories]
	df_grouped_by_categories['Prozentanteil'] = abs(df_grouped_by_categories.Betrag / df_grouped_by_categories.Betrag.sum())
	if any(df_grouped_by_categories.Prozentanteil < 0.05):
		df_grouped_by_categories = df_grouped_by_categories[['Prozentanteil']][df_grouped_by_categories.Prozentanteil > 0.05]
		df_grouped_by_categories.loc['Sonstiges'] = 1 - df_grouped_by_categories.Prozentanteil.sum()

	labels = list(df_grouped_by_categories.index)
	sizes = df_grouped_by_categories.Prozentanteil.tolist()
		#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')


	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	st.pyplot(fig1)

	num_elems = st.slider('Wie viele Zeilen sollen betrachtet werden', 0, len(df), len(df)//5 if len(df)>100 else len(df))
	df['Betrag'] = df.Betrag + ' €'
	st.dataframe(df.sort_values('Datum',ascending=False).iloc[:num_elems])
