#Jehu Gonzaga BSIT 2-A
import tkinter as tk

def add_item():
    item = entry.get().strip()  
    if item:  
        listbox.insert(tk.END, item)
        entry.delete(0, tk.END) 

def remove_item():
    selected_index = listbox.curselection()  
    if selected_index: 
        listbox.delete(selected_index[0])  

def clear_list():
    listbox.delete(0, tk.END)  

root = tk.Tk()
root.title("Listbox Example")

entry = tk.Entry(root)
entry.pack(pady=10)

add_button = tk.Button(root, text="Add", command=add_item)
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove", command=remove_item)
remove_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_list)
clear_button.pack(pady=5)

listbox = tk.Listbox(root)
listbox.pack(pady=10)

root.mainloop()
