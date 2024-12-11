from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime

# Main Application Window
root = Tk()
root.title("Pesos Loaning System")
root.geometry("800x600")
root.config(bg="#B0BEC5")

# Database Connection
def db_connection():
    return sqlite3.connect('loan_system.db')

# Function to Create Tables if they don't exist
def create_tables():
    conn = db_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS loan_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrower_name TEXT,
        loan_amount REAL,
        loan_term INTEGER,
        interest_rate REAL,
        loan_status TEXT,
        date TEXT,
        monthly_payment REAL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS deleted_ids (
        id INTEGER PRIMARY KEY
    )''')
    
    conn.commit()
    conn.close()

# Call the function to create tables
create_tables()

# Function to calculate monthly payment
def calculate_monthly_payment(loan_amount, interest_rate, loan_term):
    if loan_term <= 0:
        return 0
    # Convert interest_rate from percentage to decimal
    interest_rate = interest_rate / 100
    # Simple interest calculation for monthly payment
    monthly_payment = ((loan_amount * interest_rate) + loan_amount) / loan_term
    return round(monthly_payment, 2)

# Add a new loan record
def add_record():
    if borrower_name.get() == "" or loan_amount.get() == "" or loan_term.get() == "" or interest_rate.get() == "" or loan_status.get() == "":
        return  # Prevent adding empty records

    conn = db_connection()
    c = conn.cursor()

    # Check if there are any deleted IDs available for reuse
    c.execute("SELECT id FROM deleted_ids LIMIT 1")
    deleted_id = c.fetchone()

    if deleted_id:
        # If a deleted ID exists, use it
        record_id = deleted_id[0]
        c.execute("DELETE FROM deleted_ids WHERE id=?", (record_id,))
    else:
        # Otherwise, insert a new record with auto-incremented ID
        record_id = None  # Let SQLite handle the ID automatically

    # Calculate monthly payment
    if loan_status.get() == "Settled":
        monthly_payment = 0
        total_amount_paid = 0
    else:
        monthly_payment = calculate_monthly_payment(float(loan_amount.get()), float(interest_rate.get()), int(loan_term.get()))
        total_amount_paid = round(monthly_payment * int(loan_term.get()), 2)

    # Insert the record into the database with the current date
    c.execute("INSERT INTO loan_records (id, borrower_name, loan_amount, loan_term, interest_rate, loan_status, date, monthly_payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
              (record_id, borrower_name.get(), float(loan_amount.get()), int(loan_term.get()), float(interest_rate.get()), loan_status.get(), datetime.now().strftime('%Y-%m-%d'), monthly_payment))

    conn.commit()
    conn.close()

    # Clear the input fields
    borrower_name.delete(0, END)
    loan_amount.delete(0, END)
    loan_term.delete(0, END)
    interest_rate.delete(0, END)
    loan_status.set('')  # Reset combobox

# View all records with adjustment for "Settled" loans
def view_records():
    conn = db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM loan_records")
    records = c.fetchall()

    # Clear Treeview
    for record in tree.get_children():
        tree.delete(record)

    # Insert records into Treeview
    for record in records:
        loan_amount = record[2]
        interest_rate = record[4]
        loan_term = record[3]
        loan_status = record[5]
        monthly_payment = record[7]  # Monthly payment is at index 7 in database

        # Calculate the total amount paid (simple interest)
        if loan_status == "Settled":
            total_amount_paid = 0  # Set to 0 if the loan is settled
            monthly_payment = 0  # Set monthly payment to 0 if loan is settled
        else:
            total_amount_paid = round(monthly_payment * loan_term, 2)

        tree.insert("", END, values=(record[0], record[1], f"₱{loan_amount:,.2f}", loan_term, f"{interest_rate}%", loan_status, f"₱{total_amount_paid:,.2f}", f"₱{monthly_payment:,.2f}"))

    conn.close()

# Delete a record
def delete_record():
    try:
        record_id = int(delete_edit_id.get())
    except ValueError:
        return  # If invalid ID is entered, do nothing

    conn = db_connection()
    c = conn.cursor()

    # Delete the record from loan_records
    c.execute("DELETE FROM loan_records WHERE id=?", (record_id,))

    # Insert the deleted ID into deleted_ids for future reuse
    c.execute("INSERT INTO deleted_ids (id) VALUES (?)", (record_id,))

    conn.commit()
    conn.close()

    view_records()
    delete_edit_id.delete(0, END)  # Clear the ID field

# Update a loan record
def edit_record():
    try:
        record_id = int(delete_edit_id.get())
    except ValueError:
        return  # If invalid ID is entered, do nothing

    editor = Toplevel(root)
    editor.title("Update Loan Record")
    editor.geometry("400x400")

    conn = db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM loan_records WHERE id=?", (record_id,))
    record = c.fetchone()

    if not record:
        editor.destroy()  # If no record is found, close the editor
        return

    # Create input fields with prefilled data
    ttk.Label(editor, text="Borrower's Name", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10, sticky=W)
    borrower_name_editor = ttk.Entry(editor, width=30)
    borrower_name_editor.grid(row=0, column=1, pady=10)
    borrower_name_editor.insert(0, record[1])

    ttk.Label(editor, text="Loan Amount (in Pesos)", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky=W)
    loan_amount_editor = ttk.Entry(editor, width=30)
    loan_amount_editor.grid(row=1, column=1, pady=10)
    loan_amount_editor.insert(0, record[2])

    ttk.Label(editor, text="Loan Term (Months)", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=10, sticky=W)
    loan_term_editor = ttk.Entry(editor, width=30)
    loan_term_editor.grid(row=2, column=1, pady=10)
    loan_term_editor.insert(0, record[3])

    ttk.Label(editor, text="Interest Rate (%)", font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=10, sticky=W)
    interest_rate_editor = ttk.Entry(editor, width=30)
    interest_rate_editor.grid(row=3, column=1, pady=10)
    interest_rate_editor.insert(0, record[4])

    ttk.Label(editor, text="Loan Status", font=("Arial", 12)).grid(row=4, column=0, padx=20, pady=10, sticky=W)
    loan_status_editor = ttk.Combobox(editor, values=["Approved", "Rejected", "Settled"], width=30)
    loan_status_editor.grid(row=4, column=1, pady=10)
    loan_status_editor.set(record[5])

    # Save updated loan record with new date
    def save_update():
        # Calculate updated monthly payment
        if loan_status_editor.get() == "Settled":
            monthly_payment = 0
            total_amount_paid = 0
        else:
            monthly_payment = calculate_monthly_payment(float(loan_amount_editor.get()), float(interest_rate_editor.get()), int(loan_term_editor.get()))
            total_amount_paid = round(monthly_payment * int(loan_term_editor.get()), 2)

        c.execute("""UPDATE loan_records SET
                        borrower_name = ?, loan_amount = ?, loan_term = ?, interest_rate = ?, loan_status = ?, monthly_payment = ?
                    WHERE id = ?""", 
                  (borrower_name_editor.get(), float(loan_amount_editor.get()), int(loan_term_editor.get()), 
                   float(interest_rate_editor.get()), loan_status_editor.get(), monthly_payment, record_id))

        conn.commit()
        conn.close()
        editor.destroy()
        view_records()

    ttk.Button(editor, text="Save Changes", command=save_update).grid(row=5, column=0, columnspan=2, pady=20)

# UI Elements
ttk.Label(root, text="Borrower's Name", font=("Arial", 12), background="#B0BEC5").grid(row=0, column=0, padx=20, pady=10, sticky=W)
borrower_name = ttk.Entry(root, width=30)
borrower_name.grid(row=0, column=1, pady=10)

ttk.Label(root, text="Loan Amount (in Pesos)", font=("Arial", 12), background="#B0BEC5").grid(row=1, column=0, padx=20, pady=10, sticky=W)
loan_amount = ttk.Entry(root, width=30)
loan_amount.grid(row=1, column=1, pady=10)

ttk.Label(root, text="Loan Term (Months)", font=("Arial", 12), background="#B0BEC5").grid(row=2, column=0, padx=20, pady=10, sticky=W)
loan_term = ttk.Entry(root, width=30)
loan_term.grid(row=2, column=1, pady=10)

ttk.Label(root, text="Interest Rate (%)", font=("Arial", 12), background="#B0BEC5").grid(row=3, column=0, padx=20, pady=10, sticky=W)
interest_rate = ttk.Entry(root, width=30)
interest_rate.grid(row=3, column=1, pady=10)

ttk.Label(root, text="Loan Status", font=("Arial", 12), background="#B0BEC5").grid(row=4, column=0, padx=20, pady=10, sticky=W)
loan_status = ttk.Combobox(root, values=["Approved", "Rejected", "Settled"], width=30)
loan_status.grid(row=4, column=1, pady=10)

# Buttons for Actions
ttk.Button(root, text="Add Loan", command=add_record).grid(row=5, column=0, pady=20)
ttk.Button(root, text="View All Loans", command=view_records).grid(row=5, column=1, pady=20)

# Treeview for displaying loan records
tree = ttk.Treeview(root, columns=("ID", "Borrower", "Loan Amount", "Term", "Interest Rate", "Status", "Total Paid", "Monthly Payment"), show="headings")
tree.grid(row=6, column=0, columnspan=2, pady=20, sticky="nsew")

# Set headings for treeview and center the text
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Borrower", text="Borrower Name", anchor=CENTER)
tree.heading("Loan Amount", text="Loan Amount", anchor=CENTER)
tree.heading("Term", text="Term (Months)", anchor=CENTER)
tree.heading("Interest Rate", text="Interest Rate", anchor=CENTER)
tree.heading("Status", text="Status", anchor=CENTER)
tree.heading("Total Paid", text="Total Amount Paid", anchor=CENTER)
tree.heading("Monthly Payment", text="Monthly Payment", anchor=CENTER)

# Set column alignments to center text
tree.column("ID", anchor=CENTER, width=50)
tree.column("Borrower", anchor=CENTER, width=150)
tree.column("Loan Amount", anchor=CENTER, width=100)
tree.column("Term", anchor=CENTER, width=100)
tree.column("Interest Rate", anchor=CENTER, width=100)
tree.column("Status", anchor=CENTER, width=100)
tree.column("Total Paid", anchor=CENTER, width=150)
tree.column("Monthly Payment", anchor=CENTER, width=150)

# Entry field for deleting or updating a record by ID
ttk.Label(root, text="Enter Loan ID to Delete or Update", font=("Arial", 12), background="#B0BEC5").grid(row=7, column=0, padx=20, pady=10, sticky=W)
delete_edit_id = ttk.Entry(root, width=30)
delete_edit_id.grid(row=7, column=1, pady=10)

ttk.Button(root, text="Delete Loan", command=delete_record).grid(row=8, column=0, pady=20)
ttk.Button(root, text="Edit Loan", command=edit_record).grid(row=8, column=1, pady=20)

# Run the main loop
root.mainloop()
