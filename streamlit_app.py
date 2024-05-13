# Import python packages
import streamlit as st
import requests
#import inflect
import pandas as pd
from snowflake.snowpark.functions import col 
# from snowflake.snowpark.context import get_active_session

"""
def singularize_plural_words(input_string):
    p = inflect.engine()
    words = input_string.split()
    singularized_words = [p.singular_noun(word) if p.singular_noun(word) else word for word in words]
    return ' '.join(singularized_words)
"""

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# session = get_active_session()

cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options") \
                      .select(col("FRUIT_NAME"), col('SEARCH_ON'))

# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas() 
# st.dataframe(pd_df)
# st.stop();

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be: ", name_on_order)

options = st.multiselect(
    "Choose up to five ingredients"
    , my_dataframe
    , max_selections = 5)

if options:   
    ingredients_string = ''
    for fruit_chosen in options: 
        ingredients_string += fruit_chosen + ' '


    my_insert_stmt = \
    """ insert into smoothies.public.orders(ingredients, name_on_order) 
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop, good for tsg
    # st.stop
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert: 
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")

    ingredient_string = ''

    for fruit_chosen in options:
        ingredient_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0] 
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        print(search_on)
        
        st.subheader(fruit_chosen + ' Nutrition information')
        # New section to display fruityvice nutritions
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + str(search_on))
        # st.text(fruityvice_response)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)





















