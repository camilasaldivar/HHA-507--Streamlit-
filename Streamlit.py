#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 07:00:43 2021

@author: camilasaldivar
"""

import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.graph_objects as go



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('AHI STREAMLIT APP DEPLOYMENT')




    
    
#LOADER BAR TO STIMULATE LOADING    
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.1)
     my_bar.progress(percent_complete + 1)




primaryColor="#6eb52f"
backgroundColor="#f0f0f5"
secondaryBackgroundColor="#e0e0ef"
textColor="#262730"
font="sans serif"
  

st.write('Welcome, *Everyone!* :sunglasses:')

color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)
  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()


st.header('Hospital Dataframe:')

st.markdown('The dataframe below shows information regarding hospitals')
st.dataframe(df_hospital_2)




st.subheader('Hospital Type')
bar1 = df_hospital_2['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)
st.caption('The above chart displays the type of hospitals found within this dataframe')

st.subheader('Pie Chart of Hospital Type')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

st.subheader('Pivot Table Capturing the Rating for All Hospitals Using the Parameters of Hospital Ownership and Hospital Type')
dataframe_pivot = df_hospital_2.pivot_table(index=['hospital_ownership','hospital_type'],values=['hospital_overall_rating'],aggfunc='count')
st.dataframe(dataframe_pivot)

hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']

hospitals_tx = df_hospital_2[df_hospital_2['state'] == 'TX']


st.subheader('Map of NY Hospital Locations')
hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'})  
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])
st.map(hospitals_ny_gps)


#Bar Chart
st.subheader('Hospital Type in New York')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.caption('Most of the hospitals in the New York area are acute care, followed by psychiatric')


st.subheader('Visual Representation:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)
st.caption('The pie chart above shows the different hospital types in the New York Area, with 75.4% being acute care hospitals')



#Timeliness of Care
st.subheader('NY Hospitals - Timeliness of Care')
bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.caption('Based on the above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')


st.subheader('TX Hospitals - Timeliness of Care')
bar4 = hospitals_tx['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig5 = px.bar(bar4, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig5)
st.caption('Based on the bar chart above, we can see the the timeliness of care data for the majority of hospitals in the Texas area is not available and for 127 hospitals is the same as the national average')



st.markdown('Hospital Q: What is the most common hospital type in NY & and where do NY hospitals fall in regards to timeliness of care?')
st.markdown('As shown by the analysis above, the most common hospital type in NY is acute care (144 acute care hospitals). Most of New York Hospitals are below national average in regards to timeliness of care(103 hospitals)') 

#Drill down into INPATIENT and OUTPATIENT 
st.title('INPATIENT dataframe')
st.markdown('The dataframe displayed below is for the Inpatient facility')

st.subheader('Inpatient Facility')
bar7 = df_inpatient_2['provider_state'].value_counts().reset_index()
st.dataframe(bar7)

st.subheader('Bar Chart of Inpatient Facilities by state')
fig7 = px.bar(bar7, x='index', y='provider_state')
st.plotly_chart(fig7)



inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.subheader('Discharges')
st.markdown('Total Count of Discharges from Inpatient Captured: ' )
st.markdown( str(total_inpatient_count) )





##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.subheader('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.columns(2)

col1.subheader('Top 10 DRGs')
col1.dataframe(top10)

col2.subheader('Bottom 10 DRGs')
col2.dataframe(bottom10)




#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.subheader('COSTS')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Hospital Costs by Provider and Average Total Payments ")
st.dataframe(costs_sum)
with st.expander("See explanation"):
     st.write("""
         This table shows the total sum of the payments made to each provider.
     """)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)


st.markdown('Inpatient Q: Which is the hospital with the highest total payments in the NY area?')
st.markdown('Inpatient A: The hospital with the highest total payment in NY is New York Prebysterian Hospital with an average total payments of 10.54512M')

st.title('OUTPATIENT Dataframe')

st.subheader('Outpatient providers in the state of Texas')

outpatient_tx = df_outpatient_2[df_outpatient_2['provider_state'] == 'TX']

bar2 = outpatient_tx['provider_name'].value_counts().reset_index()
st.dataframe(bar2)
st.caption('The most common outpatient facility in the state of Texas is Scott & White Medical Center - Temple, followed by Mother Frances Hospital ')

st.subheader('Bar chart displaying different outpatient providers in Texas:')
fig3 = px.bar(bar2, x='index', y='provider_name')
st.plotly_chart(fig3)
with st.expander("See explanation"):
     st.write("""
         The chart is a visual representation that includes all of the outpatient facilities in Texas.
     """)


st.subheader('Outpatient providers in the state of New York')

outpatient_tx = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']

bar3 = outpatient_tx['provider_name'].value_counts().reset_index()
st.dataframe(bar3)
st.caption('The most common outpatient provider in the state of New York is Mary Imogene Bassett Hospital')

st.subheader('Bar chart displaying different outpatient providers in New York:')
fig4 = px.bar(bar3, x='index', y='provider_name')
st.plotly_chart(fig4)
with st.expander("See explanation"):
     st.write("""
         The chart above shows various outpatient facilities in New York.
     """)
        
st.markdown('Outpatient Q: Which are the most common outpatient facilities in NY and TX?')
st.markdown('Mary Imogene Bassett Hospital and Scott & White Medical Center respectively') 


hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
st.dataframe(filtered)

st.header('Merging datasets for SBU and CEMC Hopsital values')
st.markdown('Merging of Datasets to show SBU Hospital values')
df_hospital_2['provider_id'] = df_hospital_2['provider_id'].astype(str)
df_outpatient_2['provider_id'] = df_outpatient_2['provider_id'].astype(str)
df_merged = df_outpatient_2.merge(df_hospital_2, how='left', left_on='provider_id', right_on='provider_id')

st.dataframe(df_merged)
st.markdown('Cleaning of df_merge')
df_merged_clean = df_merged[df_merged['hospital_name'].notna()]
st.dataframe(df_merged_clean)

st.header('Stony Brook University Hospital dataset')
df_merged_clean_SB = df_merged_clean[df_merged_clean['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
df_merged_clean_SB

st.header('Carolina East Medical Center')
df_merged_clean_CEMC = df_merged_clean[df_merged_clean['hospital_name'] == 'CAROLINA EAST MEDICAL CENTER']
df_merged_clean_CEMC

st.header('Comparison of CEMC and SBU Hospitals')
final_df_comparison = pd.concat([df_merged_clean_CEMC, df_merged_clean_SB])
st.dataframe(final_df_comparison)

st.subheader('Final Comparison Pivot Table')
dataframe_pivot = final_df_comparison.pivot_table(index=['hospital_name','apc'],values=['average_total_payments'],aggfunc='mean')
st.dataframe(dataframe_pivot)

bar2 = final_df_comparison['hospital_name'].value_counts().reset_index()
st.subheader('Bar chart displaying SBU and CEMC differences between average total payments')
fig3 = px.bar(bar2, x='index', y='hospital_name')
st.plotly_chart(fig3)
st.dataframe(bar2)
st.markdown('Showing the total difference between average total payments between CEMC and SBU hospitals.')
st.markdown('SBU Hospital Question: What is the difference between total payment for Stony Brook Hospital compared to another hospital from a different state?')
st.markdown('SBU Hospital Answer: The total average payments between Stony Brook University hospital and Carolina East Medical Center(CEMC) as we can also see CEMC is a government- Hospital District or Authority and Stony Brook ownership is by Government-state.') 
st.markdown('Here we can see Stony Brook Hospital has 0 apcs for 0012, 0015 debridment compared to CEMC, and we see that Stony Brook University Hospital from this pivot table has higher cost of average total payments with Endoscopy upper airway compared to CEMC with approximately 6588 compared to Stony Brook 8645.')

st.subheader('Pivot APC for SBU Hospital')
dataframe_pivot = df_merged_clean_SB.pivot_table(index=['provider_id','apc'],values=['average_total_payments'],aggfunc='mean')
st.dataframe(dataframe_pivot)
st.markdown('SBU Hospital Q: What are the most expensive apc for SBU Hopsital?')
st.markdown('SBU Answer:The most expensive average total cost for APC in the outpatient and hospital dataframe with SBU hospital are the following')
st.markdown('1. Level IV endoscopy 2307.21, 2. Level IV Nerver Injections 1325.64, 3. Level II Cardiac Imaging 1300.67')

st.header('Merging of Hospital and Inpatient data sets')
df_hospital_2['provider_id'] = df_hospital_2['provider_id'].astype(str)
df_inpatient_2['provider_id'] = df_inpatient_2['provider_id'].astype(str)
df_merged2 = df_inpatient_2.merge(df_Hospital_2, how='left', left_on='provider_id', right_on='provider_id')
df_merged_clean2 = df_merged2[df_merged2['hospital_name'].notna()]
df_merged_clean_SB2 = df_merged_clean2[df_merged_clean2['provider_id'] == '330393']
df_merged_clean_SB2

st.header('Pivot table for average cost of each DRG for SBU Hospital')
st.subheader('Pivot DRG for SBU Hospital')
dataframe_pivot = df_merged_clean_SB2.pivot_table(index=['provider_name','drg_definition'],values=['average_total_payments'],aggfunc='mean')
st.dataframe(dataframe_pivot)

st.markdown('SBU Hospital Inpatient Q: What are the most expesive drugs comparing Stony Brook average total payments for DRG?')
st.markdown('SBU Answer: 1. ECMO or TRACH - $216636.88, 2. Trach W MV - $132951.87, 3. Cranio W Major Dev - $69981.35.')
st.markdown('All three have the most expensive total average payments for drg_definition with df_Hospital and df_Inpatient')
           

