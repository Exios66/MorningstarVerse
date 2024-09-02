# ToDo List Application for Mobile

tasks = []

def show_menu():
    print("\nMenu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Save Tasks")
    print("5. Load Tasks")
    print("6. Exit")

def add_task():
    task = input("Enter the task: ")
    if task:
        tasks.append(task)
        print(f"Task added: {task}")
    else:
        print("No task entered.")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour tasks:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")

def remove_task():
    if not tasks:
        print("No tasks to remove.")
        return
    view_tasks()
    try:
        task_num = int(input("Enter the task number to remove: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f"Removed: {removed_task}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def save_tasks(filename="tasks.txt"):
    try:
        with open(filename, 'w') as file:
            file.writelines(task + '\n' for task in tasks)
        print(f"Tasks saved to {filename}")
    except Exception as e:
        print(f"Error saving tasks: {e}")

def load_tasks(filename="tasks.txt"):
    try:
        with open(filename, 'r') as file:
            tasks.clear()
            tasks.extend(line.strip() for line in file)
        print(f"Tasks loaded from {filename}")
    except FileNotFoundError:
        print(f"No tasks found in {filename}.")
    except Exception as e:
        print(f"Error loading tasks: {e}")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            remove_task()
        elif choice == '4':
            save_tasks()
        elif choice == '5':
            load_tasks()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please select a valid option.")

if __name__ == "__main__":
    main()