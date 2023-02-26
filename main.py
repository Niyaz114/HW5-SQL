import psycopg2

# Создаем базу данных
conn = psycopg2.connect(database='clients', user='postgres', password='120498')  # Подключение к бд
with conn.cursor() as cur:  # Создаем курсор
    def create_tables(conn):
            cur.execute("""CREATE TABLE IF NOT EXISTS clients (
                        client_id SERIAL PRIMARY KEY,
                        name VARCHAR(15) NOT NULL, 
                        surname VARCHAR(15) NOT NULL, 
                        email VARCHAR(25) UNIQUE);
                        CREATE TABLE IF NOT EXISTS phone_numbers (
                        phone_number_id SERIAL PRIMARY KEY,
                        client_id INTEGER REFERENCES clients(client_id), 
                        phone_number VARCHAR(15) NOT NULL);""")
            conn.commit()
            print('Таблицы в базе созданы.')
    print()


def add_new_client(conn, name, surname, email, phone_number): # Добавление клиента
            cur.execute("""INSERT INTO clients (name, surname, email) 
                        VALUES ('{name}','{surname}','{email}'); 
                        SELECT * FROM clients;""")
            client_id = cur.fetchall()[-1][0]
            if phone_number:
                cur.execute("""INSERT INTO phone_numbers (client_id, phone_number) 
                            VALUES ({client_id}, '{phone_number}');""")
                conn.commit()
                print(f'Новый клиент добавлен!')
            print()

def add_phone_number(conn, client_id, phone_number): # Добавляем номер телефона
            cur.execute("""INSERT INTO phone_numbers (client_id, phone_number)
                        VALUES ({client_id},'{phone_number}');""")
            conn.commit()
            print(f'Дополнительный телефон добавлен')
            print()

def update_client_info(conn, client_id, name=None, surname=None, email=None, phone_number=None): # Меняем данные клиента
        if name:
            print("Меняем имя")
            cur.execute("""
                    UPDATE client set name = %s  Where id = %s ;
                    """, (name, client_id))
        if surname:
            print("Меняем фамилию")
            cur.execute("""
                    UPDATE client.users set last_name = %s  Where id = %s ;
                    """, (surname, client_id))
        if email:
            print("Меняем почту")
            cur.execute("""
                    UPDATE client.users set email = %s  Where id = %s ;
                    """, (email, client_id))
        conn.commit()
        if phone_number:
            cur.execute("""
                    SELECT id, phone FROM client.phone WHERE user_id=%s;
                    """, (client_id,))
            for phone_number in cur.fetchall():
                print('Телефоны пользователя:', phone_number)
            id_phone = input('Укажите id номера телефона, который нужно поменять:')
            cur.execute("""
                    UPDATE client.phone set phone = %s  Where user_id = %s and id = %s;
                    """, (phone_number, client_id, id_phone))
            conn.commit()
        return print("Данные успешно поменяны")

def del_phone_number(conn): # Удаляем телефон клиента
            cur.execute("""SELECT * FROM clients WHERE client_id={client_id};""")
            client_info = cur.fetchone()
            print(f'Клиент {client_info[1]} {client_info[2]}')
            print('Номера телефонов:')
            cur.execute("""SELECT * FROM phone_numbers WHERE client_id={client_id};""")
            client_phones = cur.fetchall()
            print('id'.center(5) + '-' + 'Номер телефона'.center(16))
            for client_phone in client_phones:
                print(str(client_phone[0]).center(5) + '-' + client_phone[2].center(16))
            phone_number_id = input('Введите id удаляемого номера: ')
            cur.execute("""DELETE FROM phone_numbers WHERE phone_number_id={phone_number_id};""")
            conn.commit()
            print('Номер телефона удален')


def del_client(conn): # Удаляем клиента из базы
            cur.execute("""DELETE FROM phone_numbers WHERE client_id={client_id};
                        DELETE FROM clients WHERE client_id={client_id};""")
            conn.commit()
            print('Клиент удален из базы')
            print()

def find_client(conn, name=None, surname=None, email=None, phone_number=None): # Находим клиента в базе
    print('*** найти клиента по его данным (имени, фамилии, email-у или телефону) ***')
    key = input('Введите данные для поиска: ')
    cur.execute("""SELECT DISTINCT clients.client_id, name, surname, email, phone_number
                        FROM clients
                        JOIN phone_numbers
                        ON clients.client_id = phone_numbers.client_id 
                        WHERE name LIKE '%{key}%' OR surname LIKE '%{key}%' OR email LIKE '%{key}%' 
                        OR phone_number LIKE '%{key}%';""")
    clients_info = cur.fetchall()
    print(clients_info)
    print('id'.center(5) + 'Имя'.center(15) + 'Фамилия'.center(15) +
                  'e-mail'.center(25) + 'Номер телефона'.center(16))
    print('-' * 82)
    for client in clients_info:
            print(str(client[0]).center(5) + client[1].center(15) +
                      client[2].center(15) + client[3].center(25) + client[4].center(16))
            print()
def main():
    functions = {1: create_tables,
                 2: add_new_client,
                 3: add_phone_number,
                 4: update_client_info,
                 5: del_phone_number,
                 6: del_client,
                 7: find_client
                 }
    print('1 - Функция, создающая структуру БД (таблицы)\n'
          '2 - Функция, позволяющая добавить нового клиента\n'
          '3 - Функция, позволяющая добавить телефон для существующего клиента\n'
          '4 - Функция, позволяющая изменить данные о клиенте\n'
          '5 - Функция, позволяющая удалить телефон для существующего клиента\n'
          '6 - Функция, позволяющая удалить существующего клиента\n'
          '7 - Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)\n')
    function = int(input('Выберите номер функции: '))
    functions[function]()


if __name__ == '__main__':
    while True:
        main()
conn.close()