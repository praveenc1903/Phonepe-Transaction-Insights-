import webbrowser
import streamlit as st
import threading
import time
import os
import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import mysql.connector
import streamlit as st
from PIL import Image
import base64
# ================       /     IMPORT LIBRARY    /      =================== #

# [clone libraries]
import requests
import subprocess

# [pandas, numpy and file handling libraries]
import pandas as pd
import numpy as np
import os
import json

# [SQL libraries]
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
import mysql

# [Dash board libraries]
import streamlit as st
import plotly.express as px
import psycopg2
import plotly.graph_objects as go
from streamlit_option_menu import option_menu





mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Praveen@1932000",
        auth_plugin="mysql_native_password"
    )
cursor = mydb.cursor()

cursor.execute("use phonepe_pulse")
# Clear again before next query




while cursor.nextset():
    pass
#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
#.commit()
table1 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

# Clear again before next query
while cursor.nextset():
    pass
    
#Aggregated_user
cursor.execute("select * from aggregated_user")
#.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

# Clear again before next query
while cursor.nextset():
    pass
    
#Map_insurance
cursor.execute("select * from map_insurance")
#.commit()
table9 = cursor.fetchall()

Map_insurance = pd.DataFrame(table9,columns = ("States", "Years", "Quarter", "District", "Transaction_count","Transaction_amount"))

# Clear again before next query
while cursor.nextset():
    pass
    
#Map_transaction
cursor.execute("select * from map_transaction")
#.commit()
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
#.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "District", "RegisteredUser", "AppOpens"))

#Top_insurance
cursor.execute("select * from top_insurance")
#.commit()
table5 = cursor.fetchall()
Top_insurance = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
cursor.execute("select * from top_transaction")
#.commit()
table6 = cursor.fetchall()
Top_transaction = pd.DataFrame(table6,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
#.commit()
table7 = cursor.fetchall()
Top_user = pd.DataFrame(table7, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


#Aggregated_insurance
cursor.execute("select * from aggregated_insurance;")
#.commit()
table8 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
import uuid

def Aggre_insurance_Y(df,year,context_id=None):
    if context_id is None:
        context_id = uuid.uuid4().hex[:6]

    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=400, height= 600, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount,use_container_width=True, key=f"bar_amount_{year}_{context_id}")
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=400, height= 600, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count ,use_container_width=True, key=f"bar_count_{year}_{context_id}")

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Cividis",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =400, height= 600)
        fig_india_1.update_geos(visible =False,
            resolution=50,
            showcountries=False,
            showcoastlines=False,
            showland=True,landcolor="lightgray",
            projection_scale=10)
        
        st.plotly_chart(fig_india_1,use_container_width=True,key=f"map_amount_{year}_{context_id}")

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Cividis",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =400, height= 600)
        fig_india_2.update_geos(visible =False,
            resolution=50,
            showcountries=False,
            showcoastlines=False,
            showland=True,landcolor="lightgray",
            projection_scale=10)
        


        st.plotly_chart(fig_india_2,use_container_width=True, key=f"map_count_{year}_{context_id}")

        return aiy
def Aggre_insurance_Y_Q(df, quarter, context_id=None):
    if context_id is None:
        context_id = uuid.uuid4().hex[:6]

    aiyq = df[df["Quarter"] == quarter]
    aiyq.reset_index(drop=True, inplace=True)

    aiyqg = aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_q_amount = px.bar(aiyqg, x="States", y="Transaction_amount", 
                              title=f"{aiyq['Years'].min()}  Q {quarter} TRANSACTION AMOUNT",
                              width=400, height=600,
                              color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount, use_container_width=True, key=f"q_amount_{quarter}_{context_id}")

    with col2:
        fig_q_count = px.bar(aiyqg, x="States", y="Transaction_count", 
                             title=f"{aiyq['Years'].min()}  Q {quarter} TRANSACTION COUNT",
                             width=400, height=600,
                             color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count, use_container_width=True, key=f"q_count_{quarter}_{context_id}")

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        fig_india_1 = px.choropleth(aiyqg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Cividis",
                                    range_color=(aiyqg["Transaction_amount"].min(), aiyqg["Transaction_amount"].max()),
                                    hover_name="States", title=f"{aiyq['Years'].min()}  Q {quarter} TRANSACTION AMOUNT",
                                    fitbounds="locations", width=400, height=600)
        fig_india_1.update_geos(visible =False,
            resolution=50,
            showcountries=False,
            showcoastlines=False,
            showland=True,landcolor="lightgray",
            projection_scale=10)
        st.plotly_chart(fig_india_1, use_container_width=True, key=f"q_map_amount_{quarter}_{context_id}")

    with col2:
        fig_india_2 = px.choropleth(aiyqg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="Cividis",
                                    range_color=(aiyqg["Transaction_count"].min(), aiyqg["Transaction_count"].max()),
                                    hover_name="States", title=f"{aiyq['Years'].min()}  Q {quarter} TRANSACTION COUNT",
                                    fitbounds="locations", width=400, height=600)
        fig_india_2.update_geos(visible =False,
            resolution=50,
            showcountries=False,
            showcoastlines=False,
            showland=True,landcolor="lightgray",
            projection_scale=10)
        st.plotly_chart(fig_india_2, use_container_width=True, key=f"q_map_count_{quarter}_{context_id}")

    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 400, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 400,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)


