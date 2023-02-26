import psycopg2
from pprint import pprint



def drop_db():
    cur.execute("""
            DROP TABLE client_phone;
            """)

    cur.execute("""
            DROP TABLE client_info;
            """)
    conn.commit()


def create_db():
    cur.execute("""
            CREATE TABLE IF NOT EXISTS client_info(
                user_id int NOT NULL UNIQUE,
                user_first_name VARCHAR(40) NOT NULL,
                user_last_name VARCHAR(40) NOT NULL,
                user_email VARCHAR(80) NOT NULL UNIQUE
            );
            """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS client_phone(
                id SERIAL PRIMARY KEY,
                user_id int REFERENCES client_info(user_id),
                user_phone_number TEXT
            );
            """)
    conn.commit()


def add_client(user_id, first_name, last_name, email, phone_number=None):
    cur.execute("""
            INSERT INTO client_info(user_id, user_first_name, user_last_name, user_email) VALUES(%s, %s, %s, %s);
            """, (user_id, first_name, last_name, email,))

    cur.execute("""
            INSERT INTO client_phone(user_id, user_phone_number) VALUES(%s, %s);
            """, (user_id, phone_number,))
    conn.commit()


def add_phone_number(user_id, phone_number):
    cur.execute("""
            INSERT INTO client_phone(user_id, user_phone_number) VALUES(%s, %s); 
            """, (user_id, phone_number,))
    conn.commit()


def update_client_info(user_id, first_name=None, last_name=None, email=None, phone_number=None, old_phone_number=None):
    if old_phone_number != None:
        cur.execute("""
                UPDATE client_phone 
                SET 
                user_phone_number = %s 
                WHERE 
                user_phone_number = %s; 
                """, (phone_number, old_phone_number,))

    if first_name != None:
        cur.execute("""
                UPDATE client_info 
                SET 
                user_first_name = %s
                WHERE
                user_id = %s
                """, (first_name, user_id,))

    if last_name != None:
        cur.execute("""
                UPDATE client_info 
                SET 
                user_last_name = %s
                WHERE
                user_id = %s
                """, (last_name, user_id,))

    if email != None:
        cur.execute("""
                UPDATE client_info 
                SET 
                user_email = %s
                WHERE
                user_id = %s
                """, (email, user_id,))
    conn.commit()


def delete_phone(user_id, phone_number):
    cur.execute("""
            DELETE FROM client_phone WHERE user_id = %s AND user_phone_number = %s; 
            """, (user_id, phone_number,))
    conn.commit()


def delete_client(user_id):
    cur.execute("""
            DELETE FROM client_phone WHERE user_id = %s;
            DELETE FROM client_info WHERE user_id = %s;
            """, (user_id, user_id,))
    conn.commit()


def find_client(first_name=None, last_name=None, email=None, phone_number=None):
    cur.execute("""
                    SELECT user_first_name, user_last_name, user_email, user_phone_number FROM client_info ci
                    LEFT JOIN client_phone cp ON ci.user_id = cp.user_id
                    WHERE 
                    user_first_name = %s AND user_last_name = %s AND user_email = %s AND user_phone_number = %s;
                    """, (first_name, last_name, email, phone_number,))
    pprint(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database='clients', user='postgres', password='120498') as conn:
        with conn.cursor() as cur:
             #drop_db()
             #create_db()
             #add_client()
             #add_phone_number()
             #update_client_info()
             #delete_phone()
             #delete_client()
             #find_client()

    conn.close()