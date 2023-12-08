import sqlite3
import hashlib
import random

def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()

with sqlite3.connect('Casino_db.db') as db:
    cursor = db.cursor()

    # query = """
    # CREATE TABLE IF NOT EXISTS users(
    #     id INTEGER PRIMARY KEY,
    #     name VARCHAR(30),
    #     age INTEGER(3),
    #     sex INTEGER NOT NULL DEFAULT 1,
    #     balance INTEGER NOT NULL DEFAULT 2000,
    #     login VARCHAR(15),
    #     password VARCHAR(20)
    #     );
    #
    # CREATE TABLE IF NOT EXISTS casino(
    # name VARCHAR(50),
    # description TEXT (300),
    # balance BIGINT NOT NULL DEFAULT 10000
    # )
    # """
    #
    #
    # cursor.executescript(query)

def is_registrated():
    yes_or_no = input("Do you have an account? (Yes or No): ")
    if yes_or_no.lower() == 'yes':
        log_in()


def registration():
    name = input("Name: ")
    age = int(input("Age: "))
    sex = int(input("Sex: "))
    login = input("Login: ")
    password = input("Password: ")

    try:
        db = sqlite3.connect('Casino_db.db')
        cursor = db.cursor()

        db.create_function("md5", 1, md5sum)

        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            values = [name, age, sex, login, password]

            cursor.execute("INSERT INTO users(name, age, sex, login, password) VALUES (?, ?, ?, ?, md5(?))", values)
            db.commit()
        else:
            print("The login alredy ixists")
            registration()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


def log_in():
    login = input("Login: ")
    password = input("Password: ")

    try:
        db = sqlite3.connect('Casino_db.db')
        cursor = db.cursor()

        db.create_function("md5", 1, md5sum)

        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            print("The login doesn't ixist!")
        else:
            cursor.execute("SELECT password FROM users WHERE login = ? AND password = md5(?)", [login, password])
            if cursor.fetchone() is None:
                print("The password is wrong!")
            else:
                play_casino(login)
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


def get_casino():
    while True:
        casino = input("Which casino you'd like to play at? (MaxBet or Faraon): ")
        if casino.lower() == 'maxbet':
            return 'MaxBet'
        elif casino.lower() == 'faraon':
            return 'Faraon'
        else:
            print("Please choose between 'MaxBet' and 'Faraon'. Nothing more.")

def play_casino(login):
    casino = get_casino()
    print(f"\n {casino} CASINO 🤑🤑🤑")

    try:
        db = sqlite3.connect('Casino_db.db')
        cursor = db.cursor()

        cursor.execute("SELECT age FROM users WHERE login = ? AND age >=?", [login, 18])
        if cursor.fetchone()is None:
            print("You are too young to play this kind of games, go to school!")
        else:
            bet = int(input("Bet: "))
            number = random.randint(1,100)

            balance = cursor.execute("SELECT balance FROM users WHERE login = ?", [login]).fetchone()[0]
            if balance < bet:
                print("You don't have enough money to bet!!! Go to work, fucking idiot!🤬")
            elif balance <= 0:
                print("You don't have enough money to bet!!! Go to work, fucking idiot!🤬️")
            else:
                if number <= 50:
                    cursor.execute("UPDATE users SET balance = balance - ? WHERE login = ?", [bet, login])
                    cursor.execute("UPDATE casino SET balance = balance + ? WHERE name = ?", [bet, casino])
                    print("You are out of luck. Good luck next time!😔🥹😭")

                else:
                    cursor.execute("UPDATE users SET balance = balance + ? WHERE login = ?", [bet, login])
                    cursor.execute("UPDATE casino SET balance = balance - ?  WHERE name = ?", [bet, casino])
                    print("You got lucky, congratulations! 😁😉🤩")

                db.commit()
                play_casino(login)

    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


is_registrated()
registration()
log_in()