def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=800,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=800)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(
            miysg, x="District", y="Transaction_amount",
            width=400, height=500,
            title=f"{state.upper()} DISTRICT TRANSACTION AMOUNT",
            color_discrete_sequence=px.colors.sequential.Mint_r
        )
        st.plotly_chart(fig_amount, key=f"{state}_amount_chart")

    with col2:
        fig_count = px.bar(
            miysg, x="District", y="Transaction_count",
            width=400, height=500,
            title=f"{state.upper()} DISTRICT TRANSACTION COUNT",
            color_discrete_sequence=px.colors.sequential.Mint
        )
        st.plotly_chart(fig_count, key=f"{state}_count_chart")
#chnaged 

def map_insure_plot_2(df, state):
    miys = df[df["States"] == state]
    miysg = miys.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    miysg.reset_index(inplace=True)

    # Sort by amount for better visual pie order
    miysg.sort_values(by="Transaction_amount", ascending=False, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_map_pie_1 = px.pie(
            miysg,
            names="District",
            values="Transaction_amount",
            title=f"{state.upper()} DISTRICT TRANSACTION AMOUNT",
            width=500,
            height=500,
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Mint_r
        )
        fig_map_pie_1.update_traces(textinfo='percent+label', hovertemplate="%{label}<br>₹%{value:,}<extra></extra>")
        st.plotly_chart(fig_map_pie_1, key=f"pie_amount_{state}")

    with col2:
        fig_map_pie_2 = px.pie(
            miysg,
            names="District",
            values="Transaction_count",
            title=f"{state.upper()} DISTRICT TRANSACTION COUNT",
            width=500,
            height=500,
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )
        fig_map_pie_2.update_traces(textinfo='percent+label', hovertemplate="%{label}<br>%{value:,} Txns<extra></extra>")
        st.plotly_chart(fig_map_pie_2, key=f"pie_count_{state}")
#
#def map_insure_plot_2(df,state):
#    miys= df[df["States"] == state]
#    miysg= miys.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
#    miysg.reset_index(inplace= True)
#
#    col1,col2= st.columns(2)
#    with col1:
#        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_amount",
#                              width=500, height=500, title= f"{state.upper()} DISTRICT TRANSACTION AMOUNT",
#                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
#        st.plotly_chart(fig_map_pie_1)
#
#    with col2:
#        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_count",
#                              width=500, height= 500, title= f"{state.upper()} DISTRICT TRANSACTION COUNT",
#                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
#        
#        st.plotly_chart(fig_map_pie_1)


def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=800,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Bluyl)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 800,height=800,color_discrete_sequence= px.colors.sequential.Blugrn)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("District")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    
    fig_map_user_plot_1= px.pie(muyqsg, values= "RegisteredUser",names= "District",width=500,height=500,
                                title= f"{state.upper()} REGISTERED USER",hole=0.5,
                                color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "Pincodes",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)




def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.Rainbow_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)


