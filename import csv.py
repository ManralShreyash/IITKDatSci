import csv
from datetime import datetime

# Initialize the dictionary for storing expenses
fin_dict = {}  # Dictionary to store expenses, keyed by name

# Function to save expenses to CSV
def save_expenses_to_csv(fin_dict, filename='expenses.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write each person's expenses to the CSV file
        for Log_no, expense in fin_dict.items():
            writer.writerow([Log_no, expense['date'], expense['category'], expense['amount'], expense['description']])

# Function to load expenses from CSV
def load_expenses_from_csv(filename='expenses.csv'):
    expenses = {}
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row

            # Read each row and add it to fin_dict
            for row in reader:
                Log_no = row[0]
                expense = {
                    'date': row[1],
                    'category': row[2],
                    'amount': float(row[3]),  # Convert amount to float for calculations
                    'description': row[4]
                }
                expenses[Log_no] = expense

    except FileNotFoundError:
        print(f"File '{filename}' not found. Starting with an empty list.")
    
    return expenses

# Function to fill the fin_dict with expense data
def filldict(Log_no, expense_data):
    fin_dict[Log_no] = expense_data

# Function to add a new expense and save to CSV
def main_func():
    Ans = "Y"  # Initialize the answer

    # Load existing data from CSV at the start
    global fin_dict
    fin_dict = load_expenses_from_csv()

    while Ans != 'N':
        Ans = input("Do you wish to continue putting details? (Y/N): ")
    
        if Ans == 'Y':
            Log_no = input("Entry No: ")
            Date = input("Date of bill (YYYY-MM-DD): ")
            cat = input("Category of expense (food/travel): ")
            amn = input("Amount paid: ")
            desc = input("Give short description (in one line): ")

            # Create a fresh dictionary instance for Emp_exp for each expense entry
            Emp_exp = {'date': Date, 'category': cat, 'amount': float(amn), 'description': desc}

            # Add the new expense to the fin_dict, keyed by name
            filldict(Log_no, Emp_exp)

    # Save the updated fin_dict to the CSV file
    save_expenses_to_csv(fin_dict)

# Function to view all expenses
def view_exp():
    print("\n--- All Expenses ---")
	
    for Log_no, expense in fin_dict.items():
        print(f"{Log_no}: Date: {expense['date']}, Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")
    
    check_missing_data()

# Function to check for missing details
def missing_detail(P):
    for key in P:
        if P[key] == '' or P[key] is None:  # Check if the value is missing (empty or None)
            resp = input(f"Is '{key}' the key for which data is missing? (Y/N): ")
            if resp == 'Y':
                if key == 'amount':
                    new_value = float(input(f"Please enter the value for '{key}"))
                    P[key] = new_value
                    continue
                new_value = input(f"Please enter the value for '{key}': ")
                P[key] = new_value
                print(f"Updated '{key}' with value: {new_value}")
                break  # After updating, exit the loop and return

def change_detail(P):
    for key in P:  
        resp = input(f"Is '{key}' the key for which you want to change the data for? (Y/N): ")
        if resp == 'Y':
            if key == 'amount':
                new_value = float(input(f"Please enter the value for '{key}"))
                P[key] = new_value
                continue

            new_value = input(f"Please enter the value for '{key}': ")
            P[key] = new_value
            print(f"Updated '{key}' with value: {new_value}")
            break  # After updating, exit the loop and return

# Function to handle missing values in the dictionary
def check_missing_data():
    Ans = input("Is any value in the data missing? (Y/N): ")
    while Ans != "N":
        for Log_no, data in fin_dict.items():
            print(f"Checking details for entry number {Log_no}")
            missing_detail(data)
        Ans = input("Is any value in the data missing? (Y/N): ")

    Ans1 = input("Is there any value that you wish to change? (Y/N): ")
    while Ans1 != "N":
        for Log_no, data in fin_dict.items():
            afp = input(f"Do you wish to change data for {Log_no}? (Y/N): ")
            if afp == "Y":
                change_detail(data)
        Ans1 = input("Is there any data value yet to change?(Y/N): ")

    print("Final data:", fin_dict)

# Function to set a monthly budget
def monthlybudget():
    budget = float(input("Enter a monthly budget you want to set for yourself: "))  # Convert to float
    return budget

# Function to track the budget
def tallybudget(budget, fin_dict):
    tot_exp = 0  # Initialize total expense variable

    # Calculate total expenses
    for key in fin_dict:
        sum_exp = fin_dict[key]['amount']
        tot_exp += sum_exp

    print(f"Your total expense is coming out to be: {tot_exp}")  # Use f-string for formatting
    
    # Compare expenses with the budget
    if tot_exp > budget:
        print(f"You have exceeded your monthly budget by {tot_exp - budget}")  # Use f-string for formatting
    elif tot_exp < budget:
        print(f"You still have {budget - tot_exp} left from your monthly budget")  # Use f-string for formatting
    else:
        print("You have spent the exact amount as you wanted your monthly expense to be")

# Main function for user interaction options
def options_det():
    while True:
        opt_num = int(input("Enter 1 to add expense, 2 to view expense, 3 to track budget, 4 to save expenses and 5 to exit: "))

        if opt_num == 1:
            main_func()
        elif opt_num == 2:
            view_exp()
        elif opt_num == 3:
            budget = monthlybudget()
            tallybudget(budget, fin_dict)
        elif opt_num == 4:
            save_expenses_to_csv(fin_dict)
        elif opt_num == 5:
            print("You have exited!")
            break  # Exit the loop

# Run the program
if __name__ == "__main__":
    options_det()
