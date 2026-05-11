import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("Choose the fruits you want in your custom smoothie!")

# Text input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# -----------------------------
# SNOWFLAKE CONNECTION (FIXED)
# -----------------------------
conn_params = {
    "account": st.secrets["snowflake"]["account"],
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "role": st.secrets["snowflake"]["role"],
    "warehouse": st.secrets["snowflake"]["warehouse"],
    "database": st.secrets["snowflake"]["database"],
    "schema": st.secrets["snowflake"]["schema"],
}

session = Session.builder.configs(conn_params).create()

# Get fruit list
df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in df.collect()]

# Multiselect (FIXED: must use list, not dataframe)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Build string safely
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    if st.button("Submit Order"):

        session.sql(f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """).collect()

        st.success(f"Your smoothie has been ordered, {name_on_order}! ✅")