def ques4():
    htd= Map_transaction[["District", "Transaction_amount"]]
    htd1= htd.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.bar(htd2, x= "Transaction_amount", y= "District", title="TOP 10 DISTRICT OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Reds)
    return st.plotly_chart(fig_htd)

def ques5():
    htd= Map_transaction[["District", "Transaction_amount"]]
    htd1= htd.groupby("District")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.bar(htd2, x= "Transaction_amount", y= "District", title="TOP 10 DISTRICT OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Reds)
    return st.plotly_chart(fig_htd)


def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.pie(sa2, names= "States", values= "AppOpens", title="Top 10 States With Phonepe users",hole=0.5,
                color_discrete_sequence= px.colors.sequential.Rainbow_r)
    return st.plotly_chart(fig_sa)

def ques7():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.pie(sa2, names= "States", values= "AppOpens", title="lowest 10 States With Phonepe users",hole=0.5,
                color_discrete_sequence= px.colors.sequential.Rainbow_r)
    return st.plotly_chart(fig_sa)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)


def ques10():
    dt= Map_transaction[["District", "Transaction_amount"]]
    dt1= dt.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "District", y= "Transaction_amount", title= "DISTRICT WITH HIGHEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Viridis)
    return st.plotly_chart(fig_dt)


#-------------------------------------------------Streamlit part---------------------------------------------------------------------->


st.set_page_config(layout="wide")


st.markdown("""
    <style>
    .title-3d {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        text-shadow:
            2px 2px 0 #ff6600,
            4px 4px 0 #000000;
        margin-bottom: 1rem;
    }
    </style>

    <h1 class="title-3d">
        <span style="color: orange;">PHONEPE</span> DATA VISUALIZATION AND EXPLORATION
    </h1>
""", unsafe_allow_html=True)



# Sidebar Navigation Menu
with st.sidebar:
    select = option_menu(
        "Main Menu",
        ["Home", "Data Exploration", "Top Charts"],
        icons=["house", "bar-chart", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#141414"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#e50914",
                "color": "white"
            },
            "nav-link-selected": {
                "background-color": "#e50914",
                "font-weight": "bold",
                "color": "white"
            },
        },
    )
