# Roni-s-Mac-Bar
### Data Setup: 
For the data setup, we used google colab(https://colab.research.google.com/drive/1NTlExhqaiB9hASCAbkQ-BCL3ITSOCbJf?authuser=1#scrollTo=9xYnDbwZiJ95) to sort and parse the data. We only really had to concatenate the data for the nona_data.csv file but for the shirts we had to cleverly utilize pandas to parse and seperate it from the rest of the data. The colab is a little messy but we simply just used it just to get the data combined together, drop the corrupted or empty data slots, and export the final csv's we used for this project. 

### Setup:
In order to setup this project, all you need to do is go to streamlit cloud(https://streamlit.io/cloud) and select your github and choose the repository and what file(app.py) that you want the cloud to run, and that is simply all that needs to be done to setup the dashboard. 

### Dashboard Functionality:
Using the code in app.py we created a very clean dashboard to view insights from the monthly Roni's Mac Bar data presented to us. With the use of streamlit cloud, the user will be presented with 4 graphs per section. There are 4 sections, Main insights, Additional insights, and shirt insights. Each section has a detailed Statistics tab that will summarize the key insights from all the data collected and presented by the graphs. You can hover over each graph to see the exact value presented by the x and y axis, for precise analysis. 

### Key Insights:
We conclude from the data and the graphs that from the 7 months given(October-July, 2024) Roni's Mac Bar:
* Total Orders: 9064
* Average Orders per Day: 46.5
* Busiest Hours of the Day: 12:00(11:00pm) and 19:00(7:00pm)
* Busiest Day: Saturday
* Average Items per Order: 30.1
* Most Popular Item: Mac and Cheese
* Most commmon Modifier: Regular
* Month of Least Orders: July, 2024(Can be explained by college students going home for the summer)

### Shirt Insights
We additionally included data for the merch at Roni' Mac Bar, which we find as a very important aspect of business. With this analysis we hope that the company can gain insights to expand their merch collection in the most optimal way as it is a very big asset for companies. 
* Total Shirts Sold: 19
* Most Popular Shirt Sizes: Small(23.5%), Medium(23.5%), and 2X Shirt(23.5%)
* Peak ordering hours for Shirts: 17:00(5:00pm)

### Conclusion
We hope Roni's Mac Bar can use the insights we have gained from the data, and the dashboard we created to expand and optimize their business in order to expand and reap the most profit possible.
