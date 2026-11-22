"""
main.py
Interactive terminal menu for the Requisition System.
The user types all the data (staff details, items, costs, manager decisions).
"""

from requisition import Requisition, STATUS_PENDING


# ----------------------------------------------------------------------
# Input helpers (keep asking until the input is valid)
# ----------------------------------------------------------------------
def ask_text(prompt):
    """Ask for text that cannot be empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty. Please try again.")


def ask_cost(prompt):
    """Ask for a cost that is a number and not negative."""
    while True:
        value = input(prompt).strip().replace("$", "")
        try:
            cost = float(value)
        except ValueError:
            print("  Please enter a number, for example 150 or 99.50.")
            continue
        if cost < 0:
            print("  Cost cannot be negative.")
            continue
        return cost


def ask_date(prompt):
    """Ask for a DD/MM/YYYY date. Blank means today."""
    while True:
        value = input(prompt).strip()
        if not value:
            return None
        try:
            return Requisition._validate_date(value)
        except ValueError as error:
            print(f"  {error}")


# ----------------------------------------------------------------------
# Menu actions
# ----------------------------------------------------------------------
def submit_requisition():
    print("\n--- Submit a Requisition ---")
    date = ask_date("Date (DD/MM/YYYY, press Enter for today): ")
    staff_id = ask_text("Staff ID: ")
    staff_name = ask_text("Staff Name: ")

    items = []
    print("Enter items. Press Enter on an empty item name to finish.")
    while True:
        name = input(f"  Item {len(items) + 1} name: ").strip()
        if not name:
            if items:
                break
            print("  You must enter at least one item.")
            continue
        cost = ask_cost(f"  Cost of {name}: $")
        items.append((name, cost))

    requisition = Requisition(staff_id, staff_name, date)
    total = requisition.add_requisition(items)
    status = requisition.approve_requisition()

    print(f"\nRequisition {requisition.requisition_id} submitted.")
    print(f"Total: ${Requisition.format_money(total)}")
    print(f"Status: {status}")
    if status == STATUS_PENDING:
        print("Total is $500 or more, so it needs a manager's response.")


def manager_respond():
    print("\n--- Manager Response ---")
    pending = [r for r in Requisition._all_requisitions if r.status == STATUS_PENDING]
    if not pending:
        print("There are no pending requisitions.")
        return

    print("Pending requisitions:")
    for r in pending:
        print(f"  {r.requisition_id}  {r.staff_name}  ${Requisition.format_money(r.total)}")

    while True:
        value = input("Enter Requisition ID to respond to (or Enter to cancel): ").strip()
        if not value:
            return
        if not value.isdigit():
            print("  Please enter a number.")
            continue
        requisition = Requisition.find(int(value))
        if requisition is None:
            print("  No requisition with that ID.")
        elif requisition.status != STATUS_PENDING:
            print(f"  That requisition is already '{requisition.status}'.")
        else:
            break

    choices = {"1": "approved", "2": "not approved", "3": "pending"}
    while True:
        choice = input("1 = Approve, 2 = Not approve, 3 = Leave pending: ").strip()
        if choice in choices:
            break
        print("  Please enter 1, 2 or 3.")

    status = requisition.respond_requisition(choices[choice])
    print(f"Requisition {requisition.requisition_id} is now: {status}")


def show_menu():
    print("\n========== Requisition System ==========")
    print("1. Submit a requisition")
    print("2. Manager: respond to a pending requisition")
    print("3. Display all requisitions")
    print("4. Display requisition statistics")
    print("5. Exit")


def main():
    actions = {
        "1": submit_requisition,
        "2": manager_respond,
        "3": Requisition.display_requisitions,
        "4": Requisition.requisition_statistics,
    }
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please enter a number from 1 to 5.")
            continue
        print()
        action()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
