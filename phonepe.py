import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
import requests
from urllib.request import urlopen
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open("phonepe_logo.jpg")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide")

st.sidebar.header(":violet[**PHONEPE DASHBOARD**]")
with st.sidebar:
    selected = option_menu(menu_title = "Main Menu",
        options = ["Home","Data Analysis","Map Data"],
    icons=["house","bar-chart-line", "map","exclamation-circle"],
    menu_icon= "menu-button-wide",
    default_index=0,
    styles={"nav-link": {"font-size": "10px", "text-align": "left", "margin": "-2px", "--hover-color": "red"},
                        "nav-link-selected": {"background-color": "purple"}})
                        
# Creating connection with mysql Database
mydb = sql.connect(host="localhost",
                   user="root",
                   password="12345",
                   database= "phonepe_pulse"
                  )
mycursor = mydb.cursor(buffered=True)
                        
                        # MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Phonepe Pulse Data Visualization and Exploration]")
    st.write(" ")
    st.write(" ")
    st.title(" :violet[About PhonePe:]")
    st.markdown("PhonePe is an Indian digital payments and financial services company it is based on the Unified Payments Interface (UPI) and went live in August 2016.PhonePe is accepted as a payment option by over 3.5 crore offline and online merchant outlets, constituting 99% of pin codes in the country. The app served more than 10 crore users as of June 2018,processed 500 crore transactions by December 2019, and crossed 10 crore transactions a day in April 2022. It currently has over 44 crore registered users with over 20 crore monthly active users.PhonePe is licensed by the Reserve Bank of India for the issuance and operation of a Semi Closed Prepaid Payment system.")
    st.image("home.png")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.title(" :violet[Overview:]")
    st.markdown("In this streamlit web app you will be able to see a live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner.you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users data.")
    
# MENU 2 - DATA ANALYSIS
if selected == "Data Analysis":
    st.markdown("## :violet[Data Analysis]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    columns3,columns4= st.columns([1,1.5],gap="small")
    with columns3:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    with columns4:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District based on Total phonepe users and their app opening frequency.
                """,icon="🔍"
                )
 
    if Type == "Transactions":
        col1,col2,col3 = st.columns([5,5,5],gap="small")           
            
        with col1:
        #       st.markdown("### :violet[Aggregated]")
               mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
               df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
               fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='State Top 10',
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count':'Transactions_Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        with col2:
        #        st.markdown("### :violet[Map]")
                mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])        
                fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='District Top 10',
        #                 title='Top 10',
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count':'Transactions_Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        with col3:
        #        st.markdown("### :violet[Top]")
                mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                        names='Pincode',
                        title='Pincode Top 10',
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count':'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        #Data for users:

    if Type == "Users":
        col1,col2,col3 = st.columns([5,5,5],gap="small")           
            
        with col1:
 #               st.markdown("### :violet[Aggregated]")
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.pie(df,values = 'Avg_Percentage',
                    names = 'Brand',
                    title='Top 10 Brands',
                    color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)   

        with col2:
#                st.markdown("### :violet[District]")
                mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                fig = px.pie(df,values = 'Total_Appopens',
                        title='Top 10 District',
                        names = 'District',
                                 color='Total_Users',
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
                      
        with col3:
#                st.markdown("### :violet[Pincode]")
                mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
                fig = px.pie(df,
                                 values='Total_Users',
                                 names='Pincode',
                                 title='Top 10 Users',
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 hover_data=['Total_Users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
        
# MENU 3 - Map data
if selected == "Map Data":
    st.markdown("## :violet[Map representation of a data]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))    
    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    
    if Type == "Transactions":
        
    # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        state_names = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names.sort()
        # Create a DataFrame with the state names column
        df_state_names = pd.DataFrame({'State': state_names})
        # convert dataframe to csv file
        df_state_names.to_csv('State_trans.csv', index=False)
        
        st.markdown("## :violet[Overall State Data - Transactions Amount]")
        #Getting data from mysql for df1 value 
        mycursor.execute(f"select state, sum(Count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('State_trans.csv')
        df1.State = df2

        #Graphic map representation of the map data
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_amount',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('State_trans.csv')
        df1.Total_Transactions = df1.Total_Transactions.astype(int)
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Transactions',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART - TOP PAYMENT 
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select State for Data visualization]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
            
    # EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('State_trans.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale=px.colors.sequential.Viridis)

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox(" ",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig,use_container_width=True)

        