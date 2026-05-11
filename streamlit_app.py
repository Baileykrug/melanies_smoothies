import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# User input
name_on_order = st.text_input("Name on Smoothie:")

# Snowflake connection
cnx = st.connection(
    "snowflake",
    account="...",
    user="...",
    password="...",
    role="...",
    warehouse="...",
    database="...",
    schema="..."
)

session = cnx.session()

# Fetch fruit list → convert to Python list
df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in df.collect()]

# Multiselect now works correctly
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Build insert only when button is pressed
if st.button("Submit Order"):

    if not name_on_order:
        st.error("Please enter a name for your smoothie!")
        st.stop()

    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    session.sql(my_insert_stmt).collect()

    st.success(f"Your smoothie has been ordered, {name_on_order}! ✅")
