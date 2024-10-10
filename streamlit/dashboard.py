import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar Information
st.sidebar.title("E-Commerce Public Data Analysis")
st.sidebar.write('''
    **Nama:** Rizky Tri Pamungkas
    **Email:** rizkytripamungkas9@gmail.com
    **ID Dicoding:** rizkypamungkas
''')
st.sidebar.caption("Copyright © Rizky Tri Pamungkas 2024")

all_data = pd.read_csv(r'D:/python/all_data.csv')

# Set up Streamlit layout
st.title('Dashboard: E-Commerce Public Data Analysis')

# Visualisasi 1
# Subheader
st.subheader('How is the sales trend in 2017 and 2018?')

# Filtering data only in 2017 and 2018
filtered_data = all_data[(all_data['order_year'] == 2017) | (all_data['order_year'] == 2018)]

# Group data by year and month to calculate the number of transactions
monthly_transactions = filtered_data.groupby(['order_year', 'month_num'])['order_id'].nunique().reset_index()
monthly_transactions = monthly_transactions.sort_values(by=['order_year', 'month_num'])

# Create a custom palette for colours
custom_palette = ["#0DA6D1", "#102cd4"]

# Create the figure and axes using subplots
fig, ax = plt.subplots(figsize=(12, 6))  # Create figure and axis

# Create the bar plot
sns.barplot(data=monthly_transactions, x='month_num', y='order_id', hue='order_year', palette=custom_palette, ax=ax)

# Set titles and labels
ax.set_title('Monthly Transaction Trends for the Years 2017 and 2018')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Transactions')
ax.set_xticks(range(12))  # Ensure x-ticks are 0-11
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])  # Set month labels
ax.legend(title='Year')  # Set legend title

# Show plot in Streamlit
st.pyplot(fig)  # Display the figure in Streamlit

# Visualisasi 2
st.subheader('What product categories have the highest and lowest sales?')

# Count the number of products sold per category
product_counts = all_data.groupby('product_category_name').size().reset_index(name='products')

# Sort by number of products sold
top_products = product_counts.sort_values(by='products', ascending=False).head(5)
least_products = product_counts.sort_values(by='products', ascending=True).head(5)

# Create plot
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Plots of best-selling category
sns.barplot(x="products", y="product_category_name", data=top_products, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best-selling category", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

# Plots of lowest-selling category
sns.barplot(x="products", y="product_category_name", data=least_products, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Lowest-selling category", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Best and lowest selling by category", fontsize=20)

# Show plot in Streamlit
st.pyplot(fig)

# Visualisasi 3
st.subheader('Which states recorded the most purchases?')

# Grouping the data by customer state and counting unique customers
bystate_df = all_data.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

# Sort the dataframe by customer count
bystate_df = bystate_df.sort_values(by='customer_count', ascending=False)

# Find the state with the most customers
most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Create the bar plot with a custom color palette
sns.barplot(x='customer_state',
            y='customer_count',
            data=bystate_df,
            palette=["#102cd4" if state == most_common_state else "#D3D3D3" for state in bystate_df['customer_state']],
            ax=ax)

# Set the title and labels
ax.set_title("Number of Customers from Each State", fontsize=15)
ax.set_xlabel("State")
ax.set_ylabel("Number of Customers")
ax.tick_params(axis='x', labelsize=10)

# Show the plot in Streamlit
st.pyplot(fig)

# Visualisasi 4
st.subheader('Which city has the highest number of customers by purchase?')

# Get the top 10 cities by customer count
top_city = all_data['customer_city'].value_counts().head(10)

# Find the most common city
most_common_city = top_city.idxmax()

# Sort the city counts in descending order
top_city = top_city.sort_values(ascending=False)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Create the bar plot with a custom color palette
sns.barplot(x=top_city.index,
            y=top_city.values,
            palette=["#102cd4" if city == most_common_city else "#D3D3D3" for city in top_city.index],
            ax=ax)

# Set the title and labels
ax.set_title("Number of Customers from Each City", fontsize=15)
ax.set_xlabel("City")
ax.set_ylabel("Number of Customers")
ax.set_xticklabels(top_city.index, rotation=45, fontsize=10)

# Show the plot in Streamlit
st.pyplot(fig)

#Visualisasi 5
# Subheader
st.subheader('How is the customer satisfaction level?')

# Count the occurrences of each review score and sort them in descending order
review_scores = all_data['review_score'].value_counts().sort_values(ascending=False)

# Identify the most common review score
most_common_score = review_scores.idxmax()

# Set the visual style for the plot
sns.set(style="darkgrid")

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 5))

# Generate a bar plot for review scores with a custom color for the most common score
sns.barplot(x=review_scores.index,
            y=review_scores.values,
            palette=["#102cd4" if score == most_common_score else "#D3D3D3" for score in review_scores.index],
            ax=ax)

# Set the title and labels for the plot
ax.set_title("Evaluation of satisfaction level based on rating", fontsize=15)
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
ax.tick_params(axis='x', labelsize=12)

# Show the plot in Streamlit
st.pyplot(fig)


