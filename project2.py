import json
import os

# File where user data will be stored
DATA_FILE = "user_data.json"

def load_data():
    
    #Load user data from the JSON file.
    #Returns an empty dictionary if the file doesn't exist.

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    
    #Save the given data dictionary to the JSON file.
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def user_register(user_data):
    
    #Register a new user if the username doesn't already exist.
    
    ans = input("Do you wish to register for the task manager? (Y/N): ")
    if ans.upper() == 'Y':
        username = input("Enter username: ")
        if username in user_data:
            print("Username already exists. Please choose a different username.")
            return
        password = input("Enter password: ")
        user_data[username] = {"password": password, "tasks": []}
        save_data(user_data)
        print("Registration successful!")

def user_login(user_data):
    
    #Authenticate user login based on stored credentials.
    
    user_id = input("Enter your username: ")
    user_pass = input("Enter your password: ")
    if user_id in user_data and user_data[user_id]["password"] == user_pass:
        print("Login successful!")
        return user_id
    else:
        print("Invalid username or password.")
        return None

def open_task(tasks):
    
    #Display running tasks and allow user to add or remove tasks.
    
    print("\n****** You are running the following tasks ******\n")
    if not tasks:
        print("There are no tasks running.\n")
    else:
        for idx, task in enumerate(tasks, 1):
            print(f"Task {idx}: {task}\n")

    ans = input("Do you wish to enter another task? (Y/N): ")
    if ans.upper() == 'Y':
        enter_task(tasks)
    ans = input("Do you wish to remove a task? (Y/N): ")
    if ans.upper() == 'Y':
        remove_task(tasks)

def enter_task(tasks):
    
    #Add a new task to the task list.
    
    new_entry = input("Enter task: ")
    tasks.append(new_entry)
    print("\nUpdated Task List:")
    for idx, task in enumerate(tasks, 1):
        print(f"Task {idx}: {task}\n")

def remove_task(tasks):
    
    #Remove a task from the task list based on user input.
    
    print("\nCurrent Task List:")
    for idx, task in enumerate(tasks, 1):
        print(f"Task {idx}: {task}\n")

    try:
        task_index = int(input("Enter the task number you want to remove: "))
        if 1 <= task_index <= len(tasks):
            removed = tasks.pop(task_index - 1)
            print(f"Task '{removed}' removed successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

    print("\nUpdated Task List:")
    for idx, task in enumerate(tasks, 1):
        print(f"Task {idx}: {task}\n")

def main_func():
    
    #Main driver function for the task manager system.
    
    print("****** Welcome to the Task Manager ******")
    print("1. Register\n2. Login and Manage Tasks\n3. Exit\n")

    user_data = load_data()
    current_user = None

    while True:
        try:
            opt_int = int(input("Enter option: "))
        except ValueError:
            print("Invalid input. Please enter a number corresponding to an option.")
            continue

        if opt_int == 1:
            user_register(user_data)

        elif opt_int == 2:
            if current_user is None:
                current_user = user_login(user_data)
            if current_user is not None:
                print(f"\nWelcome, {current_user}!")
                print("Task Options:\n1. View tasks\n2. Add task\n3. Remove task\n4. Logout")
                try:
                    task_opt = int(input("Enter task option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if task_opt == 1:
                    open_task(user_data[current_user]["tasks"])
                    save_data(user_data)
                elif task_opt == 2:
                    enter_task(user_data[current_user]["tasks"])
                    save_data(user_data)
                elif task_opt == 3:
                    remove_task(user_data[current_user]["tasks"])
                    save_data(user_data)
                elif task_opt == 4:
                    print(f"User '{current_user}' logged out.")
                    current_user = None
                else:
                    print("Invalid task option.")

        elif opt_int == 3:
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid option. Please choose from the menu.")

if __name__ == '__main__':
    main_func()

