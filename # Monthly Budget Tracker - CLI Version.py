# Monthly Budget Tracker - CLI Version
# This serves as the 'Logic' layer for your GUI project.

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

def main():
    manager = BudgetManager()
    
    # Simple loop for the CLI version
    while True:
        print("\n--- Budget Tracker ---")
        print("1. Add Expense")
        print("2. View All")
        print("3. View Total")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            name = input("Enter expense name: ")
            amount = input("Enter amount: ")
            cat = input("Enter category: ")
            manager.add_expense(name, amount, cat)
        elif choice == '2':
            print("\nExpenses:\n" + manager.get_all_expenses())
        elif choice == '3':
            print(f"\nTotal Spending: ${manager.get_total():.2f}")
        elif choice == '4':
            break

if __name__ == "__main__":
    main()