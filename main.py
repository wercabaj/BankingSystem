import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()


def menu():
    print("""1. Create an account
        2. Log into account
        0. Exit""")

def dont_exist(user_enter):
    total = 0
    tab = user_enter.split()
    for i in range(len(tab)):
        if i % 2 == 0:
            new_value = int(tab[i]) * 2
            if new_value > 9:
                new_value = new_value - 9
            tab[i] = str(new_value)
        total += int(tab[i])
    if total % 10 == 0:
        return False
    else:
        return True

def logged_menu(data, choice):
    choice = -1
    while choice != 0:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            print()
            cur.execute("SELECT balance FROM card WHERE number = (?);", (data[0]))
            balance = cur.fetchall()
            print("Balance:", balance)
            print()
        elif choice == 2:
            print("Enter income:")
            income = int(input())
            cur.execute("SELECT balance FROM card WHERE number = (?);", [data[0]])
            balance = cur.fetchall()
            cur.execute("UPDATE card SET balance = (?) WHERE number = (?);", (income + balance[0][0], data[0]))
            conn.commit()
            print("Income was added!")
        elif choice == 3:
            print("Transfer")
            print("Enter card number:")
            user_enter = input()
            check = False
            cur.execute("SELECT number FROM card")
            sql_data = cur.fetchall()
            for d in sql_data:
                if d[0] == user_enter:
                    check = True
                    break
            if check:
                if data[0] == user_enter:
                    print("You can't transfer money to the same account!")
                else:
                    print("Enter how much money you want to transfer:")
                    transfer = int(input())
                    cur.execute("SELECT balance FROM card WHERE number = (?);", [data[0]])
                    s_balance = cur.fetchall()[0][0]
                    if transfer > s_balance:
                        print("Not enough money!")
                    else:
                        s_balance -= transfer
                        cur.execute("UPDATE card SET balance = (?) WHERE number = (?);", (s_balance, data[0]))
                        conn.commit()
                        
                        cur.execute("SELECT balance FROM card WHERE number = (?);", [user_enter])
                        r_balance = cur.fetchall()[0][0]
                        r_balance += transfer
                        
                        cur.execute("UPDATE card SET balance = (?) WHERE number = (?);", (r_balance, user_enter))
                        conn.commit()
                        print("Success!")
                            elif user_enter[0] != '4':
                                print("Such a card does not exist.")
                                    elif dont_exist(user_enter):
                                        print("Probably you made a mistake in the card number. Please try again!")
                                            else:
                                                print("Such a card does not exist.")
                                                    elif choice == 4:
                                                        print("The account has been closed!")
                                                        cur.execute("DELETE FROM card WHERE number = (?);", [data[0]])
                                                        conn.commit()
                                                            elif choice == 5:
                                                                print()
                                                                print("You have successfully logged out!")
                                                                print()
                                                                choice = -1
                                                                    return choice
                                                                        else:
                                                                            choice = 0
                                                                                return choice


def luhn_algoritm(card_number):
    new_card_number = list(card_number)
    new_value = 0
    total = 0
    x = 0
    for i in range(15):
        if i % 2 == 0:
            new_value = int(new_card_number[i]) * 2
            if new_value > 9:
                new_value = new_value - 9
            new_card_number[i] = str(new_value)
        total += int(new_card_number[i])
    for i in range(10):
        if (total + i) % 10 == 0:
            x = i
            break
    card_number = card_number + str(x)
    return card_number


def generate_card_number():
    random.seed()
    card_number = "400000"
    for i in range(9):
        r = random.randint(0, 9)
        card_number += str(r)
    card_number = luhn_algoritm(card_number)
    cur.execute("SELECT number FROM card")
    sql_data = cur.fetchall()
    if card_number not in sql_data:
        return card_number
    else:
        generate_card_number()


def create_account():
    random.seed()
    card_number = generate_card_number()
    PIN = ""
    for i in range(4):
        r = random.randint(0, 9)
        PIN += str(r)
    print()
    print("Your card has been created")
    print("Your card number:")
    print(card_number)
    print("Your card PIN:")
    print(PIN)
    print()
    return card_number, PIN


logged = False
choice = -1
card_id = 1
while choice != 0:
    menu()
    choice = int(input())
    if choice == 1:
        card_number, PIN = create_account()
        cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (card_id, card_number, PIN, 0))
        conn.commit()
        card_id += 1
    elif choice == 2:
        print()
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        PIN = input()
        cur.execute("SELECT number, pin, balance FROM card")
        data = cur.fetchall()
        conn.commit()
        for i in range(len(data)):
            if card_number == data[i][0]:
                if PIN == data[i][1]:
                    logged = True
                    print()
                    print("You have successfully logged in!")
                    print()
                    new_data = []
                    new_data.append(data[i][0])
                    new_data.append(data[i][1])
                    new_data.append(data[i][2])
        if logged == True:
            choice = logged_menu(new_data, choice)
        else:
            print()
            print("Wrong card number or PIN!")
            print()
        logged = False

print()
print("Bye!")

conn.close()