if select == "Home":
    st.markdown("""
    <style>
        body {
            background-color: #141414;
            color: #fff;
        }
        .header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #e50914, #b00710);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .header h1 {
            font-size: 3.5rem;
            font-weight: bold;
            color: #fff;
        }
        .header p {
            font-size: 1.2rem;
            color: #f5f5f1;
            margin-top: 0.5rem;
        }
        .features {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 1rem;
        }
        .feature-card {
            background: #1f1f1f;
            border-left: 5px solid #e50914;
            border-radius: 8px;
            padding: 1rem;
            width: 48%;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 1rem;
        }
        .feature-card p {
            font-size: 1rem;
            color: #f5f5f1;
        }
        .download-btn {
            display: inline-block;
            background-color: #e50914;
            color: white !important;
            font-weight: bold;
            padding: 14px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.1rem;
            margin: 30px auto;
        }
        .download-btn:hover {
            background-color: #b00710;
        }
        .video-wrapper {
            text-align: center;
            margin: 2rem 0;
        }
        .video-title {
            font-size: 1.8rem;
            margin-bottom: 1rem;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---- HEADER SECTION ----
    st.markdown("""
    <div class="header">
        <h1>PHONEPE</h1>
        <p>INDIA'S BEST TRANSACTION APP</p>
        <p>INDIA'S DIGITAL PAYMENT PLATFORM</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- FEATURES SECTION ----
    st.markdown('<div class="features">', unsafe_allow_html=True)
    features = [
        "✓ 100% Secure and Lightning Fast",
        "✓ Instant Money Transfer",
        "✓ Transfer Money up to ₹1 Lakh Daily",
        "✓ Banking Services 24/7",
        "✓ UPI Payments & More",
    ]
    for f in features:
        st.markdown(f"""
        <div class="feature-card">
            <p>{f}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- DOWNLOAD BUTTON ----
    st.markdown("""
    <div style='text-align: center;'>
        <a class='download-btn' href='https://www.phonepe.com/app-download/' target='_blank'>
            DOWNLOAD THE APP NOW
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ---- VIDEO SECTION ----
    st.markdown("""
    <div class='video-wrapper'>
        <div class='video-title'>📹 How PhonePe Works</div>
        <iframe width="100%" height="480" src="https://www.youtube.com/embed/xhZ82fUWJ6g"
        frameborder="0" allowfullscreen></iframe>
    </div>
    """, unsafe_allow_html=True)
#--------------------------------------------2nd---------------------------------------------------------
#changed 
if select == "Data Exploration":
    # CSS for styling tabs and radio buttons with corrected spacing
    st.markdown("""
    <style>
        /* TABS */
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #1f1f1f;
            border-radius: 5px 5px 0 0;
            padding: 12px 20px;
            margin-right: 6px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #e50914;
            color: white;
        }

        /* RADIO GROUP CONTAINER */
        .stRadio > div {
            background-color: #1c1c1c;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }

        /* RADIO LABELS */
        label[data-testid="stRadioLabel"] {
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
        }

        /* RADIO OPTIONS HOVER EFFECT */
        [data-testid="stRadio"] div[role="radiogroup"] label:hover {
            color: orange;
        }

        /* BODY BACKGROUND FIX (optional, if needed) */
        .main {
            padding-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Tabs Section
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        st.markdown("### 📊 Aggregated Analysis", unsafe_allow_html=True)
        method = st.radio("**Select the Analysis Method**", [
            "Insurance Analysis",
            "Transaction Analysis",
            "User Analysis"
        ])


        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.selectbox("**Select the Year**", Aggre_insurance["Years"].unique())

            df_agg_insur_Y= Aggre_insurance_Y(Aggre_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.selectbox("**Select the Quarter**", df_agg_insur_Y["Quarter"].unique())

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)

            
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.selectbox("**Select the Year_ta**", Aggre_transaction["Years"].unique())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.selectbox("**Select the Quarter_ta**", df_agg_tran_Y["Quarter"].unique())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            

            state_Y_Q= st.selectbox("**Select the State_ta**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)


        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_au",Aggre_user["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Aggre_user,year_au)

            quarter_au= st.selectbox("Select the Quarter_au",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_au**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)
    with tab2:
        st.markdown("### 🗺️ Map Analysis", unsafe_allow_html=True)

        method_map = st.radio("**Select the Analysis Method (MAP)**", [
            "Map Insurance Analysis",
            "Map Transaction Analysis",
            "Map User Analysis"
        ])
#changed 
        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.selectbox("**Select the Year_mi**", Map_insurance["Years"].unique())

            df_map_insur_Y= Aggre_insurance_Y(Map_insurance,years_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.selectbox("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].unique())

            df_map_insur_Y_Q= Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State_mi", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_District_Analyse", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)

        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.selectbox("**Select the Year_mt**", Map_transaction["Years"].unique())

            df_map_tran_Y= Aggre_insurance_Y(Map_transaction, years_m2)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.selectbox("**Select the Quarter_mt**", df_map_tran_Y["Quarter"].unique())

            df_map_tran_Y_Q= Aggre_insurance_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_mt", df_map_tran_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_tran_Y_Q, state_m4)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_District_Analyse_mt", df_map_tran_Y["States"].unique())

            map_insure_plot_1(df_map_tran_Y,state_m3)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_user["Years"].unique())
            map_user_Y= map_user_plot_1(Map_user, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)
    with tab3:
        st.markdown("### 🔝 Top Analysis", unsafe_allow_html=True)
        method_top = st.radio("**Select the Analysis Method (TOP)**", [
            "Top Insurance Analysis",
            "Top Transaction Analysis",
            "Top User Analysis"
        ])
        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.selectbox("**Select the Year_ti**", Top_insurance["Years"].unique())
 
            df_top_insur_Y= Aggre_insurance_Y(Top_insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.selectbox("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].unique())

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.selectbox("**Select the Year_tt**", Top_transaction["Years"].unique())
 
            df_top_tran_Y= Aggre_insurance_Y(Top_transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.selectbox("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].unique())

            df_top_tran_Y_Q= Aggre_insurance_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_user["Years"].unique())

            df_top_user_Y= top_user_plot_1(Top_user,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)


#if select == "Top Charts":
#
#    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount','States With Highest Trasaction Amount',
#                                  'District With Highest Transaction Amount','District With Lowest Transaction Amount',
#                                  'Top 10 States With Phonepe users','Least 10 States With Phonepe users','States With Lowest Trasaction Count',
#                                 'States With Highest Trasaction Count',
#                                 'Top 50 District With Highest Transaction Amount'))
#    
#    if ques=="Top Brands Of Mobiles Used":
#        ques1()
#
#    elif ques=="States With Lowest Trasaction Amount":
#        ques2()
#
#    elif ques=="States With Highest Trasaction Amount":
#        ques3()
#
#    elif ques=="District With Highest Transaction Amount":
#        ques4()
#
#    elif ques=="District With Lowest Transaction Amount":
#        ques5()
#
#    elif ques=="Top 10 States With Phonepe users":
#        ques6()
#
#    elif ques=="Least 10 States With Phonepe users":
#        ques7()
#
#    elif ques=="States With Lowest Trasaction Count":
#        ques8()
#
#    elif ques=="States With Highest Trasaction Count":
#        ques9()
#
#
#    elif ques=="Top 50 District With Highest Transaction Amount":
#        ques10()

if select == "Top Charts":
    st.markdown("""
        <style>
        .top-charts-container {
            background-color: #1c1c1c;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 0 8px rgba(229, 9, 20, 0.2);
            margin-top: 1rem;
            animation: fadeIn 0.8s ease-in-out;
        }

        .top-charts-title {
            color: #ffffff;
            font-size: 2.2rem;
            font-weight: 800;
            text-shadow: 0 0 4px #e50914;
            margin-bottom: 1.5rem;
        }

        .stSelectbox > div {
            background-color: #262626 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.4rem !important;
            box-shadow: 0 0 0 1px rgba(229, 9, 20, 0.3);
        }

        .stSelectbox > div:hover {
            box-shadow: 0 0 6px #e50914;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    #st.markdown("<div class='top-charts-container'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background-color: #e50914;
        padding: 10px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        margin-bottom: 30px;
    ">
        <h2 style="color: white; font-weight: bold; font-size: 2rem; margin: 0;">
            🔝 Top Charts Analysis
        </h2>
    </div>
    """, unsafe_allow_html=True)
    ques = st.selectbox("**Select the Question**", (
        'Top Brands Of Mobiles Used',
        'States With Lowest Trasaction Amount',
        'States With Highest Trasaction Amount',
        'District With Highest Transaction Amount',
        'District With Lowest Transaction Amount',
        'Top 10 States With Phonepe users',
        'Least 10 States With Phonepe users',
        'States With Lowest Trasaction Count',
        'States With Highest Trasaction Count',
        'Top 50 District With Highest Transaction Amount'
    ))
    # Render the result inside the container
    if ques == "Top Brands Of Mobiles Used":
        ques1()
    elif ques == "States With Lowest Trasaction Amount":
        ques2()
    elif ques == "States With Highest Trasaction Amount":
        ques3()
    elif ques == "District With Highest Transaction Amount":
        ques4()  # Important this is inside the container
    elif ques == "District With Lowest Transaction Amount":
        ques5()
    elif ques == "Top 10 States With Phonepe users":
        ques6()
    elif ques == "Least 10 States With Phonepe users":
        ques7()
    elif ques == "States With Lowest Trasaction Count":
        ques8()
    elif ques == "States With Highest Trasaction Count":
        ques9()
    elif ques == "Top 50 District With Highest Transaction Amount":
        ques10()
    st.markdown("</div>", unsafe_allow_html=True)  # Make sure this closes the box

st.markdown("""
<style>
.footer-banner {
    background: linear-gradient(135deg, #e50914, #b0060f);
    padding: 20px;
    margin-top: 4rem;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7);
    text-align: center;
}
.footer-banner h2 {
    color: white;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    margin: 0;
}
.footer-banner p {
    margin-top: 10px;
    color: #ffe6e6;
    font-size: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
</style>

<div class="footer-banner">
    <h2>📊 Report Submitted by Praveen</h2>
    <p>© 2025 All Rights Reserved | Designed with Streamlit</p>
</div>
""", unsafe_allow_html=True)


#def open_browser():
#    time.sleep(1)  # Give Streamlit a second to start
#    webbrowser.open_new("http://localhost:8501")
#
#if __name__ == "__main__":
#    threading.Thread(target=open_browser).start()
#    os.system("Phonepe.py")  
