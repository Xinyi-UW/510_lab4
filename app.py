import os
import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self, database_url):
        self.con = psycopg2.connect(database_url)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                price TEXT NOT NULL,
                rating TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.con.commit()

def setup_database(db):
    try:
        db.create_table()
        print("Database setup completed: Table 'books' is ready.")
    except Exception as e:
        print(f"Failed to set up database: {e}")

def main():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        st.error("Database URL is not set.")
        return

    try:
        with Database(DATABASE_URL) as db:
            setup_database(db)  # Ensure the table is created
            df = pd.read_sql('SELECT * FROM books', db.con)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    if df.empty:
        st.error("No data available to display.")
        return

    st.title('Book Explorer')

    # UI layout adjustments
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("Search by book name")
        if search_query:
            df = df[df['title'].str.contains(search_query, case=False)]

    with col2:
        # Separate search fields for Price and Rating
        price_query = st.text_input("Search by price (e.g., £20)")
        if price_query:
            df = df[df['price'] == price_query]

        rating_query = st.selectbox("Filter by rating", ['', 'One', 'Two', 'Three', 'Four', 'Five'])
        if rating_query:
            df = df[df['rating'] == rating_query]

    # Sorting options
    sort_by = st.selectbox("Sort by", ["Price", "Rating"], index=0)
    df = df.sort_values(by=sort_by.lower(), ascending=False)

    if df.empty:
        st.warning("No results found.")
    else:
        st.dataframe(df, height=600)

if __name__ == "__main__":
    main()
