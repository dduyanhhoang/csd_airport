import sqlite3


# Create table if it does not exist
def create_table():
    conn = sqlite3.connect('airport_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS AIRPORT (
                    ID INTEGER PRIMARY KEY,
                    X INTEGER,
                    Y INTEGER
                    )''')
    conn.commit()
    conn.close()


def insert_airport(airport_id, x, y):
    conn = sqlite3.connect('airport_system.db')
    c = conn.cursor()
    c.execute('INSERT INTO AIRPORT (ID, X, Y) VALUES (?, ?, ?)', (airport_id, x, y))
    conn.commit()
    conn.close()


def insert_airports():
    airports = [
        (1, 50, 100),
        (2, 150, 200),
        (3, 250, 300),
        (4, 350, 400),
        (5, 450, 500)
    ]

    for airport in airports:
        insert_airport(airport[0], airport[1], airport[2])


# Main function to create table and insert data
def main():
    # create_table()
    # insert_airports()
    # print("Data inserted successfully")
    conn = sqlite3.connect('airport_system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM AIRPORT')
    print(c.fetchall())
    conn.close()


if __name__ == "__main__":
    main()
