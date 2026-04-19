
# Start of Lucy's Part
import tkinter as tk
from tkinter import messagebox

class Expense:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = float(amount)
        self.category = category

class BudgetManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, name, amount, category):
        new_expense = Expense(name, amount, category)
        self.expenses.append(new_expense)

    def get_total(self):
        return sum(exp.amount for exp in self.expenses)

    def get_all_expenses(self):
        report = ""
        for exp in self.expenses:
            report += f"{exp.name} ({exp.category}): ${exp.amount:.2f}\n"
        return report

class BudgetApp: # Starts the GUI class that will create the window and connect the logic 
    def __init__(self, root):
        # End of Lucy's Part
        self.root = root # The main window
        self.root.title("Budget Tracker") # Title of the window

        self.manager = BudgetManager() # Creates an instance of the BudgetManager to handle the logic

        self.build_interface() # Call to build GUI interface
        self.bind_events() # Call to bind events like button clicks and key presses
        self.refresh_view() # Call to update the display with data from logic layer

    def build_interface(self): # Builds GUI elements and layout
        self.main_frame = tk.Frame(self.root, padx=12, pady=12) # Creates a main frame with padding
        self.main_frame.pack(fill="both", expand=True) # Packs the frame to fill the window and allow it to expand

        self.build_input_section() # Call to build the input section
        self.build_action_section() # Call to build the action section
        self.build_display_section() # Call to build the display section

    def build_input_section(self): # Builds the section of the GUI where the user can enter expense data
        input_frame = tk.LabelFrame( # Creates a labeled frame for the input section
            self.main_frame, # The parent of this frame is the main frame
            text="Expense Entry", # Label for the frame
            padx=10, # Padding 
            pady=10, # Padding 
        )
        input_frame.pack(fill="x") # Packs the input frame to fill horizontally

        tk.Label(input_frame, text="Expense Name:").grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 8),
        )
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 8))

        tk.Label(input_frame, text="Amount:").grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 8),
        )
        self.amount_entry = tk.Entry(input_frame, width=30)
        self.amount_entry.grid(row=1, column=1, sticky="ew", pady=(0, 8))

        tk.Label(input_frame, text="Category:").grid(row=2, column=0, sticky="w")
        self.category_entry = tk.Entry(input_frame, width=30)
        self.category_entry.grid(row=2, column=1, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

    def build_action_section(self):
        action_frame = tk.Frame(self.main_frame, pady=12)
        action_frame.pack(fill="x")

        self.add_button = tk.Button(
            action_frame,
            text="Add Expense",
            command=self.handle_add_expense,
            bg="blue",
            fg="white",
            width=14,
        )
        self.add_button.pack(anchor="w")

    def build_display_section(self): # Builds the part of GUI that shows the list of expenses and total
        display_frame = tk.LabelFrame( # A labeled frame for the display section
            self.main_frame, # The parent of this frame is the main frame
            text="Budget Summary", # Label
            padx=10, # Padding
            pady=10, # Padding
        )
        display_frame.pack(fill="both", expand=True) # Packs the display frame to fill the space and allow it to expand

        tk.Label(display_frame, text="Expenses:").pack(anchor="w") # Label for the expenses display area, left aligned

        self.text_display = tk.Text(display_frame, height=10, width=45) # Text widget to show list of expenses
        self.text_display.pack(fill="both", expand=True, pady=(6, 10)) # Packs the text widget to fill the space. Adds vertical padding

        self.total_label = tk.Label(
            display_frame,
            text="Total: $0.00",
            font=("Arial", 12, "bold"), # Font for the total label
        )
        self.total_label.pack(anchor="e")

    def bind_events(self):
        self.root.bind("<Return>", self.handle_add_expense_event)

    def handle_add_expense_event(self, event):
        self.handle_add_expense()

    def handle_add_expense(self):
        name, amount_text, category = self.get_form_data()

        validation_error = self.validate_entry(name, amount_text) # Returns error if there is a problem
        if validation_error: # Exits the function and shows a warning if there is a validation error
            messagebox.showwarning("Input Error", validation_error) # Displays the warning message box with error message
            return 

        try: # Tries to add the expense but will catch a value error if the amount is not a number
            self.manager.add_expense(name, amount_text, category) # Calls the add_expense method of the manager to add new expense
        except ValueError: # Catches a ValueError if the amount is not a valid number
            messagebox.showerror("Error", "Amount must be a number.")
            return

        self.clear_form() # Clears the entry fields after adding an expense
        self.refresh_view() # Refreshes the display to show the updated list of expenses

    def get_form_data(self): # Gets the text from the entry fields and returns them as tuples
        name = self.name_entry.get().strip()
        amount_text = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        return name, amount_text, category

    def validate_entry(self, name, amount_text): # Validates that the boxes are not empty and returns an error if there is a problem
        if not name or not amount_text:
            return "Please enter both a name and an amount."
        return ""

    def clear_form(self): # Clears the entry fields and sets focus to the name entry
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.name_entry.focus_set()

    def refresh_view(self): # Updates the text display with the list of expenses and updates the total label
        self.text_display.delete("1.0", tk.END) # Clears the text display area

        expense_report = self.manager.get_all_expenses() # Gets the formatted list of expenses from the manager
        if expense_report: # Inserts expense report
            self.text_display.insert(tk.END, expense_report) 
        else: # If there are no expenses, show a message
            self.text_display.insert(tk.END, "No expenses added yet.")

        self.total_label.config(text=f"Total: ${self.manager.get_total():.2f}") # Updates the total with the new total from the manager


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
