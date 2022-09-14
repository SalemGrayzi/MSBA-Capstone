### Importing the required packages
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import markdown
import hydralit_components as hc
import time
from streamlit_metrics import metric, metric_row
import io
import hydralit as hy
from millify import millify
### setting page to wide automatically to avoid it being centered
st.set_page_config(layout="wide")
### Setting picture to dashboard and resizing it
st.image("https://play-lh.googleusercontent.com/qPmIH0OemtPoTXyEztnpZVW-35sEWvrw99DIX6n1sklf1mDekUxtMzyInpJlTOATsp5B",width=100)

### Building the HydraApp
app = hy.HydraApp(title='Diwan')

### Importing csv file from github onto streamlit by default, and can be used to import dataset
d1,d2,d3=st.columns(3)
with d1.expander('Upload Data'):
     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
     if uploaded_file is None:
        df= pd.read_csv('https://github.com/SalemGrayzi/status/blob/main/Statuscsv.csv?raw=true')
     else:
         df = pd.read_csv(uploaded_file)

### Filling missing values in Adress column with the mode
df['Address'] =  df['Address'].fillna('بشامون')

###Droping columns that dont add value to the analysis
df.drop(['Order No_','Phone No_','Receipt No','Company'], axis = 1, inplace = True)

### Dropping dublicates in the dataset
df.drop_duplicates(inplace=True)

### Changing Boolean values into their respectable names
df['Handheld Used'] = df['Handheld Used'].map(
                   {True:'Used PDA' ,False:"Didn't Use PDA"})
df['OnlineApp'] = df['OnlineApp'].map(
                   {True:'Application' ,False:'Phone Call'})

### changing time created into datetime with the specified format
df['Time Created'] = pd.to_datetime(df['Time Created'], format='%I:%M:%S %p')

### In the bellow section it conatains all the graphs made

###################################### Graph to get orders per day in a year
st.cache()
### Graphing the day names with a certain order and text shown on graph
Day=px.histogram(df, x= "Day Name",text_auto=True,category_orders={'Day Name':["Monday","Tuesday","Wednesday", "Thursday", "Friday", "Saturday","Sunday"]})
Day.update_layout(title="Orders per Day in a Year",xaxis_title="Day",yaxis_title="") ### adding more details on the graph

###################################### Graph to get number of order per driver
st.cache()
driver=px.histogram(df, y="Driver Name", text_auto=True) ### Plotting drivers onto a histogram with no filter 
driver.update_layout(yaxis={'categoryorder':'total ascending'}) ### plotting in ascending order
driver.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")### adding more details on the graph

#################################################################### This graph was sent into its area due to filtering reasoning
### Plotting drivers onto a histogram with no filter 
#split_size = st.slider('Top n Drivers', 0, 90, 5) ### making a slider to be used to filter the graph
#dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index() ### Grouping them then using the filter to specify how many it should show
#dfd.columns = ['Driver Name', 'count'] ### adding the columns to the values returned previously 
#drv = px.bar(dfd, y='Driver Name', x = 'count') ### plotting the graph 

###################################### Graph to find the percent of PDA usage
st.cache()
vt=df['Handheld Used'].value_counts() ### Counting each distinct variable
vts=df['Handheld Used'].value_counts().index ### Finding the index position of an the variable
pda=go.Figure(data=[go.Pie(labels=vts, values=vt, pull=[0.2, 0])]) ### Plotting it in a pie chart and adding the seperate factor using pull
pda.update_traces(textposition='inside', textinfo='percent+label') ### Adding text and percentage inside the graph
pda.update_layout(title="Percent of PDA Usage") ### Cahnging title 
### For dynamic text purposes 
hp,hp1 = (df['Handheld Used'].value_counts() /
                      df['Handheld Used'].value_counts().sum()) * 100

