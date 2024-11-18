from tkinter import *
import sqlite3

def edit():
    editor = Tk()
    editor.title('Update Record from Database')
    editor.geometry("500x500")

    conn = sqlite3.connect('C:/Users/STUDENT8/mydata.db')
    c = conn.cursor()

    record_id = delete_box.get()

    if not record_id.isdigit():
        error_label = Label(editor, text="Please enter a valid ID number.")
        error_label.grid(row=0, column=0, columnspan=2)
        return

    c.execute("SELECT * FROM my_infojehu WHERE oid=?", (record_id,))
    record = c.fetchone()

    if not record:
        error_label = Label(editor, text="Record not found!")
        error_label.grid(row=0, column=0, columnspan=2)
        return

    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, pady=(10, 0))
    f_name_editor.insert(0, record[0])  # First name

    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row=0, column=0, padx=10, pady=(10, 0))

    # Last Name Entry and Label
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1, pady=(10, 0))
    l_name_editor.insert(0, record[1])  # Last name

    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row=1, column=0, padx=10, pady=(10, 0))

    # Age Entry and Label
    age_editor = Entry(editor, width=30)
    age_editor.grid(row=2, column=1, pady=(10, 0))
    age_editor.insert(0, record[2])  # Age

    age_label = Label(editor, text="Age")
    age_label.grid(row=2, column=0, padx=10, pady=(10, 0))

    # Address Entry and Label
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=3, column=1, pady=(10, 0))
    address_editor.insert(0, record[3])  # Address

    address_label = Label(editor, text="Address")
    address_label.grid(row=3, column=0, padx=10, pady=(10, 0))

    # Email Entry and Label
    email_editor = Entry(editor, width=30)
    email_editor.grid(row=4, column=1, pady=(10, 0))
    email_editor.insert(0, record[4])  # Email

    email_label = Label(editor, text="Email")
    email_label.grid(row=4, column=0, padx=10, pady=(10, 0))

    def save_update():
        updated_f_name = f_name_editor.get()
        updated_l_name = l_name_editor.get()
        updated_age = age_editor.get()
        updated_address = address_editor.get()
        updated_email = email_editor.get()

        c.execute('''UPDATE my_infojehu SET
                        f_name = ?, l_name = ?, age = ?, address = ?, email = ?
                        WHERE oid = ?''', 
                  (updated_f_name, updated_l_name, updated_age, updated_address, updated_email, record_id))

        conn.commit()
        conn.close()

        editor.destroy()

        query()

    save_btn = Button(editor, text="Save Changes", command=save_update)
    save_btn.grid(row=5, column=0, columnspan=2, pady=20, padx=10, ipadx=104)

    editor.mainloop()

     

    

def submit():
    conn = sqlite3.connect('C:/Users/STUDENT8/mydata.db')
    c = conn.cursor()

    c.execute("INSERT INTO my_infojehu VALUES (:f_name, :l_name, :age, :address, :email)",
              {
                'f_name': f_name.get(),
                'l_name': l_name.get(),
                'age': age.get(),
                'address': address.get(),
                'email': email.get(),
              })
    
    conn.commit()
    conn.close()

    # Clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    age.delete(0, END)
    address.delete(0, END)
    email.delete(0, END)

def query():
    conn = sqlite3.connect('C:/Users/STUDENT8/mydata.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM my_infojehu")
    records = c.fetchall()
    conn.close()

    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) >= 30:
            widget.grid_forget()

    print_records = ''
    for record in records:
        print_records += f"{record[0]} {record[1]} {record[2]} {record[3]} {record[4]} (ID: {record[5]})\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=30, column=0, columnspan=2)

def delete():
    conn = sqlite3.connect('C:/Users/STUDENT8/mydata.db')
    c = conn.cursor()
    c.execute("DELETE FROM my_infojehu WHERE oid=?", (delete_box.get(),))
    conn.commit()

    delete_box.delete(0, END)

    conn.close()

    query()


root = Tk()
root.title('My CRUD Project')
root.geometry("500x500")

f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)

age = Entry(root, width=30)
age.grid(row=2, column=1, padx=20)

address = Entry(root, width=30)
address.grid(row=3, column=1, padx=20)

email = Entry(root, width=30)
email.grid(row=4, column=1, padx=20)

f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0)

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

age_label = Label(root, text="Age")
age_label.grid(row=2, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=3, column=0)

email_label = Label(root, text="Email")
email_label.grid(row=4, column=0)

delete_box = Entry(root, width=30)
delete_box.grid(row=10, column=1, padx=30)

delete_box_label = Label(root, text="Select ID No.")
delete_box_label.grid(row=10, column=0)

submit_btn = Button(root, text="Add Record to Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=77)

query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=104)

delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=105)

update_btn = Button(root, text="Edit Record", command=edit)
update_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=105)

root.mainloop()
