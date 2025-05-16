import os
import datetime

#==========================ENHANCEMENTS===========================================

def show_current_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"Current Date : {current_date}")


def get_username(u_id):
    if os.path.exists("Users.txt"):
        with open("Users.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[0] == u_id:
                    return( parts[1] ) # Return the name
    return None  

def count_customers_from_file(filename="customers.txt"):
    with open(filename, "r") as file:
        return sum(1 for line in file if line.strip())
    
def count_transactions(account_id):
    """Count all transactions for a specific account"""
    if not os.path.exists("Transactions.txt"):
        return 0
    
    count = 0
    with open("Transactions.txt", "r") as file:
        for line in file:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4 and parts[0] == account_id:
                count += 1
    return count


#=================================================================================


def generate_id(prefix, filename):
    """
    Generate a new ID by finding the highest existing ID + 1
    Args:
        prefix: 'U' for User, 'C' for Customer, 'AC' for Account
        filename: File to check for existing IDs
    """
    max_id = 0
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if parts:  # Check if line has data
                    existing_id = parts[0]
                    try:
                        # Extract numeric part (e.g., "U00001" → 1, "AC00002" → 2)
                        num = int(''.join(filter(str.isdigit, existing_id)))
                        if num > max_id:
                            max_id = num
                    except ValueError:
                        continue
    return f"{prefix}{max_id + 1:05d}"  # Format with leading zeros

# Initialize files if they don't exist
def initialize_files():
    if not os.path.exists("Users.txt"):
        open("Users.txt", 'w').close()
    if not os.path.exists("Customers.txt"):
        open("Customers.txt", 'w').close()
    if not os.path.exists("Accounts.txt"):
        open("Accounts.txt", 'w').close()
    if not os.path.exists("Transactions.txt"):
        open("Transactions.txt", 'w').close()

# Admin functions
def create_admin():
    if not admin_exists():
        with open("Users.txt", "a") as file:
            file.write("U00000    | Admin  | Admin@123   | admin\n")
        print("Admin account created successfully!")
        print("Admin User ID: U00000")
        print("Secret pin must be given to admin manually.\n")


def admin_exists():
    if not os.path.exists("Users.txt"):
        return False
    with open("Users.txt", "r") as file:
        for line in file:
            if "admin" in line.strip().lower():
                return True
    return False


def generate_user_id():
    max_id = 0  # Track the highest ID number found
    if os.path.exists("Users.txt"):
        with open("Users.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    user_id = parts[0]  # Extract ID (e.g., "U00001")
                    try:
                        # Convert "U00001" → 1, "U00003" → 3, etc.
                        num = int(user_id[1:])  
                        if num > max_id:
                            max_id = num
                    except ValueError:
                        continue  # Skip malformed IDs
    return f"U{max_id + 1:05d}"  # New ID = highest ID + 1 (e.g., U00004)


def create_customer(user_id, name, password, role="user"):
    name = name.title()     ## TITLE CASE
    with open("Users.txt", "a") as file:
        file.write(f"{user_id:<10}| {name:<7}| {password:<12}| {role}\n")
    print("Customer created successfully!")

# Login verification
def verify_login(user_id, password):
    if not os.path.exists("Users.txt"):
        return None
    with open("Users.txt", "r") as file:
        for line in file:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4 and parts[0] == user_id and parts[2] == password:
                return parts[3]
    return None

# Customer functions
def generate_customer_id():
    digit = 1
    if os.path.exists("Customers.txt"):
        with open("Customers.txt", "r") as file:
            digit = len(file.readlines())
    return "C" + str(digit).zfill(5)


def create_customer_file(customer_id, name, user_id):
    name = name.title()
    with open("Customers.txt", "a") as file:
        file.write(f"{customer_id:<10}| {name:<12}| {user_id:<12}\n")


def show_all_customers():
    if os.path.exists("Users.txt"):
        print(f"\n{'User ID':<10}| {'Name':<12}| {'Password':<12}| {'Role'}")
        print("-" * 50)
        with open("Users.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) == 4:
                    print(f"{parts[0]:<10}| {parts[1]:<9}| {parts[2]:<13}| {parts[3]}")
    else:
        print("No customer data found.")

# Account functions
def generate_account_id():
    digit = 1
    if os.path.exists("Accounts.txt"):
        with open("Accounts.txt", "r") as file:
            digit = len(file.readlines())
    return "AC" + str(digit).zfill(5)


def create_account_file(account_id, user_id, customer_id, balance):
    with open("Accounts.txt", "a") as file:
        file.write(f"{account_id:<10}| {user_id:<10}| {customer_id:<10}| {balance:<10.2f}\n")


def get_account_balance(account_id):
    if not os.path.exists("Accounts.txt"):
        return None
    with open("Accounts.txt", "r") as file:
        for line in file:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4 and parts[0] == account_id:
                return float(parts[3])
    return None


def update_account_balance(account_id, new_balance):
    lines = []
    found = False
    
    if os.path.exists("Accounts.txt"):
        with open("Accounts.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[0] == account_id:
                    line = f"{account_id:<10}| {parts[1]:<10}| {parts[2]:<10}| {new_balance:<10.2f}\n"
                    found = True
                lines.append(line)
    
    if found:
        with open("Accounts.txt", "w") as file:
            file.writelines(lines)
        return True
    return False

# Transaction functions
def record_transaction(account_id, transaction_type, amount, balance):
    with open("Transactions.txt", "a") as file:
        file.write(f"{account_id:<10}| {transaction_type:<15}| {amount:<10.2f}| {balance:<10.2f}\n")


def get_user_accounts(user_id):
    accounts = []
    if os.path.exists("Accounts.txt"):
        with open("Accounts.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[1] == user_id:
                    accounts.append({
                        'account_id': parts[0],
                        'balance': float(parts[3])
                    })
    return accounts


def get_transaction_history(account_id):
    transactions = []
    if os.path.exists("Transactions.txt"):
        with open("Transactions.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[0] == account_id:
                    transactions.append({
                        'type': parts[1],
                        'amount': float(parts[2]),
                        'balance': float(parts[3])
                    })
    return transactions

# User details
def view_user_details(user_id):
    name = ""
    role = ""
    print("\n--- Profile Details ---")
    
    # Fetch user details from Users.txt
    if os.path.exists("Users.txt"):
        with open("Users.txt", "r") as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) == 4 and parts[0] == user_id:
                    name = parts[1]
                    role = parts[3]
                    print(f"User ID   : {parts[0]}")
                    print(f"Name      : {parts[1]}")
                    print(f"Password  : {parts[2]}")
                    print(f"Role      : {parts[3]}")
                    break
    
    # Fetch customer details from Customers.txt
    if os.path.exists("Customers.txt"):
        with open("Customers.txt", "r") as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) == 3 and parts[2] == user_id:
                    print(f"Customer ID: {parts[0]}")
                    break
                else:
                    print("Incorrect userID")
                    break
    
    # Show account information
    accounts = get_user_accounts(user_id)
    if accounts:
        print("\nYour Accounts:")
        for account in accounts:
            print(f"Account ID: {account['account_id']} | Balance: {account['balance']:.2f}")


def delete_customer(user_id=None):
    """Delete a customer and all associated data"""
    if user_id is None:
        print("\n--- Delete Customer ---")
        user_id = input("Enter user ID to delete: ").strip()
    
    # Prevent admin from deleting themselves
    if user_id == "U00000":
        print("Error: Cannot delete the primary admin account!")
        return
    
    # First check if user exists
    user_exists = False
    user_name = ""
    if os.path.exists("Users.txt"):
        with open("Users.txt", "r") as file:
            for line in file:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[0] == user_id:
                    user_exists = True
                    user_name = parts[1]
                    break
    
    if not user_exists:
        print("Error: User not found!")
        return
    
    # Show confirmation prompt
    print(f"\nWARNING: You are about to delete user {user_id} ({user_name})")
    print("This will permanently delete:")
    print("- User credentials")
    print("- All associated accounts")
    print("- All transaction history")
    
    confirm = input("Are you sure? (Type 'Y' to confirm): ").strip().upper()
    if confirm != 'Y':
        print("Deletion cancelled.")
        return
    
    # Initialize flags
    user_found = False
    customer_found = False
    account_found = False
    account_ids = []
    
    # 1. Delete from Users.txt
    if os.path.exists("Users.txt"):
        with open("Users.txt", "r") as file:
            lines = file.readlines()
        
        with open("Users.txt", "w") as file:
            for line in lines:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[0] == user_id:
                    user_found = True
                else:
                    file.write(line)
    
    # 2. Delete from Customers.txt
    if os.path.exists("Customers.txt"):
        with open("Customers.txt", "r") as file:
            lines = file.readlines()
        
        with open("Customers.txt", "w") as file:
            for line in lines:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 3 and parts[2] == user_id:
                    customer_found = True
                else:
                    file.write(line)
    
    # 3. Delete from Accounts.txt and get account IDs
    if os.path.exists("Accounts.txt"):
        with open("Accounts.txt", "r") as file:
            lines = file.readlines()
        
        with open("Accounts.txt", "w") as file:
            for line in lines:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[1] == user_id:
                    account_ids.append(parts[0])
                    account_found = True
                else:
                    file.write(line)
    
    # 4. Delete related transactions
    if os.path.exists("Transactions.txt") and account_ids:
        with open("Transactions.txt", "r") as file:
            lines = file.readlines()
        
        with open("Transactions.txt", "w") as file:
            for line in lines:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 4 and parts[0] not in account_ids:
                    file.write(line)
    
    # Result message
    print(f"\nSuccessfully deleted user {user_id}!")
    if customer_found:
        print("- Removed from customer records")
    if account_found:
        print(f"- Deleted {len(account_ids)} account(s)")
    print("- Removed all related transactions");


def view_all_balances():
    if not os.path.exists("Accounts.txt") or not os.path.exists("Users.txt"):
        print("Accounts file not found")
        return
    
    user_names = {}
    with open("Users.txt", "r") as Users_file:
        for line in Users_file:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 2:
                user_id = parts[0]
                user_name = parts[1]
                user_names[user_id] = user_name

    print("\n-------------- All User Balances --------------")
    print(f"\n{'Account Number':<12} | {'Name':<20} | {'Balance':<10}")
    print("-" * 50)
    
    with open("Accounts.txt", "r") as file:
        for line in file:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4:
                account_id = parts[0]
                user_id = parts[1]
                balance = parts[3]
                name = user_names.get(user_id, "Unknown")
                print(f"{account_id:<12} | {name:<20} | {balance:<10}")

# Banking operations
def deposit_money(account_id):
    amount = float(input("Enter amount to deposit: "))
    if amount <= 0:
        print("Amount must be positive.")
        return
    
    balance = get_account_balance(account_id)
    if balance is None:
        print("Account not found.")
        return
    
    new_balance = balance + amount
    if update_account_balance(account_id, new_balance):
        record_transaction(account_id, "DEPOSIT", amount, new_balance)
        print(f"Deposit successful. New balance: {new_balance:.2f}")
    else:
        print("Failed to update account balance.")


def withdraw_money(account_id):
    amount = float(input("Enter amount to withdraw: "))
    if amount <= 0:
        print("Amount must be positive.")
        return
    
    balance = get_account_balance(account_id)
    if balance is None:
        print("Account not found.")
        return
    
    if amount > balance:
        print("Insufficient funds.")
        return
    
    new_balance = balance - amount
    if update_account_balance(account_id, new_balance):
        record_transaction(account_id, "WITHDRAWAL", -amount, new_balance)
        print(f"Withdrawal successful. New balance: {new_balance:.2f}")
    else:
        print("Failed to update account balance.")


def transfer_money(from_account_id, user_id):
    to_account_id = input("Enter recipient account ID: ")
    amount = float(input("Enter amount to transfer: "))
    
    if amount <= 0:
        print("Amount must be positive.")
        return
    
    # Check if recipient account exists
    to_balance = get_account_balance(to_account_id)
    if to_balance is None:
        print("Recipient account not found.")
        return
    
    # Check sender's balance
    from_balance = get_account_balance(from_account_id)
    if from_balance is None:
        print("Your account not found.")
        return
    
    if amount > from_balance:
        print("Insufficient funds.")
        return
    
    # Perform transfer
    new_from_balance = from_balance - amount
    new_to_balance = to_balance + amount
    
    if update_account_balance(from_account_id, new_from_balance) and update_account_balance(to_account_id, new_to_balance):
        record_transaction(from_account_id, "TRANSFER OUT", -amount, new_from_balance)
        record_transaction(to_account_id, "TRANSFER IN", amount, new_to_balance)
        print(f"Transfer successful. Your new balance: {new_from_balance:.2f}")
    else:
        print("Transfer failed.")


def view_transaction_history(account_id):
    transactions = get_transaction_history(account_id)
    if not transactions:
        print("No transactions found for this account.")
        return
    
    print(f"\nTransaction History for Account {account_id}")
    print("-" * 60)
    print(f"{'Type':<15} | {'Amount':>10} | {'Balance':>10}")
    print("-" * 60)
    
    for trans in transactions:
        print(f"{trans['type']:<15} | {trans['amount']:>10.2f} | {trans['balance']:>10.2f}")


def change_password(user_id):
      # Verify current password
    current_pw = input("Enter current password: ")
    if not verify_current_password(user_id, current_pw):
        print("Incorrect current password!")
        return
    
    # Get new password
    new_pw = input("Enter new password: ")
    confirm_pw = input("Confirm new password: ")
    
    if new_pw != confirm_pw:
        print("Error: Passwords don't match!")
        return
    
    if len(new_pw) < 4:  # Minimum 4 characters
        print("Error: Password too short (min 4 characters)!")
        return
    
    # Update password
    if update_password_in_file(user_id, new_pw):
        print("Password updated successfully!")
    else:
        print("Failed to update password. Please try again.")


def verify_current_password(user_id, current_pw):
    """Check if entered password matches stored password"""
    if not os.path.exists("Users.txt"):
        return False
        
    with open("Users.txt", "r") as file:
        for line in file:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4 and parts[0] == user_id:
                return parts[2] == current_pw  # Direct comparison
    return False


def update_password_in_file(user_id, new_pw):
    """Update password in Users.txt"""
    lines = []
    updated = False
    
    with open("Users.txt", "r") as file:
        for line in file:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4 and parts[0] == user_id:
                # Update the password (store as plaintext)
                line = f"{parts[0]:<10}| {parts[1]:<7}| {new_pw:<12}| {parts[3]}\n"
                updated = True
            lines.append(line)
    
    if updated:
        with open("Users.txt", "w") as file:
            file.writelines(lines)
        return True
    return False

# Admin dashboard
def admin_dashboard():
    while True:
        print("\nAdmin Dashboard:")
        print("1. Create new customer")
        print("2. View all users")
        print("3. View all customer balances")
        print("4. Search customer")
        print("5. Delete customer")
        print("6. Withdraw money")
        print("7. Deposit money")
        print("8. Money transfer")
        print("9. View all transactions")
        print("10. Exit admin dashboard")
        print("11. Total Customer count")
        print("12. View Transaction Count")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Enter customer name: ")
                password = input("Set temporary password: ")
                balance = float(input("Enter initial balance: "))
                account_id = generate_id('AC', "Accounts.txt")
                user_id = generate_id('U', "Users.txt")
                customer_id = generate_id('C', "Customers.txt")
                create_customer(user_id, name, password, role="user")
                create_customer_file(customer_id, name, user_id)
                create_account_file(account_id, user_id, customer_id, balance)
                record_transaction(account_id, "INITIAL DEPOSIT", balance, balance)
            elif choice == 2:
                show_all_customers()
            elif choice == 3:
                view_all_balances()
            elif choice == 4:
                user_id = input("Enter user ID to search: ")
                view_user_details(user_id)
            elif choice == 5:
                user_id = input("Enter user ID to delete: ")
                delete_customer(user_id)
            elif choice in [6, 7]:  # Withdraw, Deposit, or Transfer
                # First get the account ID
                account_id = input("Enter account ID: ")
                account_balance = get_account_balance(account_id)
                if account_balance is None:
                    print("Account not found!")
                    continue
                
                if choice == 6:
                    withdraw_money(account_id)
                elif choice == 7:
                    deposit_money(account_id)
            
            elif choice == 8:  # Money transfer
                    # Get sender account details
                    sender_account_id = input("Enter sender's account ID: ")
                    sender_balance = get_account_balance(sender_account_id)
                    if sender_balance is None:
                        print("Sender account not found!")
                        continue

                    # Get recipient account details
                    recipient_account_id = input("Enter recipient's account ID: ")
                    recipient_balance = get_account_balance(recipient_account_id)
                    if recipient_balance is None:
                        print("Recipient account not found!")
                        continue

                    if sender_account_id == recipient_account_id:
                        print("Cannot transfer to the same account!")
                        continue

                    # Get transfer amount
                    try:
                        amount = float(input("Enter amount to transfer: "))
                        if amount <= 0:
                            print("Amount must be positive.")
                            continue
                        if amount > sender_balance:
                            print("Insufficient funds in sender's account.")
                            continue
                    except ValueError:
                        print("Invalid amount entered.")
                        continue

                    # Perform transfer
                    new_sender_balance = sender_balance - amount
                    new_recipient_balance = recipient_balance + amount

                    if (update_account_balance(sender_account_id, new_sender_balance) and 
                        update_account_balance(recipient_account_id, new_recipient_balance)):
                        record_transaction(sender_account_id, 
                                        f"TRANSFER TO {recipient_account_id}", 
                                        -amount, new_sender_balance)
                        record_transaction(recipient_account_id, 
                                        f"TRANSFER FROM {sender_account_id}", 
                                        amount, new_recipient_balance)
                        print("\nTransfer successful!")
                        print(f"Sender's new balance: {new_sender_balance:.2f}")
                    else:
                        print("Transfer failed. Please try again.")



            elif choice == 9:
                account_id = input("Enter account ID to view transactions: ")
                view_transaction_history(account_id)
            elif choice == 10:
                break
            elif choice == 11:
                num = count_customers_from_file()
                print(f"Total Customer : {num}")
            elif choice == 12:  # Transaction Count
                account_id = input("Enter account ID: ")
                count = count_transactions(account_id)
                print(f"\nAccount {account_id} has {count} transactions")
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number.")

# User panel
def user_panel(user_id):
    accounts = get_user_accounts(user_id)
    if not accounts:
        print("No accounts found for this user.")
        return
    
    # If user has only one account, use it automatically
    account_id = accounts[0]['account_id'] if len(accounts) == 1 else None
    
    while True:
        print("\nUser Panel:")
        print("1. View your details")
        print("2. View your balance")
        print("3. Withdraw money")
        print("4. Deposit money")
        print("5. Money transfer")
        print("6. View transaction history")
        print("7. Change Password")
        print("8. Exit")
        print("9. Show current date")

        try:
            choice = int(input("Enter your choice: "))
            
            if account_id is None and choice in [2,3,4,5,6]:
                print("You have multiple accounts. Please select an account:")
                for i, acc in enumerate(accounts, 1):
                    print(f"{i}. Account {acc['account_id']} (Balance: {acc['balance']:.2f})")
                acc_choice = int(input("Select account (1-{}): ".format(len(accounts))))
                if 1 <= acc_choice <= len(accounts):
                    account_id = accounts[acc_choice-1]['account_id']
                else:
                    print("Invalid selection.")
                    continue
            
            if choice == 1:
                view_user_details(user_id)
            elif choice == 2:
                balance = get_account_balance(account_id)
                print(f"\nAccount {account_id} balance: {balance:.2f}")
            elif choice == 3:
                withdraw_money(account_id)
            elif choice == 4:
                deposit_money(account_id)
            elif choice == 5:
                transfer_money(account_id, user_id)
            elif choice == 6:
                view_transaction_history(account_id)
            elif choice == 7:  
                change_password(user_id)
            elif choice == 8:
                break
            elif choice == 9:
                show_current_date()
            else : 
                print("Invalid choice!")
        except ValueError:
            print("Enter numbers only!")




initialize_files()
create_admin()


while True:
        print("\n" + "-" * 50)
        print("      Welcome to the Mini Bank System")
        print("-" * 50)
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                u_id = input("Enter admin user ID: ")
                pin = input("Enter admin password: ")
                role = verify_login(u_id, pin)
                if role == "admin":
                    print(f"\nWelcome Admin {u_id}!")
                    admin_dashboard()
                else:
                    print("Incorrect admin credentials.")
            elif choice == 2:
                u_id = input("Enter your user ID: ")
                pw = input("Enter your password: ")
                role = verify_login(u_id, pw)
                if role == "user":
                    name = get_username(u_id)
                    print(f"\nWelcome {name}!")
                    user_panel(u_id)
                elif role == "admin":
                    print("This is an admin account. Use Admin Login.")
                else:
                    print("Invalid user id or password.")
            elif choice == 3:
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Try 1–3.")
        except ValueError:
            print("Enter numbers only!")