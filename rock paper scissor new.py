from tkinter import *
from tkinter import messagebox
import sys
import tabulate
import random
import sqlite3
global no_of_games 
global count
global flag
global user

def create_database():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      username TEXT PRIMARY KEY,
                      password TEXT,
                      highest_score INTEGER DEFAULT 0
                    )''')
    connection.commit()
    connection.close()


def check_username_exists(username):
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT username FROM users WHERE username = ?''', (username,))
    result = cursor.fetchone()
    connection.close()
    return result is not None



def display():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM users''')
    rows = cursor.fetchall()
    connection.close()
    print(tabulate.tabulate(rows, headers=['username', 'password', 'highest_score'], tablefmt='grid'))


def validate_login(username, password):
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT username, password FROM users WHERE username = ? AND password = ?''', (username, password))
    result = cursor.fetchone()
    connection.close()
    return result is not None


def store_user_details(username, password):
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    connection.commit()
    connection.close()


def get_highest_score(username):
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT highest_score FROM users WHERE username = ?''', (username,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else 0

def store_highest_score(username, score):
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users SET highest_score = ? WHERE username = ?''', (score, username))
    connection.commit()
    connection.close()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.opponent = None
        self.choice = None

    def set(self, choice):
        self.choice = choice

    def display(self):
        winner.config(text=f"{self.name} WIN!!")
    
    def set_opponent(self, player):
        self.opponent = player

def display_choice():
    choice_you.config(text=player1.choice)
    choice_computer.config(text=player2.choice)

def display_score():
    score_you.config(text=player1.score)
    score_computer.config(text=player2.score)

def reset():
    global no_of_games
    global count
    player1.score = 0
    player2.score = 0
    count = 0
    display_score()

def stopmatch():
    if player1.score>player2.score:
        messagebox.showinfo("RESULT",f"{player1.name} WON THE GAME!!")
    elif player1.score<player2.score:
        messagebox.showinfo("RESULT",f"{player2.name} WON THE GAME!!")
    else:
        messagebox.showinfo("RESULT","MATCH TIE!!")
    if player1.score > get_highest_score(user):
            store_highest_score(user, player1.score)
            messagebox.showinfo("New Highest Score!", f"New highest score for {user}: {player1.score}")
            high_score_display.config(text = player1.score)
    reset()

def play():
    global count
    global no_of_games
    try:
       no_of_games
    except NameError:
       messagebox.showerror("ERROR","SELECT NO OF GAMES!!")
    if count<no_of_games:
       if player1.choice == "ROCK" and player2.choice == "PAPER":
           player2.score += 1
           player2.display()
       elif player1.choice == "ROCK" and player2.choice == "SCISSOR":
           player1.score += 1
           player1.display()
       elif player1.choice == "PAPER" and player2.choice == "ROCK":
           player1.score += 1
           player1.display()
       elif player1.choice == "PAPER" and player2.choice == "SCISSOR":
           player2.score += 1
           player2.display()
       elif player1.choice == "SCISSOR" and player2.choice == "ROCK":
           player2.score += 1
           player2.display()
       elif player1.choice == "SCISSOR" and player2.choice == "PAPER":
           player1.score += 1
           player1.display()
       else:
           winner.config(text="TIE!!")
       display_score()
       count+=1
       highest_score = get_highest_score(player1.name)
       high_score_display.config(text=highest_score)
    if count == no_of_games:
        stopmatch()
    
def exit_program():
    window.destroy()
    sys.exit()

def set_no_of_games():
    global no_of_games
    try:
        no_of_games = int(no_of_games_entry.get())
        if no_of_games <= 0:
            messagebox.showerror("Error", "Please enter a positive number of games.")
            return
        else:
            player1.score = 0
            player2.score = 0
            display_score()
    except ValueError:
        messagebox.showerror("ERROR", "ENTER A VALID NUMBER!!")
        return        
    
create_database()

flag = 0

root1 = Tk()
root1.title("Registration Window")
root1.geometry("350x150")

def register():
    username = username_entry.get()
    password = password_entry.get()
    if not check_username_exists(username):
        store_user_details(username, password)
        messagebox.showinfo("Registration Successful", "User registered successfully")
        root1.destroy()
    else:
        messagebox.showerror("Registration Failed", "Username already exists")

def cancel():
    response = messagebox.askyesno("Question", "Do you want to close the window?")
    if response:
        root1.destroy()
    else:
        messagebox.showwarning("Warning", "Please register again!!")

# Username Label and Entry
Label(root1, text="Username:").grid(row=0, column=0)
username_entry = Entry(root1)
username_entry.grid(row=0, column=1)

# Password Label and Entry
Label(root1, text="Password:").grid(row=1, column=0)
password_entry = Entry(root1)
password_entry.grid(row=1, column=1)

# Login Button
login_button = Button(root1, text="Register", command=register)
login_button.place(x=60, y=45)

# Cancel Button
cancel_button = Button(root1, text="Cancel", command=cancel)
cancel_button.place(x=140, y=45)

root1.mainloop()

root = Tk()
root.title("Login Window")
root.geometry("350x150")