###################################### Order status depending on which order method was used
st.cache()
### using seaborn to plot this 
gh = sns.catplot(
    data=df, kind="count",
    x="Status", hue="Handheld Used",
     palette=['tab:red', 'tab:blue'], alpha=.6, height=6,order=df['Status'].value_counts().index
)
gh.fig.suptitle("Order Status with Usage of PDA") ### changing the title
gh.set_axis_labels(x_var="Order Status", y_var="") ### changing the x and y axis labels

###################################### A graph illustrating which picker is using a PDA
st.cache()
### using seaborn to plot this 
pdapicker = sns.catplot(
    data=df, kind="count",
    y="PickerName", hue="Handheld Used",
     palette=['tab:blue', 'tab:red'], alpha=.6,height=6,order=df['PickerName'].value_counts().index
)
pdapicker.set(title ="Usage of PDA per Picker", ylabel='Picker') ### changing the x and y axis labels

###################################### Fidning the percentage of order status based on each picker
st.cache()
stpk = px.histogram(df, y="PickerName", color="Status",barnorm = "percent",hover_data=["Status"])
stpk.update_layout(yaxis={'categoryorder':'total ascending'}) ### plotting in ascending order
stpk.update_layout(title="Picker's Percentage of Order Status",xaxis_title="Percentage",yaxis_title="Picker") ### adding more details on the graph

###################################### Percentage of revenue based on order methods
st.cache()
### Graphing orders methods based on order being delivered
onmount=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df.loc[df['Status'] == 'Delivered'].Amount, pull=[0.2, 0])]) ### Plotting it in a pie chart and adding the seperate factor using pull
onmount.update_traces(textposition='inside', textinfo='percent+label') ### Adding text and percentage inside the graph
onmount.update_layout(title="Revenue of Ordering Method") ### Changing title 

###################################### Percentage of lost sales based on order methods
st.cache()
### Graphing orders methods based on order being canceled
onmount2=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df.loc[df['Status'] == 'Canceled'].Amount, pull=[0.2, 0])]) ### Plotting it in a pie chart and adding the seperate factor using pull
onmount2.update_traces(textposition='inside', textinfo='percent+label') ### Adding text and percentage inside the graph
onmount2.update_layout(title="Lost Sales of Ordering Method") ### Changing title 
### For dynamic text purposes
os,os1 = (df.groupby('OnlineApp')['Status'].count() /
                      df['OnlineApp'].value_counts().sum()) * 100

#################################################################### This graph was sent into its area due to filtering reasoning
### slider for filtering in graph 
#n_size = st.sidebar.slider('Top n Customers', 0, 90, 5)
#dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size) ### from slider number its shows the desired ones by grouping 
#amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"])) ### graphing them
#amc=px.histogram(data_frame=dfna, x='Amount', y='Name')

###################################### ORder status based on order methods
st.cache()
sto=px.histogram(df, y="Status", color="OnlineApp",text_auto=True) ### Plotting with values shown on the graph
sto.update_layout(title="Status of Order per Ordering Method",xaxis_title="",yaxis_title="Status of Order") ### adding more details onto the graph

###################################### Time of incoming orders in a day
st.cache()
dfds = df.groupby(['Time Created']).size().to_frame().reset_index() ### Grouping them to get count and its variables
dfds.columns = ['Time Created', 'count'] ### adding the columns to the values returned previously 
tc = px.line(dfds, x='Time Created', y= 'count') ### plotting the graph 
tc.update_layout(title="Time Created of Orders",xaxis_title="Time in 24 Hour Format",yaxis_title="") ### adding more details onto the graph

###################################### Time it takes for an order to deploy
st.cache()
dfds1 = df.groupby(['Time to deploy']).size().to_frame().reset_index() ### Grouping them to get count and its variables
dfds1.columns = ['Time to deploy', 'count'] ### adding the columns to the values returned previously 
tdc = px.line(dfds1, x='Time to deploy', y= 'count') ### plotting the graph 
tdc.update_layout(title="Time to Deploy an Order",xaxis_title="Time in Minutes",yaxis_title="") ### adding more details onto the graph

