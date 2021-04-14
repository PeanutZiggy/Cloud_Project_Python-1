from tkinter import *
from tkinter import ttk as ttk
import tkinter.messagebox
import mysql.connector
import aws_app
from functools import partial


# connecting to the database
connectiondb = mysql.connector.connect(
    host="users.cvbmzde6kxzh.eu-west-2.rds.amazonaws.com", user="admin", passwd="Password123!", database="users")
cursordb = connectiondb.cursor()


def login():
    global root2
    root2 = Toplevel(root)
    root2.title("Account Login")
    root2.geometry("450x300")
    root2.config(bg="white")

    global username_verification
    global password_verification
    Label(root2, text='Please Enter your Account Details', bd=5, font=('arial', 12, 'bold'), relief="groove", fg="white",
          bg="#ec7211", width=300).pack()
    username_verification = StringVar()
    password_verification = StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", fg="black",
          font=('arial', 12, 'bold')).pack()
    Entry(root2, textvariable=username_verification).pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :", fg="black",
          font=('arial', 12, 'bold')).pack()
    Entry(root2, textvariable=password_verification, show="*").pack()
    Label(root2, text="").pack()
    Button(root2, text="Login", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=login_verification).pack()
    Label(root2, text="")


def logged_destroy():
    logged_message.destroy()


def failed_destroy():
    failed_message.destroy()


def user_exists_destroy():
    user_exists_message.destroy()


def no_notes_destroy():
    exist_note.destroy()


def logged():
    root2.destroy()
    global logged_message
    logged_message = Toplevel(root)
    logged_message.title("Welcome")
    logged_message.geometry("500x200")
    Label(logged_message, text="Welcome {}! ".format(
        username_verification.get()), fg="#ec7211", font="bold").pack()
    Label(logged_message, text="").pack()
    Button(logged_message, text="Create Note", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=new_note_page).pack()
    Button(logged_message, text="View Notes", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=exist_note_page).pack()
    Button(logged_message, text="Logout", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=logged_destroy).pack()


def failed():
    global failed_message
    failed_message = Toplevel(root2)
    failed_message.title("Invalid Message")
    failed_message.geometry("500x100")
    Label(failed_message, text="Invalid Username or Password",
          fg="red", font="bold").pack()
    Label(failed_message, text="").pack()
    Button(failed_message, text="Ok", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=failed_destroy).pack()


def user_exists():
    global user_exists_message
    user_exists_message = Toplevel(root2)
    user_exists_message.title("Invalid Username")
    user_exists_message.geometry("500x100")
    Label(user_exists_message, text="Username already exists",
          fg="red", font="bold").pack()
    Label(user_exists_message, text="").pack()
    Button(user_exists_message, text="Ok", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=user_exists_destroy).pack()


def login_verification():
    user_verification = username_verification.get()
    pass_verification = password_verification.get()
    sql = "select * from users.users where username = %s and password = %s"
    cursordb.execute(sql, [(user_verification), (pass_verification)])
    results = cursordb.fetchall()
    if results:
        for i in results:
            logged()
            break
    else:
        failed()


def Exit():
    wayOut = tkinter.messagebox.askyesno(
        "Notes Online", "Do you want to exit the system?")
    if wayOut > 0:
        root.destroy()
        return


def create_user():
    user_new = username_new.get()
    pass_new = password_new.get()

    sql_insert = "insert into users.users (username, password) values (%s, %s)"
    sql_check = "SELECT username, COUNT(*) FROM users.users WHERE username = %s"

    cursordb.execute(
        "SELECT username, COUNT(*) FROM users.users WHERE username = %s GROUP BY username", (user_new,))

    results = cursordb.fetchone()

    row_count = cursordb.rowcount
    print(row_count, results)
    if row_count <= 0:
        cursordb.execute(sql_insert, [(user_new), (pass_new)])
        connectiondb.commit()
        print(cursordb.rowcount, "record inserted.")
        aws_app.create_bucket(user_new, aws_app.client)
        root2.destroy()
    else:
        user_exists()


def register():
    global root2
    root2 = Toplevel(root)
    root2.title("Create Account")
    root2.geometry("450x300")
    root2.config(bg="white")

    global username_new
    global password_new

    Label(root2, text='Please Enter your New Account Details', bd=5, font=('arial', 12, 'bold'), relief="groove", fg="white",
          bg="#ec7211", width=300).pack()
    username_new = StringVar()
    password_new = StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", fg="black",
          font=('arial', 12, 'bold')).pack()
    Entry(root2, textvariable=username_new).pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :", fg="black",
          font=('arial', 12, 'bold')).pack()
    Entry(root2, textvariable=password_new, show="*").pack()
    Label(root2, text="").pack()
    Button(root2, text="Register", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=create_user).pack()
    Label(root2, text="")


