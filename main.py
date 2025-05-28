# Final Enhanced Restaurant Management System with PDF Generation, Dropdown, Registration, Calculator Tool, and Validations
from tkinter import *
from tkinter import ttk
import random
from datetime import datetime
from tkinter import messagebox
import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def main():
    win = Tk()
    app = LoginPage(win)
    win.mainloop()

class LoginPage:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1350x750+0+0")
        self.win.title("Restaurant Management System")

        style = ttk.Style()
        style.theme_use('clam')

        self.title_label = ttk.Label(self.win, text="Restaurant Management System", font=('Arial', 35, "bold"), background="lightgrey")
        self.title_label.pack(side=TOP, fill=X)

        self.main_frame = ttk.Frame(self.win)
        self.main_frame.place(x=250, y=150, width=800, height=450)

        self.login_lbl = ttk.Label(self.main_frame, text="Login", anchor=CENTER, font=('sans-serif', 25, 'bold'))
        self.login_lbl.pack(side=TOP, fill=X, pady=10)

        self.entry_frame = ttk.LabelFrame(self.main_frame, text="Enter Details", padding=20)
        self.entry_frame.pack(fill=BOTH, expand=TRUE)

        username = StringVar()
        password = StringVar()

        ttk.Label(self.entry_frame, text="Enter Username:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(self.entry_frame, textvariable=username).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.entry_frame, text="Enter Password:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(self.entry_frame, textvariable=password, show="*").grid(row=1, column=1, padx=5, pady=5)

        def check_login():
            if not username.get() or not password.get():
                messagebox.showerror("Input Error", "Both fields are required.")
                return
            if os.path.exists("users.txt"):
                with open("users.txt", "r") as f:
                    for line in f:
                        user, pw = line.strip().split(",")
                        if user == username.get() and pw == password.get():
                            self.billing_btn.config(state="normal")
                            return
            messagebox.showerror("Error!", "Invalid login credentials.")

        def reset():
            username.set("")
            password.set("")

        def billing_sect():
            self.newWindow = Toplevel(self.win)
            self.app = Window2(self.newWindow)

        def register():
            if not username.get() or not password.get():
                messagebox.showerror("Input Error", "Username and Password cannot be empty.")
                return
            with open("users.txt", "a") as f:
                f.write(f"{username.get()},{password.get()}\n")
            messagebox.showinfo("Success", "Registration successful!")
            reset()

        btn_frame = ttk.Frame(self.entry_frame)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Login", command=check_login).grid(row=0, column=0, padx=10)
        self.billing_btn = ttk.Button(btn_frame, text="Billing", command=billing_sect, state="disabled")
        self.billing_btn.grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Reset", command=reset).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Register", command=register).grid(row=0, column=3, padx=10)