#################################################################### This graph was sent into its area due to filtering reasoning
### slider for filtering in graph
#slides = st.sidebar.slider('Top n Locations', 0, 90, 5)
#addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index() ### from slider number its shows the desired ones by grouping 
#addy.columns = ['Adress', 'count'] ### turning them into columns
#addresss = px.bar(addy, y='Adress', x = 'count') ### plotting the variables

###################################### Average revenue per day
st.cache()
### Graphing the day names with a certain order and text shown on graph
dincome = px.histogram(df, x="Day Name",y='Amount', histfunc='avg',text_auto=True,category_orders={'Day Name':["Monday","Tuesday","Wednesday", "Thursday", "Friday", "Saturday","Sunday"]})
dincome.update_layout(title="Average Revenue Per Day",xaxis_title="Day Name",yaxis_title="Amount") ### adding more details on the graph

### Creating the first tab of hydralit
@app.addapp(is_home=True,icon='🏪') # Setting this to be the home tab and adding an icon
def Home():
 st.cache()
 st.title('Diwan Delivery Analysis') ### Adding page title
 ### Adding comments onto the home tab for understanding the dashboard
 st.header('What is the objective of this Dashboard?')
 st.write('In this dashboard, we are trying to analyze Diwan’s Delivery sector, by making visuals to help us understand what is happening on the ground as it brings many managerial insights about how the company is doing throughout the year. This dashboard will go into three various sub-sections in the delivery sector. The three sub-sections that we will be focusing on are:')
 st.write('1-	Employees related analysis')
 st.write('2-	Type of methods used in ordering')
 st.write('3-	Customer analysis and the area they are ordering from')
 st.write('After going through each tab and its respectable analysis we would understand in more detail how this information can enable us to adapt accordingly. Each tab represents a certain sub-section and a quick analysis of what is being presented.')

 ### Adding Tableau dashboard link for secondary dashboard
 st.write('For additional visuals feel free to press the following link')
 link = '[Tableau]https://public.tableau.com/app/profile/salem.gr/viz/DiwanDeliverySectorAnalysis/DiwanDeliverySectorAnalysis'
 st.markdown(link, unsafe_allow_html=True)

 ### Importing the table ive made on the queuing model using csv github
 st.write('The following button has three models depending on demand Diwan should hire accordingly with its following costs')
 df1= pd.read_csv('https://github.com/SalemGrayzi/status/raw/main/Queing%20Model.csv')

  
## defining a code to convert df1 into utf-8
 def convert_df(df1):
     return df1.to_csv().encode('utf-8')

## Converting the csv file to utf-8
 csv = convert_df(df1)

