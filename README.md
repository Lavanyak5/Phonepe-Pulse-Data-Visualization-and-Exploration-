# Phonepe-Pulse-Data-Visualization-and-Exploration-

A User-Friendly Tool to describe the data visualization and Exploration.

    PhonePe is an Indian digital payments and financial services company it is based on the Unified Payments Interface (UPI) and went live in August 2016.PhonePe is accepted as a payment option by over 3.5 crore     offline and online merchant outlets, constituting 99% of pin codes in the country. The app served more than 10 crore users as of June 2018,processed 500 crore transactions by December 2019, and crossed 10       crore transactions a day in April 2022. It currently has over 44 crore registered users with over 20 crore monthly active users.PhonePe is licensed by the Reserve Bank of India for the issuance and operation    of a Semi Closed Prepaid Payment system.

Tools Required for this Website:
      1.Plotly - (To plot and visualize the data)
      2.Pandas - (To Create a DataFrame with the scraped data)
      3.mysql.connector - (To store and retrieve the data in mysql)
      4.Streamlit - (To Create Graphical user Interface)
      5.json - (To load the json files)

Steps for loading the JSON file from repository and to convert it as csv file :

  1.Import the Libraries:
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

  2. Cloning the Data :
        1.Initially, we Clone the data from the Phonepe GitHub repository by using Python libraries. https://github.com/PhonePe/pulse.git
        2.Process the clone data by using Python algorithms and transform the processed data into DataFrame formate.
        3.Finally, create a connection to the MySQL server and create a Database and stored the Transformed data in the MySQL server.

Data Extraction code :

path1 = "C:\\Users\\machinename\\Phonepe_Pulse\\pulse\\data\\aggregated\\transaction\\country\\india\\state\\"  ---> (C:\\Users\\machinename) folder path of where you are trying to save your data.
agg_trans_list = os.listdir(path1)

columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
            'Transaction_amount': []}
for state in agg_trans_list:
    cur_state = path1 + state + "\\"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "\\"
        agg_file_list = os.listdir(cur_year)
        
        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            A = json.load(data)
            
            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))
                
df_agg_trans = pd.DataFrame(columns1)
     

  3. Extracting the data and creating data visualization Dashboard
       1. create a Dashboard by using Streamlit and applying selection and dropdown options on the Dashboard and show the output are Geo visualization, bar chart, and Dataframe Table.
       2. To create colourful and insightful dashboard I've used Plotly libraries in Python. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on a charts and map.
       3. Finally creating the Dashboard using streamlit application.



      
