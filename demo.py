"""
demo.py
Test run for the Requisition System (Task 1, step 6).
Creates 5 requisitions covering different scenarios, shows statistics,
lets the manager respond, then shows the updated results.
"""

from requisition import Requisition


def submit(staff_id, staff_name, date, items):
    """Create a requisition, add its items, run auto-approval."""
    requisition = Requisition(staff_id, staff_name, date)
    total = requisition.add_requisition(items)
    status = requisition.approve_requisition()
    print(f"Submitted {requisition.requisition_id} for {staff_name}: "
          f"${Requisition.format_money(total)} -> {status}")
    return requisition


def main():
    print("STEP 1: Submitting requisitions\n")

    # Under $500 -> approved automatically
    r1 = submit("FN19", "John Paul", "03/04/2024",
                [("Printer paper", 150), ("Toner", 300)])            # $450
    r4 = submit("FN02", "Catlin White", "03/05/2024",
                [("Desk lamp", 90), ("Office chair", 400)])          # $490

    # $500 or more -> pending, needs a manager
    r2 = submit("FN20", "Tracy Brown", "05/04/2024",
                [("Monitor", 600), ("Keyboard", 400)])               # $1000
    r3 = submit("FN15", "Emma Wellington", "07/05/2024",
                [("Laptop", 3000), ("Docking station", 500)])        # $3500
    r5 = submit("FN07", "Liam Smith", "10/05/2024",
                [("Training course", 500)])                          # exactly $500 (edge case)

    print("\nSTEP 2: Requisitions and statistics before manager response\n")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()

    print("STEP 3: Manager responds to requisitions of $500 or more\n")
    r2.respond_requisition("pending")        # left as pending
    r3.respond_requisition("not approved")
    r5.respond_requisition("approved")
    r1.respond_requisition("not approved")   # already approved, so rejected safely

    print("\nSTEP 4: Requisitions and statistics after manager response\n")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()

    print("STEP 5: Input validation checks\n")
    bad_inputs = [
        ("Empty item list", lambda: Requisition("FN30", "Test User").add_requisition([])),
        ("Negative cost", lambda: Requisition("FN31", "Test User").add_requisition([("Pen", -5)])),
        ("Text as cost", lambda: Requisition("FN32", "Test User").add_requisition([("Pen", "ten")])),
        ("Bad date", lambda: Requisition("FN33", "Test User", "2024-13-40")),
    ]
    for label, action in bad_inputs:
        try:
            action()
        except ValueError as error:
            print(f"{label}: caught error -> {error}")


if __name__ == "__main__":
    main()