### Creating a download button to get the queuing model
 st.download_button(
     label="Download Queuing Model",
     data=csv,
     file_name='Queuing_Model.csv',
     mime='text/csv',
  )

 ### Word documents from google drive where it has the full report once clicked it downloads
 st.write('For the full analysis press the following link to be redirected to the report')
 link1 = '[Full Report]https://drive.google.com/uc?export=download&id=1DIpi1zVrAKAaCe8EFs0ePeVgfx6hwj8N'
 st.markdown(link1, unsafe_allow_html=True)
 ### Powerpoint from google drive once clicked it downloads
 st.write('For the powerpoint press the following link')
 link1 = '[Powerpoint]https://drive.google.com/uc?export=download&id=1MrmHWmS_klWlUdxgblnQHxWrkqb-Qjsj'
 st.markdown(link1, unsafe_allow_html=True)
 ### making columns to put both check boxes together side by side   
 c1,c2 = st.columns(2)
    
 head = c1.checkbox('First Few Rows') # Making a checkbox for showing df.head
 if head:
     st.write(df.head())

 if c2.checkbox('Show all graphs'): # Adding all graph into a single button to see
    st.subheader('All Graphs')
    container1 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g1, g2,g21 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container1:
        with g1:
            Day
        with g21:
            driver


    container2 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g3, g4, g41 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container2:
        with g3:
            #s1,s2 = st.columns(2)
            split_size = st.slider('Top n Drivers', 0, 90, 5)
            dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
            dfd.columns = ['Driver Name', 'count']
            drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
            drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
            drv
        with g41:
            pda
    container3 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g5,g6,g61 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container3:
        with g5:
            st.pyplot(gh)
        with g61:
            st.pyplot(pdapicker)
    container4 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g7,g8,g81 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container4:
        with g7:
            stpk
        with g81:
            onmount
    container5 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g9,g10,g01 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container5:
        with g9:
            onmount2
        with g01:
            n_size = st.slider('Top n Customers', 0, 90, 5)
            dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
            amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
            amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
            amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
            amc
    container6 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g11,g12,g02 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container6:
        with g11:
            sto
        with g02:
            tc
    container7 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g13,g14,g04 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with container7:
        with g13:
            tdc
        with g04:
            slides = st.slider('Top n Locations', 0, 90, 5)
            addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
            addy.columns = ['Adress', 'count']
            addresss = px.bar(addy, y='Adress', x = 'count', text_auto=True)
            addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
            addresss
    container8 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    g15,g16 = st.columns(2) ### using 2 columns just so i can move it to the left side  
    ### Putting the graphes into the containers and their columns
    with container8:
        with g15:
            dincome
        with g16:
            st.write('')

# End of tab 1

############################################################################ Building the second tab

@app.addapp(title='Employee Related Analysis',icon='💼') ### Adding the name of tab as well as an icon
def app2():
 st.cache()
### A brief introduction on this section
 st.write('In this section, we are going to be talking about how the pickers are utilizing the PDA equipment as well as how it might affect an order status. Here we will find the distribution of PDA usage across the pickers to find the percentage of if they are using said equipment or not. After finding the percentage of usage of PDA we turn our heads to find the proportions of each picker if their orders were canceled or delivered as this might arise some issues that some pickers might be falling behind whether it’s their service or an issue they are facing for higher cancelation rates.')

### Setting a selectbox with all graphs related to this section
 PDA1 = st.selectbox('Employee Related Analysis',
                                    ['None','Pickers','Picker and Order Status','PDA Usage','Drivers','PDA and Status of Order','All'])

### Setting up the selectbox for the following graphs with each graph having a small dynamic description of graph 
 if PDA1 == 'Pickers':
    st.pyplot(pdapicker)
    st.write('Here we can see each picker that is using a PDA or not. as we can see many of the pickers are not using the PDA in thier daily operations.')
 elif PDA1 == 'PDA Usage':
        pda
        st.write(f'From this graph we can analyze that {round(hp1,2)}% of pickers are using PDAs compared to {round(hp,2)}% of them not using PDA. This shows that we should find a way to push the usage of PDAs across the pickers.')
 elif PDA1 == 'Picker and Order Status':
        stpk
        st.write('In this graph we can see the proportions of each picker from their total orders based on cancelation, and completed orders. The Blue shows the orders that have been completed comapared to red which shows the cancelations. As we can see there are couple of pickers that have a higher probability of their orders being canceled this is why we need to get to the bottom of the issue to fix it.')
 elif PDA1 == 'Drivers':