def create_note():
    note = content.get()
    file_name = file_name_temp.get()
    file_name = f'{file_name}.txt'
    user_note = username_verification.get()
    file = aws_app.create_temp_file(file_name, note)
    aws_app.upload_file(username_verification.get(), file)
    print("note saved")


def new_note_page():
    global new_note
    new_note = Toplevel(root)
    new_note.title("Note")
    new_note.geometry("350x400")
    new_note.config(bg="white")
    tc = ttk.Notebook(new_note)

    tab = ttk.Frame(tc)
    tc.add(tab, text='Notebook')
    tc.pack(fill="both")

    global content
    global file_name_temp
    content = StringVar()
    file_name_temp = StringVar()

    ttk.Label(tab, text="Please put your note here").pack(fill="both")
    ttk.Label(tab, text="Name").pack(fill="both")

    Entry(tab, textvariable=file_name_temp).pack()
    ttk.Label(tab, text="Note").pack(fill="both")
    Entry(tab, textvariable=content, width=50).pack()
    Button(tab, text="Add", bg="#ec7211", fg='white', relief="raised",
           font=('arial', 12, 'bold'), command=lambda: [create_note(), new_note.destroy()]).pack()


def delete_and_update_note(index):
    aws_app.delete_reminder(username_verification.get(), note_list[index])
    print('note deleted')
    note = content_list[index].get()
    file_name = note_list[index]
    file_name = f'{file_name}.txt'
    user_note = username_verification.get()
    file = aws_app.create_temp_file(file_name, note)
    aws_app.upload_file(username_verification.get(), file)
    print("note updated")


def delete_note(index):
    print(note_list)
    aws_app.delete_reminder(username_verification.get(), note_list[index])
    note_list_new = aws_app.display_all_reminders(username_verification.get())
    print(note_list_new)
    print('note deleted')


def exist_note_page():
    global exist_note
    exist_note = Toplevel(root)
    exist_note.title("Note")
    exist_note.geometry("500x500")
    exist_note.config(bg="white")
    tc = ttk.Notebook(exist_note)
    global content, content_list, note_list
    note_list = aws_app.display_all_reminders(username_verification.get())

    if note_list:

        content = StringVar()
        content_list = ['' for i in note_list]

        current_content = ''
        for index, value in enumerate(note_list):
            content_list[index] = StringVar()
            tab = ttk.Frame(tc)
            tc.add(tab, text=value)
            tc.pack(fill="both")
            current_content = aws_app.get_reminder_text(
                username_verification.get(), value)

            ttk.Label(tab,
                      text=current_content).pack(fill="both")

            Entry(tab,
                  textvariable=content_list[index], width=50).pack(fill='both')

            Button(tab, text="Save", bg="#ec7211", fg='white', relief="raised",
                   font=('arial', 12, 'bold'), command=partial(delete_and_update_note, index)).pack()

            Button(tab, text="Delete", bg="#ec7211", fg='white', relief="raised",
                   font=('arial', 12, 'bold'), command=partial(delete_note, index)).pack()

            Button(tab, text="Exit", bg="#ec7211", fg='white', relief="raised",
                   font=('arial', 12, 'bold'), command=exist_note.destroy).pack()
    else:
        ttk.Label(exist_note,
                  text="No notes. Please create a New Note").pack(fill="both")
        Button(exist_note, text="Create Note", bg="#ec7211", fg='white', relief="raised",
               font=('arial', 12, 'bold'), command=lambda: [new_note_page(), no_notes_destroy()]).pack()


def main_display():
    global root
    root = Tk()
    root.config(bg="white")
    root.title("Notes Online")
    root.geometry("500x500")
    Label(root, text='Welcome to Notes Online',  bd=20, font=('arial', 20, 'bold'), relief="groove", fg="white",
          bg="#ec7211", width=300).pack()
    Label(root, text="").pack()

    Button(root, text='Log In', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="raised", fg="white",
           bg="#ec7211", command=login).pack()
    Label(root, text="").pack()

    Button(root, text='Register', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="raised", fg="white",
           bg="#ec7211", command=register).pack()
    Label(root, text="").pack()

    Button(root, text='Exit', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="raised", fg="white",
           bg="#ec7211", command=Exit).pack()
    Label(root, text="").pack()


main_display()
root.mainloop()
