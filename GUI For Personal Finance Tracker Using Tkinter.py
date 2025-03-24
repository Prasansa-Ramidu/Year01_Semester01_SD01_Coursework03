# Import the tkinter library
import tkinter as tk
# Import the ttk module for tkinter
from tkinter import ttk
# Import the JSON module
import json
# Import datetime class from datetime module
from datetime import datetime

class FinanceTrackerGUI:
    def __init__(self, root):
        # Initialize the FinanceTrackerGUI class with the root window
        self.root = root
        # Name the main appliction root window as "Personal Finance Tracker"
        self.root.title("Personal Finance Tracker")
        # Create the widgets for the FinanceTrackerGUI
        self.create_widgets()
        # Load the transactions from the json file("transactions.json") and assign it to transactions variable
        self.transactions = self.load_transactions("transactions.json")

    # This function used to create widgets for the FinanceTrackerGUI
    def create_widgets(self):
        # Frame for table and scrollbar
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying transactions
        self.tree = ttk.Treeview(self.frame, columns=("amount", "date"))
        self.tree.heading("#0", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("date", text="Date")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Search bar and button
        search_var = tk.StringVar()
        search_entry = ttk.Entry(self.root, textvariable=search_var)
        search_entry.pack(padx=5, pady=5, fill=tk.X)
        search_button = ttk.Button(self.root, text="Search", command=lambda: self.search_transactions(search_var.get()))
        search_button.pack(padx=10, pady=5)

        # Sort buttons
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(padx=10, pady=5)
        ttk.Button(sort_frame, text="Sort by Amount", command=lambda: self.sort_by_column("amount", False)).grid(row=0, column=0, padx=5)
        ttk.Button(sort_frame, text="Sort by Date", command=lambda: self.sort_by_column("date", False)).grid(row=0, column=1, padx=5)

        # Add transaction
        add_frame = ttk.Frame(self.root)
        add_frame.pack(padx=10, pady=5)
        ttk.Label(add_frame, text="Amount:").grid(row=0, column=0, padx=5)
        self.amount_entry = ttk.Entry(add_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(add_frame, text="Date(YYYY-MM-DD):").grid(row=1, column=0, padx=5)
        self.date_entry = ttk.Entry(add_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(add_frame, text="Add Transaction", command=self.add_transaction).grid(row=3, column=0, padx=5, pady=10)

        # Update transaction and Reset button/Transaction id label and Entry field
        ttk.Button(add_frame, text="Update Transaction", command=self.update_transaction).grid(row=3, column=1, padx=5, pady=10)
        ttk.Button(add_frame, text="Resetting Button", command=self.reset).grid(row=3, column=2, padx=5, pady=10)
        ttk.Label(add_frame, text="Transaction Id:").grid(row=2, column=0, padx=5)
        self.transaction_id_entry = ttk.Entry(add_frame)
        self.transaction_id_entry.grid(row=2, column=1, padx=5, pady=5)

        # Display summary and Delete transaction
        ttk.Button(add_frame, text="Display summary", command=self.display_summary).grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(add_frame, text="Delete Transaction", command=self.delete_transaction).grid(row=4, column=2, padx=5, pady=10)

    # This function used to load the transactions from the JSON file
    def load_transactions(self, filename):
        # load the transactions in the JSON file
        try:
            with open(filename, "r") as file:
                transactions = json.load(file)
                return transactions
        except FileNotFoundError:
            print("File not found.")
            return {}
        except json.JSONDecodeError:
            print("File data is not in a correct json format")
            return {}
        except Exception as e:
            print("An error occured:", e)
            return {}
        
    # This function used to save transactions to a JSON file
    def save_transactions(self):
        # Write updated transactions to the JSON file
        try:
            with open("transactions.json", "w") as file:
                json.dump(self.transactions, file)
        except Exception as e:
            print("Error occurred while saving transactions:", e)
        
    # This function used to display the transactions in the FinanceTrackerGUI 
    def display_transactions(self, transactions):
        # Remove existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add transactions to the treeview
        for category, category_transactions in transactions.items():
            for transaction in category_transactions:
                self.tree.insert("", "end", text=category, values=(transaction["amount"], transaction["date"]))
        print("Transactions Displayed Sucessfully")

    # This function used to search transactions in the FinanceTrackerGUI
    def search_transactions(self, query):
        # Remove existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Search through transactions
        for category, category_transactions in self.transactions.items():
            for transaction in category_transactions:
                if query.lower() in str(transaction["amount"]).lower() or query.lower() in str(transaction["date"]).lower():
                    self.tree.insert("", "end", text=category, values=(transaction["amount"], transaction["date"]))
        print("Search Transactions Went Sucessfully")

    # This function used to values sorting process
    def sort_by_column(self, col, reverse):
        # Sort transactions by selected column
        sorted_transactions = {}

        for category, transactions in self.transactions.items():
            sorted_transactions[category] = sorted(transactions, key=lambda x: x[col], reverse=reverse)

        # Display sorted transactions
        self.display_transactions(sorted_transactions)
        print("Sorted Transaction Data According To The Date Or Amount Went Sucessfully")

    # This function used to add new transaction to the FinanceTrackerGUI
    def add_transaction(self):
        # Read the amount_entry and date_entry fields
        amount_str = self.amount_entry.get()
        date_str = self.date_entry.get()

        if amount_str and date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
                amount = float(amount_str)
                if amount < 0:   
                    category = "Groceries"
                elif amount == 0:
                    return None
                else:
                    category = "Salary"
                new_transaction = {"amount": amount, "date": date}

                # Append new transaction to existing transactions
                if category in self.transactions:
                    self.transactions[category].append(new_transaction)
                else:
                    self.transactions[category] = [new_transaction]
                    
                self.save_transactions()
                print("Transactions Added Sucessfully")
                
                # Refresh the displayed transactions
                self.display_transactions(self.transactions)
                self.reset()

            except ValueError:
                print("Invalid amount or date format.")
            except Exception as e:
                print("An error occured:", e)
        else:
            print("Please enter both amount_str and date_str.")

    # This function used to update the transaction data that has been in the FinanceTrackerGUI        
    def update_transaction(self):
        # Read the amount_entry, date_entry and transaction_id_entry fields 
        amount_str = self.amount_entry.get()
        date_str = self.date_entry.get()
        transaction_id_str = self.transaction_id_entry.get()      

        if amount_str and date_str and transaction_id_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
                amount = float(amount_str)
                if amount < 0:   
                    category = "Groceries"
                elif amount == 0:
                    return None
                else:
                    category = "Salary"
                transa_id = int(transaction_id_str)
                if category in self.transactions:
                    print(f"transaction for {category}: ")

                transaction_found = False
                for x, transaction in enumerate(self.transactions[category]):
                    if x == transa_id:
                        print(transa_id, "amount:", transaction["amount"], "date:", transaction["date"])
                        self.transactions[category][transa_id] = {"amount": amount, "date": date}

                        self.save_transactions()
                        print("Transactions Updated Sucessfully")
                        transaction_found = True
                        break
                    
                if not transaction_found:
                    print("transaction id not found")                    
                        
                # Refresh the displayed transactions
                self.display_transactions(self.transactions)
                self.reset()
                
            except ValueError:
                print("Invalid amount or date or transa_id format.")
            except IndexError:
                print("Invalid index id for transa_id. Please try again!")
            except Exception as e:
                print("An error occured:", e)
        else:
            print("Please enter amount_str, date_str and transaction_id_str.")
            
    # This function used to display summary of transactions
    def display_summary(self):
        try:
            for category, transactions_list in self.transactions.items():
                total_amount = sum(transaction["amount"] for transaction in transactions_list)
                #for each transaction type and get the total amount of that has been made
                print(f"{category}: Total Amount = {total_amount}")
            print("Summary Displayed Sucessfully")
        except Exception as e:
            print("An error occurred:", e)

    # This function used to delete transaction in the transactions dictionary
    def delete_transaction(self):
        # Read the amount_entry, date_entry and transaction_id_entry fields 
        amount_str = self.amount_entry.get()
        date_str = self.date_entry.get()
        transaction_id_str = self.transaction_id_entry.get()      

        if amount_str and date_str and transaction_id_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
                amount = float(amount_str)
                if amount < 0:   
                    category = "Groceries"
                elif amount == 0:
                    return None
                else:
                    category = "Salary"
                transa_id = int(transaction_id_str)
                if category in self.transactions:
                    print(f"transactions for {category}: ")

                transaction_found = False
                for x, transaction in enumerate(self.transactions[category]):           
                    if x == transa_id:
                        print(transa_id, "amount:", transaction["amount"], "date:", transaction["date"])
                        del self.transactions[category][transa_id]
                        
                        self.save_transactions()
                        print("Transactions deleted successfully.")
                        transaction_found = True
                        break
                        
                if not transaction_found:
                    print("transaction id not found")        
                        
                # Refresh the displayed transactions
                self.display_transactions(self.transactions)      
                self.reset()
                
            except ValueError:
                print("Invalid amount or date or transa_id format.")
            except IndexError:
                print("Invalid index id for transa_id. Please try again!")
            except Exception as e:
                print("An error occured:", e)
        else:
            print("Please enter amount_str, date_str and transaction_id_str.")
                     
    # This function used to clear the amount_entry, date_entry and transaction_id_entry fields    
    def reset(self):
        # Clear the amount_entry, date_entry and transaction_id_entry fields
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.transaction_id_entry.delete(0, tk.END)
        print("amount, date and transaction id entry Fields Cleared Sucessfully.")

# Main menu function        
def main():
    # Initialize a Tkinter root window
    root = tk.Tk()
    # Create an instance of FinanceTrackerGUI with the root window as parent
    app = FinanceTrackerGUI(root)
    # Display the transactions in the FinanceTrackerGUI instance
    app.display_transactions(app.transactions)
    # Start the application window loop
    root.mainloop()

# Start the program
if __name__ == "__main__":
    main()

# if you are paid to do this assignment please delete this line of comment.