#        driver
        s1,s2 = st.columns(2)
        split_size = s1.slider('Top n Drivers', 0, 90, 5)
        dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
        dfd.columns = ['Driver Name', 'count']
        drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
        drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
        drv
        st.write(f'The top {split_size} drivers are shown, with the corresponding number of orders throughout the year')
 elif PDA1 == 'PDA and Status of Order':
        st.pyplot(gh)
        st.write('This graph is very important as it shows us how does PDA affect the order status. As we can see orders that were canceled with the usage of PDA has a much lower ratio compared to not using PDAs. Even though delivered orders are similar to each other but with cancelation there is a big difference between them.')

 elif PDA1 == 'All':
    containerera = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    era1,era2,era21 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containerera:
        with era1:
            st.pyplot(pdapicker)
        with era21:
            driver
    containerera1 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    era3,era4,era41 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containerera1:
        with era3:
            split_size = st.slider('Top n Drivers', 0, 90, 5)
            dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
            dfd.columns = ['Driver Name', 'count']
            drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
            drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
            drv
        with era41:
            pda
    containerera2 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    era5,era6,era61 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containerera2:
        with era5:
            stpk
        with era61:
            st.pyplot(gh)
 elif PDA1 == 'None':
        st.write(str(''))

# End of tab 2

############################################################################ Building tab 3

@app.addapp(title='Ordering Methods',icon='📲') ### Tab 3's name and icon
def app3():
 st.cache()
### Small introduction of tab
 st.write('In this section, we focus on which ordering method is bringing in the most revenue and causing lost opportunity sales. The two methods are using the phone to order, or the application. Finally, we would like to find which ordering method has a higher probability of lost sales, and which generates the most revenue.')

### Setting up the selectbox for the following graphs with each graph having a small dynamic description of graph 
 App = st.selectbox('Application or Call Analysis',
                                     ['None', 'App vs. Call Revenues and Lost Sales','Status of Delivery Using App','All'])

 if App == 'App vs. Call Revenues and Lost Sales':
     onmount
     onmount2
     st.write(f'The order methods that are being used to order would be {round(os,2)}% application and {round(os1,2)}% phone calls')
 elif App == 'Status of Delivery Using App':
     sto
     st.write('The ratio between delivered and canceled between the two ordering methods is significant as we can see phone calls have a higher probability to be canceled compared to applications. This could indicate an issue in the call center resulting in more canceled orders.')
 elif App == 'All':
    containeraca = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    aca1,aca2,aca3 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containeraca:
        with aca1:
            onmount
        with aca3:
            onmount2
    containeraca1 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    aca4,aca5,aca51 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    with containeraca1:
        with aca4:
            sto
 elif App == 'None':
     st.write(str(''))

# End of tab 3

############################################################################ Building tab 4

@app.addapp(title='Customer Analysis',icon='📈') ### Naming the fourth tab and setting up its icon
def app4():
 st.cache()
### Small introduction of tab
 st.write('Finally, the last section covers the customers. In this section, we will be looking at overall lost sales and generated revenues, and several other pieces of information that are valuable to understanding Diwan’s customers. Here we look at revenues generated by each customer and which day generates the most. An important part is analyzing which days are the highest demand, and the area they are coming from. Last but not least is finding the distribution of the time of incoming orders to understand during which time has the biggest workload on the pickers, and see how long it takes to deploy an order.')

 def my_value(number):
     return ("{:,}".format(number)) # a function to format numbers to have commas in them

### Creating KPI design showing the revenue and lost sales
 asd=df.loc[df['Status'] == 'Delivered'].Amount.sum()
 asc=df.loc[df['Status'] == 'Canceled'].Amount.sum()
### Making columns so they can be side by side
 col1, col2 = st.columns(2)
 col1.metric(label="Revenue in LBP", value=millify(asd, precision=2), delta_color="inverse") ### total revenue
 col2.metric(label="Lost Sales in LBP", value=millify(asc, precision=2), delta_color="inverse") ### Total loss of sales

