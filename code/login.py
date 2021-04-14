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
          bg="blue", width=300).pack()
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
    Button(root2, text="Login", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=login_verification).pack()
    Label(root2, text="")


def logged_destroy():
    logged_message.destroy()
    root2.destroy()


def failed_destroy():
    failed_message.destroy()


def user_exists_destroy():
    user_exists_message.destroy()


def logged():
    global logged_message
    logged_message = Toplevel(root2)
    logged_message.title("Welcome")
    logged_message.geometry("500x200")
    Label(logged_message, text="Login Successfully!... Welcome {} ".format(
        username_verification.get()), fg="green", font="bold").pack()
    Label(logged_message, text="").pack()
    Button(logged_message, text="Create Note", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=new_note_page).pack()
    Button(logged_message, text="Edit Note", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=exist_note_page).pack()
    Button(logged_message, text="Logout", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=logged_destroy).pack()


def failed():
    global failed_message
    failed_message = Toplevel(root2)
    failed_message.title("Invalid Message")
    failed_message.geometry("500x100")
    Label(failed_message, text="Invalid Username or Password",
          fg="red", font="bold").pack()
    Label(failed_message, text="").pack()
    Button(failed_message, text="Ok", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=failed_destroy).pack()


def user_exists():
    global user_exists_message
    user_exists_message = Toplevel(root2)
    user_exists_message.title("Invalid Username")
    user_exists_message.geometry("500x100")
    Label(user_exists_message, text="Username already exists",
          fg="red", font="bold").pack()
    Label(user_exists_message, text="").pack()
    Button(user_exists_message, text="Ok", bg="blue", fg='white', relief="groove",
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
        "Login System", "Do you want to exit the system")
    if wayOut > 0:
        root.destroy()
        return


def create_user():
    user_new = username_new.get()
    pass_new = password_new.get()
    sql_insert = "insert into users.users (username, password) values (%s, %s)"
    sql_check = "SELECT username, COUNT(*) FROM users.users WHERE username = %s"
    cursordb.execute(sql_check, (user_new,))
    results = cursordb.fetchall()
    row_count = cursordb.rowcount
    if row_count == 0:
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
          bg="blue", width=300).pack()
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
    Button(root2, text="Login", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=create_user).pack()
    Label(root2, text="")


#################################################
# in the final version of the app
# files will be uploaded in bucket
# with the name of the user (replacing the firstpybucket)
# when a new user is registered
# new bucket is created
# when logged in - variable will hold the name of the user
# which will be the name of the bucket
######################################################
def create_note():
    note = content.get()
    file_name = file_name_temp.get()
    # file_name = f'{file_name}.txt'
    file_name = f'{file_name}.txt'
    user_note = username_verification.get()
    file = aws_app.create_temp_file(file_name, note)
    aws_app.upload_file(username_verification.get(), file)
    print("note saved")


def new_note_page():
    global note
    note = Toplevel(root)
    note.title("Note")
    note.geometry("900x800")
    note.config(bg="white")
    tc = ttk.Notebook(note)

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
    Entry(tab, textvariable=content).pack()
    Button(tab, text="Add", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=create_note).pack()


def delete_and_update_note(index):
    # print(note_list)
    # print(index)
    aws_app.delete_reminder(username_verification.get(), note_list[index])
    # print(content_list[index].get())
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
    # print(index)
    aws_app.delete_reminder(username_verification.get(), note_list[index])
    note_list_new = aws_app.display_all_reminders(username_verification.get())
    print(note_list_new)
    print('note deleted')


def exist_note_page():
    global note
    note = Toplevel(root)
    note.title("Note")
    note.geometry("900x800")
    note.config(bg="white")
    tc = ttk.Notebook(note)
    global content, content_list, note_list
    note_list = aws_app.display_all_reminders(username_verification.get())

    # if statement here
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
                  textvariable=content_list[index]).pack(fill='both')

            Button(tab, text="Save", bg="blue", fg='white', relief="groove",
                   font=('arial', 12, 'bold'), command=partial(delete_and_update_note, index)).pack()

            Button(tab, text="Delete", bg="blue", fg='white', relief="groove",
                   font=('arial', 12, 'bold'), command=partial(delete_note, index)).pack()
    else:
        ttk.Label(note,
                  text="No notes. Please create a New Note").pack(fill="both")
        Button(note, text="Create Note", bg="blue", fg='white', relief="groove",
               font=('arial', 12, 'bold'), command=new_note_page).pack()


def main_display():
    global root
    root = Tk()
    root.config(bg="white")
    root.title("Login System")
    root.geometry("500x500")
    Label(root, text='Welcome to Log In System',  bd=20, font=('arial', 20, 'bold'), relief="groove", fg="white",
          bg="blue", width=300).pack()
    Label(root, text="").pack()

    Button(root, text='Log In', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="white",
           bg="blue", command=login).pack()
    Label(root, text="").pack()

    Button(root, text='Register', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="white",
           bg="blue", command=register).pack()
    Label(root, text="").pack()

    Button(root, text='Exit', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="white",
           bg="blue", command=Exit).pack()
    Label(root, text="").pack()


main_display()
root.mainloop()