def login():
    global flag
    global user
    username = username_entry.get()
    password = password_entry.get()
    if validate_login(username, password):
        user = username
        messagebox.showinfo("Login Status", "You have logged in")
        flag = 1
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def cancel():
    response = messagebox.askyesno("Question", "Do you want to close the window?")
    if response:
        sys.exit(0)
    else:
        messagebox.showwarning("Warning", "Please Login Again!!")

Label(root, text="Username:").grid(row=0, column=0)
username_entry = Entry(root)
username_entry.grid(row=0, column=1)


Label(root, text="Password:").grid(row=1, column=0)
password_entry = Entry(root, show="*")
password_entry.grid(row=1, column=1)

login_button = Button(root, text="Login", command=login)
login_button.place(x=60, y=45)

cancel_button = Button(root, text="Cancel", command=cancel)
cancel_button.place(x=140, y=45)

root.mainloop()

if flag == 1:
    window = Tk()
    window.geometry("800x800")
    window.configure(bg='#F5F5DC')

    choices = ["ROCK", "PAPER", "SCISSOR"]
    count = 0

    title = Label(window, text="ROCK PAPER SCISSORS", font=("PARISIENNE", 30), fg='#00008B')
    title.pack()
    title.place(relx=0.35, rely=0.05)

    high_score_display = Label(window, text="", fg='#00008B', bg = '#AAFACA' , height=1, width=5, font=5)
    high_score_display.pack()
    high_score_display.place(relx=0.20, rely=0.9)
    high_score_display.config(text = get_highest_score(user))

    player1 = Player("YOU")
    player2 = Player("COMPUTER")

    player1.set_opponent(player2)
    player2.set_opponent(player1)

    no_of_games_label = Label(window, text="ENTER NO OF GAMES:", fg='#00008B', height=1, width=20, font=1)
    no_of_games_label.pack()
    no_of_games_label.place(relx=0.35, rely=0.2)

    no_of_games_entry = Entry(window, width=10)
    no_of_games_entry.pack()
    no_of_games_entry.place(relx=0.5, rely=0.2)

    set_no_of_games_button = Button(window, text="Set", fg='#00008B', bg="#ccaaaa", height=1, width=5, font=5, command=set_no_of_games)
    set_no_of_games_button.pack()
    set_no_of_games_button.place(relx=0.55, rely=0.2)

    rock = Button(window, text="Rock", fg='#00008B', bg="#CCAAAA", height=3, width=15, font=10,
                command=lambda: [player1.set("ROCK"), player2.set(random.choice(choices)), display_choice(), play()])
    paper = Button(window, text="Paper", fg='#00008B', bg="#CCAAAA", height=3, width=15, font=10,
                command=lambda: [player1.set("PAPER"), player2.set(random.choice(choices)), display_choice(), play()])
    scissor = Button(window, text="Scissor", fg='#00008B', bg="#CCAAAA", height=3, width=15, font=10,
                    command=lambda: [player1.set("SCISSOR"), player2.set(random.choice(choices)), display_choice(), play()])
    exitbutton = Button(window, text="EXIT", fg='#00008B', bg="#FF5500", height=2, width=10, font=10, command=exit_program)
    resetbutton = Button(window, text="RESET", fg='#00008B', bg="#FF5500", height=2, width=10, font=10, command=reset)

    rock.pack()
    paper.pack()
    scissor.pack()
    exitbutton.pack()
    resetbutton.pack()

    rock.place(relx=0.45, rely=0.3)
    paper.place(relx=0.45, rely=0.4)
    scissor.place(relx=0.45, rely=0.5)
    resetbutton.place(relx=0.4, rely=0.85)
    exitbutton.place(relx=0.53, rely=0.85)

    you = Label(window, text=player1.name, fg='#00008B', bg = '#CCAACC', height=5, width=15, font=10)
    computer = Label(window, text=player2.name, fg='#00008B', bg = '#CCAACC', height=5, width=15, font=10)

    you.pack()
    computer.pack()

    you.place(relx=0.15, rely=0.2)
    computer.place(relx=0.75, rely=0.2)

    choice_you = Label(window, text=player1.choice, fg='#00008B', height=5, width=15, font=10)
    choice_computer = Label(window, text=player2.choice, fg='#00008B', height=5, width=15, font=10)

    choice_you.pack()
    choice_computer.pack()

    choice_you.place(relx=0.15, rely=0.4)
    choice_computer.place(relx=0.75, rely=0.4)

    score_you = Label(window, text=player1.score, fg='#00008B', height=5, width=15, font=10)
    score_computer = Label(window, text=player2.score, fg='#00008B', height=5, width=15, font=10)

    score_you.pack()
    score_computer.pack()

    score_you.place(relx=0.15, rely=0.6)
    score_computer.place(relx=0.75, rely=0.6)

    high_score = Label(window, text="HIGHEST SCORE:", fg='#00008B', bg = '#AAFACA' , height=1, width=15, font=5)
    high_score.pack()
    high_score.place(relx=0.08, rely=0.9)

    winner = Label(window, text="", fg='#00008B', bg = '#AAFACA' , height=3, width=30, font=10)
    winner.pack()
    winner.place(relx=0.4, rely=0.65)


    window.mainloop()
display()    
