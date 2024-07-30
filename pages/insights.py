import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import json

DB_URL = "sqlite:///data/data.sqlite"  # Define database URL

def get_connection() -> 'sqlalchemy.engine.Engine':
    engine = create_engine(DB_URL)
    return engine

conn = get_connection()  # Create a connection using the get_connection function

# Create pandas DataFrames from the SQL tables
sales_df = pd.read_sql_query("SELECT * FROM Sales", conn)
customers_df = pd.read_sql_query("SELECT * FROM Customers", conn)

# Define the restaurants variable
restaurants = [
    {"id": 1, "name": "The Auckland Eatery", "location_id": 1},
    {"id": 2, "name": "Arch Hill Diner", "location_id": 2},
    {"id": 3, "name": "Devonport Delights", "location_id": 3},
    {"id": 4, "name": "Takapuna Tastes", "location_id": 4},
    {"id": 5, "name": "Parnell Pizzeria", "location_id": 5},
    {"id": 6, "name": "Ponsonby Pasta", "location_id": 6},
    {"id": 7, "name": "CBD Cuisine", "location_id": 7},
    {"id": 8, "name": "Wellington Waffles", "location_id": 8},
    {"id": 9, "name": "Te Aro Tacos", "location_id": 9},
    {"id": 10, "name": "Thorndon Thali", "location_id": 10},
    {"id": 11, "name": "Victoria Vegan", "location_id": 11},
    {"id": 12, "name": "CBD Cafe", "location_id": 12},
    {"id": 13, "name": "Kapiti Kitchen", "location_id": 13},
    {"id": 14, "name": "Addington Appetizers", "location_id": 14},
    {"id": 15, "name": "Aranui Asian", "location_id": 15},
    {"id": 16, "name": "Riccarton Ribs", "location_id": 16},
    {"id": 17, "name": "Merivale Mexican", "location_id": 17},
]

# Create a DataFrame from the list of dictionaries
restaurants_df = pd.DataFrame(restaurants)

# Merge the Ratings and Restaurants DataFrames on the 'id' column
ratings_df = pd.read_sql_query("SELECT * FROM Ratings", conn)
merged_df = pd.merge(ratings_df, restaurants_df, left_on='restaurant_id', right_on='id')

# Select the restaurant names from the merged DataFrame
restaurant_names = merged_df['name']

city_df = pd.read_sql_query("SELECT restaurant_id, number_of_customers, locations.city, locations.suburb FROM customers JOIN restaurants ON customers.restaurant_id = restaurants.id JOIN locations ON restaurants.location_id = locations.id", conn)

suburb_coords = {
    "Arch Hill": {"lat": -36.8604, "lon": 174.7460},
    "Devonport": {"lat": -36.8303, "lon": 174.7952},
    "Takapuna": {"lat": -36.7866, "lon": 174.7766},
    "Parnell": {"lat": -36.8527, "lon": 174.7832},
    "Ponsonby": {"lat": -36.8553, "lon": 174.7473},
    "Auckland CBD": {"lat": -36.8485, "lon": 174.7633},
    "Te Aro": {"lat": -41.2942, "lon": 174.7741},
    "Thorndon": {"lat": -41.2749, "lon": 174.7754},
    "Mount Victoria": {"lat": -41.2948, "lon": 174.7834},
    "Wellington CBD": {"lat": -41.2865, "lon": 174.7762},
    "Kapiti": {"lat": -40.9000, "lon": 175.0120},
    "Addington": {"lat": -43.5392, "lon": 172.6203},
    "Aranui": {"lat": -43.5217, "lon": 172.6946},
    "Riccarton": {"lat": -43.5311, "lon": 172.5990},
    "Merivale": {"lat": -43.5166, "lon": 172.6161}
}

def add_coordinates(df):
    df['lat'] = df['suburb'].apply(lambda x: suburb_coords[x]['lat'] if x in suburb_coords else None)
    df['lon'] = df['suburb'].apply(lambda x: suburb_coords[x]['lon'] if x in suburb_coords else None)
    return df

def make_choropleth(input_df, input_lat, input_lon, input_column, input_color_theme):
    fig = px.scatter_geo(
        input_df,
        lat=input_lat,
        lon=input_lon,
        color=input_column,
        color_continuous_scale=input_color_theme,
        size=input_column,
        hover_name="suburb",
        projection="natural earth",
        labels={input_column: input_column.capitalize()},
        title='Number of Customers by Suburb'
    )
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return fig

def main():
    st.title('Restaurant Data Dashboard')

    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Select a page:', ['Sales', 'Customers', 'Ratings'])

    if page == 'Sales':
        st.header('Projected Sales Revenue Data')
        st.write(sales_df)
        sales_per_restaurant = sales_df.groupby('restaurant_id')['sales_amount'].sum().reset_index()

        # Merge the sales_per_restaurant and restaurants_df DataFrames on the 'restaurant_id'/'id' column
        sales_per_restaurant = pd.merge(sales_per_restaurant, restaurants_df, left_on='restaurant_id', right_on='id')

        fig = px.pie(sales_per_restaurant, values='sales_amount', names='name', title='Sales Amount by Restaurant')
        st.plotly_chart(fig)


    elif page == 'Customers':
        st.header('Projected Customer Amount Data')
        st.table(city_df)

        # Aggregate the data by restaurant_id
        customers_per_restaurant = customers_df.groupby('restaurant_id')['number_of_customers'].sum().reset_index()
        # Merge the customers_per_restaurant and restaurants_df DataFrames on the 'restaurant_id'/'id' column
        customers_per_restaurant = pd.merge(customers_per_restaurant, restaurants_df, left_on='restaurant_id', right_on='id')
        
        # Create a bar chart with the aggregated data
        fig = px.bar(customers_per_restaurant, x='name', y='number_of_customers', title='Number of Customers by Restaurant')
        st.plotly_chart(fig)

        # Aggregate the data by suburb for the choropleth map
        suburb_agg_df = city_df.groupby('suburb', as_index=False)['number_of_customers'].sum()

        # Add coordinates to the DataFrame
        suburb_agg_df = add_coordinates(suburb_agg_df)

        # Generate the choropleth map for New Zealand suburbs
        choropleth = make_choropleth(suburb_agg_df, 'lat', 'lon', 'number_of_customers', 'Viridis')
        st.plotly_chart(choropleth)

    elif page == 'Ratings':
        st.header('Ratings Data')
        st.table(ratings_df)

        # Aggregate the data by restaurant_id
        ratings_per_restaurant = ratings_df.groupby('restaurant_id')['rating'].mean().reset_index()
        
        # Merge the ratings_per_restaurant and restaurants_df DataFrames on the 'restaurant_id'/'id' column
        ratings_per_restaurant = pd.merge(ratings_per_restaurant, restaurants_df, left_on='restaurant_id', right_on='id')
        
        # Create a bar chart with the aggregated data
        fig = px.bar(ratings_per_restaurant, x='name', y='rating', title='Average Ratings by Restaurant')
        st.plotly_chart(fig)



if __name__ == "__main__":
    main()
