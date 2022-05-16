# --- IMPORT DEPENDANCIES ---
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# --- SET UP STREAMLIT TEXTS ---
st.set_page_config(page_title='GRDP Analytics',
                   page_icon=":bar_chart",
                   layout="wide")

st.title('Philippine GRDP Dashboard')
st.caption('Gross Regional Domestic Product by Industry of all regions in the Philippines | At Current Prices')

st.sidebar.header('Selection Pane')

# --- GET DESIRED REGION AND INDUSTRIES OF THE USER TO EXPLORE ---
user_region_choice = st.sidebar.selectbox('Select a region:',('Region I',
 'Region II',
 'Region III',
 'CAR',
 'NCR',
 'Region IVA',
 'Region IVB',
 'Region V',
 'Region VI',
 'Region VII',
 'Region VIII',
 'Region IX',
 'Region X',
 'Region XI',
 'Region XII',
 'Region XIII',
 'ARMM'))

user_industries_choice = st.sidebar.multiselect('Select Industry/Industries:',
        ['Agriculture, Forestry and Fishing', 
        'Production',
        'Mining and Quarrying', 
        'Manufacturing',
        'Electricity, Steam, Water and Waste Management', 
        'Construction',
        'Services',
        'Wholesale and Retail Trade: Repair of Motor Vehicles and Motorcycles',
        'Transportation and Storage',
        'Accomodation and Food Service Activities',
        'Information and Communication', 
        'Financial and Insurance Activities',
        'Real Estate and Ownership of Dwellings',
        'Professional and Business Services',
        'Public Administration and Defense: Compulsory Social Activities',
        'Education', 
        'Human Health and Social Work Activities',
        'Other Services'])

st.sidebar.markdown('---')

st.sidebar.caption('''

The creator of this page gives credits or acknowledgement to Philippine Statistics Authority (PSA) as the data used in this project are from their database.

Terms of use of PSA clearly stated that:

"The statistical tables (or datasets) including documents (collectively as material) on this site are classified under Open Data with Creative Commons Attribution License (cc-by). This means that you are free to share (copy and redistribute) the material in any medium or format; remix, transform and build upon the material without any restrictions other than proper source attribution:"

The project's Raw Data used can be found in the folder entitled 'Raw_Extracted_Data' in the GitHub Repository of this project. Those are the files formatted in excel (xlsx).

Data Source: https://openstat.psa.gov.ph/Database/Gross-Regional-Domestic-Product


**_John_ _Paul_ _M._ _Curada,_ _Aspiring_ _Data_ _Scientist_**



''')

# --- READ THE DATA OF THE SELECTED REGION AND INDUSTRIES ---
df = pd.read_excel('All_Regions_GRDP.xlsx', sheet_name=user_region_choice, engine='openpyxl')
df.rename(columns={'Unnamed: 0':'Year'},inplace=True)


# --- ORGANIZE FUNCTIONS ---
def compare_chart_industries(df, user_industries_choice):
    fig = go.Figure()
    for choice in user_industries_choice:
        fig.add_trace(go.Scatter(x= df['Year'].values, y=df[choice].values, name=choice, mode='lines+markers',
                                 line=dict(width=3)))


    fig = fig.update_layout(title=f'GRDP of Selected Industries of {user_region_choice} from 2000 - 2001',xaxis_title='Year',yaxis_title='Amount in Peso (₱)')
    return st.plotly_chart(fig, use_container_width=True)

def GDP_bar_chart(df):
    fig = px.bar(df, x='Year', y='Gross Domestic Product')
    show_fig = st.plotly_chart(fig, use_container_width=True)
    return show_fig

def find_min_gdp_column_year(df):

    # find the lowest value in df
    lowest_ind_grdp = min([min(df[col].values) 
                            for col in df.columns
                            if col != 'Year'
                            if col != 'Gross Domestic Product'])

    # find the column that has the minimum value
    lowest_ind_grdp_column = [col
                       for col in df.apply(lambda row: row[row == lowest_ind_grdp].index.tolist() , axis=1) 
                       if len(col) != 0 ][0][0] 

    # find the Index of the lowest industry gdp value
    lowest_gdp_idx = np.where(df[lowest_ind_grdp_column].values == lowest_ind_grdp)[0][0]

    # find the Year of the lowest industry gdp value
    lowest_ind_gdp_year = df['Year'][lowest_gdp_idx]
    
    return lowest_ind_grdp, lowest_ind_grdp_column, lowest_ind_gdp_year

def find_max_gdp_column_year(df):

    #find the highest value in df
    highest_ind_grdp = max([max(df[col].values) 
                            for col in df.columns
                            if col != 'Year'
                            if col != 'Gross Domestic Product'])

    # find the column that has the maximum value
    highest_ind_grdp_column = [col
                       for col in df.apply(lambda row: row[row == highest_ind_grdp].index.tolist() , axis=1) 
                       if len(col) != 0 ][0][0] 

    # find the Index of the lowest industry gdp value
    highest_gdp_idx = np.where(df[highest_ind_grdp_column].values == highest_ind_grdp)[0][0]

    # find the Year of the lowest industry gdp value
    highest_ind_gdp_year = df['Year'][highest_gdp_idx]
    
    return highest_ind_grdp, highest_ind_grdp_column, highest_ind_gdp_year



# --- SHOW THE Lowest GRDP of an Industry, GDP Growth Rate from 2000 to 2021, and Highest GRDP of an Industry of a the selected region ---
min_grdp, min_column, min_year = find_min_gdp_column_year(df)
max_grdp, max_column, max_year = find_max_gdp_column_year(df)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader(f'Lowest GRDP of an Industry: ')
    lowest_grdp_comma = "{:,}".format(min_grdp)
    left_column.metric(f'{min_column} Industry', f"₱{lowest_grdp_comma}", f'Year of {min_year}', delta_color="off")
    
with middle_column:
    st.subheader(f'{user_region_choice} GDP Growth Rate: ')
    gdp_growth_rate = round(((df['Gross Domestic Product'].values[-1] / df['Gross Domestic Product'].values[0]) - 1)*100, 2)
    Y2021_gdp_comma = "{:,}".format(df['Gross Domestic Product'].values[-1])
    middle_column.metric("Gross Domestic Product of 2021", f"₱{Y2021_gdp_comma}", f'{gdp_growth_rate}%')

with right_column:
    st.subheader(f'Highest GRDP of an Industry: ')
    highest_grdp_comma = "{:,}".format(max_grdp)
    right_column.metric(f'{max_column} Industry', f"₱{highest_grdp_comma}", f'Year of {max_year}',delta_color="off")

st.markdown('---')


# --- SHOW THE LINE CHART AND THE BAR CHART ---
col1, col2 = st.columns(2)
with col1:
    st.subheader('Line Chart of Selected Region and Industries')
    compare_chart_industries(df, user_industries_choice)

with col2:
    st.subheader(f'GDP Bar Chart of {user_region_choice}')
    GDP_bar_chart(df)


# --- SHOW AND LET USER DOWNLOAD THE DF IN CSV FORMAT ---
st.subheader(f'Data Frame of {user_region_choice}')
df_for_regional_data = df
for column in df_for_regional_data.columns:
    if column != 'Year':
        df_for_regional_data[column] = df_for_regional_data[column].apply(lambda x : "{:,}".format(x)) 

st.dataframe(df_for_regional_data)
@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')
csv = convert_df(df)
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name=f'{user_region_choice}_data.csv',
     mime='text/csv',
 )


 