### Setting up the selectbox for the following graphs with each graph having a small dynamic description of graph 
 App = st.selectbox('Customer Analysis',
                                     ['None','Days','Revenue Per Customer','Wait Time to Deploy','Time of Incoming Orders','Address','Average Revenue Per Day','All'])

 if App == 'Revenue Per Customer':
     s11,s22 = st.columns(2)
     n_size = s11.slider('Top n Customers', 0, 90, 5)
     dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
     amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
     amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
     amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
     amc
     st.write(f'This visual is important for Diwan to find its highest revenue generated customers, as this assists Diwan in implementing a loyalty program for their customers. Using the filter we are able to find the top {n_size} of customers and their respectable revenues.')
 elif App == 'Wait Time to Deploy':
     tdc
     st.write(f'On average there is an 60-minute wait to deploy an order. This shows us the distribution of wait times before an order is deployed as this is important to achieve a better service level and compete with other competitors.')
 elif App == 'Time of Incoming Orders':
     tc
     st.write('Understanding when orders are coming in is important to allocate the right human resource, as we can see between 10 am and 2 pm we can see most orders are coming in then declining at a steady rate.')
 elif App == 'Days':
     Day
     st.write('Throughout the week we can see that demand is constant except for Monday with the highest demand and Friday with the lowest demand but on average there is a 100 order difference between the days.')
 elif App == 'Average Revenue Per Day':
     dincome
     st.write('Days with high demand don’t necessarily mean the highest revenue generated days on average as this graph illustrates. Wednesday has the highest revenue compared to Friday with little variation between each day.')
 elif App == 'Address':
     s11,s22 = st.columns(2)
     slides = s11.slider('Top n Locations', 0, 90, 5)
     addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
     addy.columns = ['Adress', 'count']
     addresss = px.bar(addy, y='Adress', x = 'count',text_auto=True)
     addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
     addresss
     st.write(f'Due to the location of Diwan, most orders are coming in from Bchamoun, followed by Aramoun, and finally Khaldeh. This is due to the prime location that enables Diwan to service these 3 major areas. The graph is showing the top {slides} locations, depending on desired number')
 elif App == 'All':
    containerca = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    ca1,ca2,ca21 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containerca:
        with ca1:
            n_size = st.slider('Top n Customers', 0, 90, 5)
            dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
            amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
            amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
            amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
            amc
        with ca21:
            tdc
    containerca1 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    ca3,ca4,ca41 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containerca1:
        with ca3:
            tc
        with ca41:
            Day
    containerca2 = st.container() ### Adding a container and columns so grpahs are side by side through out all graphs
    ca5,ca6,ca61 = st.columns(3) ### using 3 columns due to having 2 the graphs over lap when 2 columns is done 
    ### Putting the graphes into the containers and their columns
    with containerca2:
        with ca5:
            slides = st.slider('Top n Locations', 0, 90, 5)
            addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
            addy.columns = ['Adress', 'count']
            addresss = px.bar(addy, y='Adress', x = 'count',text_auto=True)
            addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
            addresss
        with ca61:
            dincome
 elif App == 'None':
     st.write(str(''))

# End of tab 4

######################################################### Building tab 5
@st.cache(allow_output_mutation=True)

@app.addapp(title='Queuing Model ',icon='⌚') ### This tab was built to explain who the person behind all this

