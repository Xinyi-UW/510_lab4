import psycopg2

class Database:
    def __init__(self, DATABASE_URL) -> None:
        self.con = psycopg2.connect(DATABASE_URL)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def create_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            rating TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(q)
        self.con.commit()


    def insert_book(self, book):
        q = """
        INSERT INTO books (title, price, rating) VALUES (%s, %s, %s)
        """
        try:
            self.cur.execute(q, (book['title'], book['price'], book['rating']))
            self.con.commit()
            print("Book inserted successfully:", book['title'])  # Logging the successful insertion
        except Exception as e:
            print("Failed to insert book:", e)  # This will show any SQL errors or connection issues




        
