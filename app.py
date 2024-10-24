from typing import ValuesView
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import random
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title = "HRMIS-V", page_icon=":bar_chart:",layout="wide")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#st.title('Uber pickups in NYC')
df =  pd.read_excel(
    io="2021-23.xlsx",
    sheet_name='cases',
    skiprows= 0,
    usecols='A:N',
    nrows=10000,
)
#print(df)
#st.dataframe(df)

st.sidebar.header("Please Filter Here :")
state = st.sidebar.multiselect(
    "Select the Province :",
    options=df["State"].unique(),
    default=df["State"].unique()

)
hrcat = st.sidebar.multiselect(
    "Select the HR Cat:",
    options=df["HRCat"].unique(),
    default=df["HRCat"].unique()

)



df_selection = df.query(
    "State == @state & HRCat == @hrcat"
)



st.title(" :bar_chart: HRMIS - Violation ( Dashboard) ")
#st.markdown("#")

total_cases = len(df_selection.index)
total_vic = df_selection ['TotalV'].sum()
total_maleV = int( df_selection['MaleV'].sum())
total_femaleV = int (df_selection["FemaleV"].sum())
total_fir =  df_selection ["Fir"].where(df_selection ['Fir'] == 'Yes').count()
total_arrested = df_selection ["Arrested"].where(df_selection ['Arrested'] == 'Yes').count()

left_column , middle_column , right_column = st.columns(3)

with left_column:
    st.header("Total Cases :" f" {total_cases}")
    #st.subheader(f" {total_cases}")  

with middle_column:
   # st.header("Total Victim :"f"{total_vic}")
    st.header("Total Victim :"f"{total_maleV + total_femaleV}")

  #  st.subheader(f"{total_vic}")
    st.subheader(" :mens: Male Victim : "f"{total_maleV}")
    st.subheader(" :womens: Female Victim : "f"{total_femaleV}")
  

with right_column :
    st.header("Total FIR :"f"{total_fir}")
    #st.subheader(f"{total_fir}") 
    st.subheader("Arrested :"f"{total_arrested}")

st.markdown("---")

left_column , right_column = st.columns(2)

with left_column:
    labels = 'Male','Female'
    sizes = [total_maleV,total_femaleV]
    explode = (0,0.1)
    title="Male & Female Victim in %"
    fig1 , ax1  = plt.subplots() 
    ax1.pie(sizes, explode=explode, labels=labels , autopct='%1.01f%%',
            shadow=False, startangle=90 )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Male & Female Victim %")
    st.pyplot(fig1 )


with right_column:
    labels = 'Fir Reg','Arrested'
    sizes = [total_fir,total_arrested]
    explode = (0,0.1)
    fig1 , ax1  = plt.subplots() 
    ax1.pie(sizes, explode=explode, labels=labels , autopct='%1.01f%%',
            shadow=False, startangle=90 )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(" Reg FIR / Arrested %")
    st.pyplot(fig1 )

st.markdown("---")
st.markdown("#")

#st.dataframe(df_selection)

left_column , right_column = st.columns(2)

with left_column:

    labels = ['Punjab','Sindh', 'KPK','Balochistan']

    total_punjab_female = df_selection ["FemaleV"].where(df_selection ['State'] == 'Punjab').sum()
    total_punjab_male = df_selection ["MaleV"].where(df_selection ['State'] == 'Punjab').sum()

    total_sindh_female = df_selection ["FemaleV"].where(df_selection ['State'] == 'Sindh').sum()
    total_sindh_male = df_selection ["MaleV"].where(df_selection ['State'] == 'Sindh').sum()

    total_kpk_female = df_selection ["FemaleV"].where(df_selection ['State'] == 'KhyberPakhtunkhawa').sum()
    total_kpk_male = df_selection ["MaleV"].where(df_selection ['State'] == 'KhyberPakhtunkhawa').sum()

    total_balochistan_female = df_selection ["FemaleV"].where(df_selection ['State'] == 'Balochistan').sum()
    total_balochistan_male = df_selection ["MaleV"].where(df_selection ['State'] == 'Balochistan').sum()


    totalbar=[total_punjab_male + total_punjab_female ,total_sindh_male +total_sindh_female ,total_kpk_male + total_kpk_female ,total_balochistan_male+total_balochistan_female]
    x = np.arange(len(labels))  # the label locations
    #width = 0.25  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, totalbar , color=[ 'red', 'green', 'blue', 'cyan'])
    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_ylabel('Scores')
    ax.set_title('Number of Victims (Province Wise)')
    ax.set_xticks(x, labels)
   # ax.legend()
    ax.bar_label(rects1, padding=2)
    fig.tight_layout()
    st.pyplot(fig)


with right_column :
    labels = ['Punjab','Sindh', 'KPK','Balochistan']
    man_bar = [total_punjab_male,total_sindh_male,total_kpk_male,total_balochistan_male]
    female_bar = [total_punjab_female,total_sindh_female,total_kpk_female,total_balochistan_female]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, man_bar, width, label='Men')
    rects2 = ax.bar(x + width/2, female_bar, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_ylabel('Scores')
    ax.set_title('Number of Victims in Provinces (Gender wise)')
    ax.set_xticks(x, labels)
   # ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    st.pyplot(fig)

st.markdown("##")
st.markdown("---")
st.markdown("##")


option = st.selectbox(
     'Select the Province ',
     (state))

st.markdown("##")
#st.write('You selected:', option)


df_selection = df.query(
    "State == @option"
)

df = df_selection.groupby('District').size().reset_index(name='counts')
n = df['District'].unique().__len__()+1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)

# Plot Bars
plt.figure(figsize=(16,10), dpi= 80)
plt.bar(df['District'], df['counts'], color=c, width=.5)
for i, val in enumerate(df['counts'].values):
    plt.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':12})

# Decoration
plt.gca().set_xticklabels(df['District'], rotation=60, horizontalalignment= 'right')
plt.title("Number of Victims  in " + str(option) +  " (District Wise)", fontsize=22)
#plt.ylabel('# Vehicles')
plt.ylim(0, df['counts'].max()+10)
st.pyplot(plt)

st.markdown("##")
st.markdown("---")
st.markdown("##")



df = df_selection.groupby('HRCat').size().reset_index(name='counts')
n = df['HRCat'].unique().__len__()+1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)

# Plot Bars
plt.figure(figsize=(16,10), dpi= 80)
plt.bar(df['HRCat'], df['counts'], color=c, width=.5)
for i, val in enumerate(df['counts'].values):
            plt.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':12})

# Decoration
plt.gca().set_xticklabels(df['HRCat'], rotation=60, horizontalalignment= 'right')
plt.title("Number of Victims  in " + str(option) +  " (Violation Wise)", fontsize=22)
#plt.ylabel('# Vehicles')
plt.ylim(0, df['counts'].max()+10)
st.markdown("##")
st.pyplot(plt)


