import streamlit as st
import pandas as pd

# create page title
st.title('Personal Finanz Tracker')
st.header('Übersicht und Zusammenfassung von Vermögen')

def render_web_data(total_flatex_value, absolute_profit, total_raiffeisen_giro_value, total_raiffeisen_creditcard_value):
	
	# display values via metrics
	col1, col2, col3 = st.columns(3)
	col1.metric(label="Flatex Total Value", value=total_flatex_value + " €", delta=absolute_profit + " €")
	col2.metric(label='Raiffeisen Giro Total Value', value = total_raiffeisen_giro_value + " €")
	col3.metric(label='Raiffeisen Creditcard Total Value', value = total_raiffeisen_creditcard_value + " €")

def render_df(PATH_DATA):

	# read in data and extract date information
	df = pd.read_csv(PATH_DATA,sep=";",parse_dates=['Datum'])
	df['Betrag'] = df.Betrag.str.replace('.','').str.replace(',','.').astype('float')
	df['Tag'] = df.Datum.dt.day
	df['Monat'] = df.Datum.dt.month
	df['Jahr'] = df.Datum.dt.year
	df = df[df.Jahr == 2021]

	option = st.selectbox(
	     'Wonach soll gefiltert werden?',
	     ('Datum', 'Kategorie'))

	if option == 'Datum':
	    num_elems = st.slider('Wie viele Zeilen sollen betrachtet werden', 0, len(df), 50)
	    st.dataframe(df.sort_values('Datum',ascending=False).iloc[:num_elems])
	    #df_by_day = df.groupby(['Monat']).sum()
	else:
	    df_by_category = df.groupby('Kategorie').sum()
	    st.bar_chart(df_by_category.sort_values('Betrag',ascending=False)['Betrag'])