def app5():
 st.cache()
 st.header('Interactive Queuing Model')
 st.write('The queuing model considers 6 variables, this is due to the flexibility of the model and can be used for other processes in the organization, but in the scope of the capstone we will focus on the delivery sector. The variables are:')
 st.write('1-	Number of pickers in the system')
 st.write('2-	Incoming orders per hour')
 st.write('3-	Pickers capacity which is calculated by 60 minutes divided by how many minutes a picker takes on average to deploy an order')
 st.write('4-	Picker’s salary per hour to get total cost')
 st.write('5-	Cost of call per minute to get total cost of waiting')
 st.write('6-	The LBP exchange rate as it is exchanging constantly')
 st.write('After inserting the variables into the specified area the model would return:')
 st.write('•	Utilization of pickers')
 st.write('•	Average amount of wait before deploying an order')
 st.write('•	Labor cost with the number of specified pickers and their cost per hour')
 st.write('•	Call cost of customers who are waiting in the system')
 st.write('•	Total cost of labor, and call')
 st.write('•	Lastly converting it to U.S.D')

 def my_value(number):
     return ("{:,}".format(number)) # a function to format numbers to have commas in them



 with st.form(key='form1'):
     col11, col22, col33, col44, col55, col66 = st.columns(6) # creating 6 columns to put all the input boxes next to each other
     emp = col11.number_input('Number of Pickers', value=12,min_value=1, step=1)
     orde= col22.number_input('Orders per Hour',value=11)
     cap = col33.number_input("Picker's Capacity per Hour",value=1)
     costp = col44.number_input("Picker's Salary per Hour",value=16203.70)
     costc = col55.number_input('Cost of Call per Minute',value=0.004,format="%.5f")
     rate = col66.number_input('Insert LBP Exchange Rate',value=29500)
     st.cache()
     try:
        result = orde/(emp*cap)
     except ZeroDivisionError: # error will appear if zero division error appears
        result = 0 # then returning 0 as output

     print(result)

     if (result < 0 or result > 1) : #if Utilization is less than 0 and greater than 1 returns an error
        st.error('Inavlid Model')
     else:
        sc=(result**np.sqrt(2*(emp+1)))/orde # formula to calculate the first part of the equation using the numbers that have been input
        try:
            uf=1/(1-(orde/(emp*cap)))
        except ZeroDivisionError: # error will appear if zero division error appears
            uf = 0# then returning 0 as output
        mint=uf*sc # calculating orders per minute
        wait=mint*60 # then turning it into hours
        lc=costp*emp # calculating labor costs
        wc=costc*60 # calculating the cost of call per hour
        wcr=wc*rate # turning it into the black market exhange of LBP
        wcrr=mint*wcr*orde # total cost of call per hour
        total=lc+wcrr # total cost of labor and call
        totalusd=total/rate
        qm1, qm2, qm3 = st.columns(3)
        qm1.metric("Pickers Utilization %", value=round(result*100,2))
        qm2.metric("Avg. Wait Time", value=round(wait, 2))
        qm3.metric("Total Cost in USD", value=round(totalusd,2))
     st.form_submit_button('Press to calculate') #button to be pressed to initiate calculating
    # Writing the results from the calculations
 if(st.button("Click for more...")):
   st.write(f'Utilization of pickers {round(result*100,2)}%')
   st.write(f'On average minutes {round(wait, 2)} before order deployment')
   st.write(f'Labor cost for {emp} pickers would be {my_value(round(lc))} LBP per hour')
   st.write(f'Call cost for {orde} customers waiting would be {my_value(round(wcrr))} LBP per hour')
   st.write(f'Total cost would be {my_value(round(total))} LBP per hour')
   st.write(f'Total cost in U.S.D would be ${round(totalusd,2)} per hour')
# End of tab 5

######################################################### Building tab 6
@app.addapp(title='About',icon='🤵') ### This tab was built to explain who the person behind all this

def app6():
 st.write('This dashboard was made possible by Salem Gr., for Diwan Hyper Market located in Lebanon, Old Saida Road Chouaifet. The dashboard was built to help analyze Diwan’s delivery sector to assist them in lowering wait time and show data collected to make managerial decisions to improve their service levels.')
 st.write('I am an AUB graduate studying to become a data analyst by using the methods learned at AUB to solve real-world problems and assist companies in understanding the data they acquired to find issues or ways to improve in this competitive world. With the power of data analysis and my undergraduate degree in International Business and management finding and understanding issues are up to my field of expertise. This dashboard and related report are proof of what my combined degrees can offer you.')
 st.write('Feel free to contact me for any future project using one of the following methods described below')
 if(st.button("Contact Information")):
    st.markdown("Phone Number (Lebanon): +961 78 810 351")
    st.markdown("Phone Number (U.S.): +1 786 609 0482")
    st.markdown("Email Address: shg09@mail.aub.edu")
    link2 = '[linkedin] https://www.linkedin.com/in/salemgr/'
    st.markdown(link2, unsafe_allow_html=True)

# End of tab 6
#########################################################

#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()