class Window2:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1320x750+0+0")
        self.win.title("Restaurant Management System")

        style = ttk.Style()
        style.theme_use('clam')

        ttk.Label(self.win, text="Restaurant Management System", font=('Arial', 30, 'bold')).pack(side=TOP, fill=X, pady=10)

        bill_no = random.randint(100, 9999)
        bill_no_tk = IntVar(value=bill_no)

        calc_var = StringVar()
        cust_nm = StringVar()
        cust_cot = StringVar()
        date_pr = StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        item_qty = StringVar()
        cone = StringVar()

        total_list = []
        self.grd_total = 0

        self.menu_items = {
            "Burger": 120,
            "Pizza": 250,
            "Pasta": 180,
            "Sandwich": 90,
            "Cold Drink": 40
        }

        entry_frame = ttk.LabelFrame(self.win, text="Customer and Order Details", padding=20)
        entry_frame.place(x=20, y=95, width=500, height=620)

        def form_row(label, var, row, readonly=False):
            ttk.Label(entry_frame, text=label).grid(row=row, column=0, sticky=W, pady=5)
            state = 'readonly' if readonly else 'normal'
            ttk.Entry(entry_frame, textvariable=var, state=state).grid(row=row, column=1, pady=5, padx=5)

        form_row("Bill Number", bill_no_tk, 0, readonly=True)
        form_row("Customer Name", cust_nm, 1)
        form_row("Customer Contact", cust_cot, 2)
        form_row("Date", date_pr, 3, readonly=True)

        ttk.Label(entry_frame, text="Item Purchased").grid(row=4, column=0, sticky=W, pady=5)
        self.item_selector = ttk.Combobox(entry_frame, values=list(self.menu_items.keys()), state="readonly")
        self.item_selector.grid(row=4, column=1, pady=5, padx=5)
        self.item_selector.bind("<<ComboboxSelected>>", lambda e: cone.set(self.menu_items[self.item_selector.get()]))

        form_row("Item Quantity", item_qty, 5)
        form_row("Cost of One", cone, 6, readonly=True)

        def default_bill():
            self.bill_txt.delete("1.0", END)
            self.bill_txt.insert(END, f"Flavor Fusion\n7 Street, Badaun\nContact: +919845228457\n")
            self.bill_txt.insert(END, f"Bill Number: {bill_no_tk.get()}\n{'='*60}\n")

        def genbill():
            if not cust_nm.get() or not cust_cot.get().isdigit() or len(cust_cot.get()) != 10:
                messagebox.showerror("Input Error", "Enter a valid 10-digit contact and name.")
                return
            self.bill_txt.insert(END, f"Customer Name : {cust_nm.get()}\nCustomer Contact : {cust_cot.get()}\nDate : {date_pr.get()}\n")
            self.bill_txt.insert(END, f"{'='*60}\nProduct Name\tQuantity\tPrice\tTotal\n{'='*60}\n")
            self.add_btn.config(state="normal")
            self.total_btn.config(state="normal")

        def add_func():
            if not self.item_selector.get() or not item_qty.get().isdigit():
                messagebox.showerror("Error!", "All fields must be filled correctly.")
                return
            qty = int(item_qty.get())
            cost = int(cone.get())
            total = qty * cost
            total_list.append(total)
            self.bill_txt.insert(END, f"{self.item_selector.get()}\t{qty}\t{cost}\t{total}\n")

        def total_func():
            self.grd_total = sum(total_list)
            self.bill_txt.insert(END, f"{'='*60}\nGrand Total: Rs.{self.grd_total}\n{'='*60}\n")
            self.save_btn.config(state="normal")

        def clear_func():
            cust_nm.set("")
            cust_cot.set("")
            item_qty.set("")
            cone.set("")

        def reset_func():
            total_list.clear()
            self.grd_total = 0
            default_bill()
            self.add_btn.config(state="disabled")
            self.total_btn.config(state="disabled")
            self.save_btn.config(state="disabled")

        def save_func():
            filename = f"bill_{bill_no_tk.get()}.pdf"
            c = canvas.Canvas(filename, pagesize=A4)
            text = self.bill_txt.get("1.0", END).split('\n')
            y = 800
            for line in text:
                c.drawString(50, y, line)
                y -= 20
            c.save()
            messagebox.showinfo("Saved", f"PDF saved as {filename}")

        def open_calculator():
            calc_win = Toplevel(self.win)
            calc_win.title("Calculator")
            calc_var = StringVar()
            Entry(calc_win, textvariable=calc_var, font=('Arial', 18), bd=10, relief=RIDGE, justify=RIGHT).grid(row=0, column=0, columnspan=4)
            buttons = [
                ["7", "8", "9", "+"],
                ["4", "5", "6", "-"],
                ["1", "2", "3", "*"],
                ["0", ".", "=", "/"],
                ["C"]
            ]
            def click(event):
                b = event.widget.cget("text")
                if b == "=":
                    try:
                        result = eval(calc_var.get())
                        calc_var.set(result)
                    except:
                        calc_var.set("Error")
                elif b == "C":
                    calc_var.set("")
                else:
                    calc_var.set(calc_var.get() + b)
            for i in range(len(buttons)):
                for j in range(len(buttons[i])):
                    btn = Button(calc_win, text=buttons[i][j], font=('Arial', 15), width=5, height=2)
                    btn.grid(row=i+1, column=j)
                    btn.bind("<Button-1>", click)

        btn_frame = ttk.Frame(entry_frame)
        btn_frame.grid(row=7, columnspan=2, pady=20)

        self.add_btn = ttk.Button(btn_frame, text="Add", command=add_func, state="disabled")
        self.add_btn.grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Generate", command=genbill).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Clear", command=clear_func).grid(row=0, column=2, padx=5)
        self.total_btn = ttk.Button(btn_frame, text="Total", command=total_func, state="disabled")
        self.total_btn.grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Reset", command=reset_func).grid(row=1, column=1, padx=5, pady=5)
        self.save_btn = ttk.Button(btn_frame, text="Save PDF", command=save_func, state="disabled")
        self.save_btn.grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(btn_frame, text="Open Calculator", command=open_calculator).grid(row=2, column=0, columnspan=3, pady=5)

        self.bill_frame = ttk.LabelFrame(self.win, text="Bill Area")
        self.bill_frame.place(x=550, y=100, width=720, height=600)

        self.bill_txt = Text(self.bill_frame, font=("Courier New", 12))
        self.bill_txt.pack(fill=BOTH, expand=True)
        default_bill()

if __name__ == "__main__":
    main()
