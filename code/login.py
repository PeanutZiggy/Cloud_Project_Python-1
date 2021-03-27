from tkinter import *
from tkinter import ttk as ttk
import tkinter.messagebox
import mysql.connector
import aws_app


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


def logged():
    global logged_message
    logged_message = Toplevel(root2)
    logged_message.title("Welcome")
    logged_message.geometry("500x130")
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
    sql = "insert into users.users (username, password) values (%s, %s)"
    cursordb.execute(sql, [(user_new), (pass_new)])
    connectiondb.commit()
    print(cursordb.rowcount, "record inserted.")
    create_bucket(user_new, client)


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


# def retrieve_note():
#     sql = '''
#     IF object_id("note") is not null
#         PRINT "Present!"
#     ELSE
#         PRINT "Not accounted for"'''
#     cursordb.execute(sql)
#     connectiondb.commit()


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
    file_name = f'{file_name}.txt'
    user_note = username_verification.get()
    file = aws_app.create_temp_file(file_name, note)
    aws_app.upload_file('firstpybucket', file)
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


def save_note():
    note = content.get()
    file_name = file_name_temp.get()
    user_note = username_verification.get()
    file = aws_app.create_temp_file(file_name)
    # upload_file(user_note, file)
    aws_app.upload_file('firstpybucket', file)
    print("note saved")
    # sql = "insert into users.users (username, note) values (%s, %s)"
    # cursordb.execute(sql, [(user_note), (note)])
    # connectiondb.commit()
    # print(cursordb.rowcount, "note saved.")


def exist_note_page():
    global note
    note = Toplevel(root)
    note.title("Note")
    note.geometry("900x800")
    note.config(bg="white")
    tc = ttk.Notebook(note)
    note_list = aws_app.display_all_reminders('firstpybucket')

    current_content = ''
    for value in note_list:
        tab = ttk.Frame(tc)
        tc.add(tab, text=value)
        tc.pack(fill="both")
        current_content = aws_app.get_reminder_text('firstpybucket', value)

        ttk.Label(tab,
                  text=current_content).pack(fill="both")

    global content
    content = StringVar()

    Entry(note,
          textvariable=content).pack(fill='both')
    Button(note, text="Add", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=save_note).pack()
    Button(note, text="Save", bg="blue", fg='white', relief="groove",
           font=('arial', 12, 'bold'), command=save_note).pack()


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
