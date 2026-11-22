"""
requisition.py
Requisition System prototype (BACT7501 Assessment 2).

Contains the Requisition class, which stores one staff requisition and
provides methods to add items, approve, respond, display and report
statistics for all requisitions.
"""

from datetime import datetime

# Module-level settings (shared by every requisition)
AUTO_APPROVAL_LIMIT = 500      # totals below this are approved automatically
STARTING_REQUISITION_ID = 10000

# Status values kept in one place so spelling is always consistent
STATUS_PENDING = "Pending"
STATUS_APPROVED = "Approved"
STATUS_NOT_APPROVED = "Not approved"


class Requisition:
    """One staff requisition plus class-level tracking of all requisitions."""

    # Class (shared) data: one counter and one list for every object
    _next_id = STARTING_REQUISITION_ID
    _all_requisitions = []

    def __init__(self, staff_id, staff_name, date=None):
        """Initialise the shared data for a new requisition."""
        staff_id = str(staff_id).strip().upper()
        staff_name = str(staff_name).strip()
        if not staff_id:
            raise ValueError("Staff ID cannot be empty.")
        if not staff_name:
            raise ValueError("Staff name cannot be empty.")

        # Unique requisition ID from the shared counter
        Requisition._next_id += 1
        self.requisition_id = Requisition._next_id

        self.date = self._validate_date(date)
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.items = []                 # list of (item_name, cost)
        self.total = 0.0
        self.status = STATUS_PENDING
        self.approval_reference = None

        Requisition._all_requisitions.append(self)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_date(date):
        """Return a date string in DD/MM/YYYY. Uses today if none given."""
        if date is None:
            return datetime.now().strftime("%d/%m/%Y")
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date '{date}'. Use DD/MM/YYYY.")
        return date

    @staticmethod
    def format_money(amount):
        """Show 450 as '450' and 499.5 as '499.50' (no scientific notation)."""
        if float(amount).is_integer():
            return f"{int(amount)}"
        return f"{amount:.2f}"

    def _generate_reference(self):
        """Approval reference = Staff ID + last 3 digits of requisition ID."""
        return f"{self.staff_id}{str(self.requisition_id)[-3:]}"

    # ------------------------------------------------------------------
    # Task 1.5a  Data capture and computation
    # ------------------------------------------------------------------
    def add_requisition(self, items):
        """
        Accept a list of (item_name, cost) pairs, store them and
        return the requisition total.
        """
        if not items:
            raise ValueError("A requisition must contain at least one item.")

        clean_items = []   # validate everything first, then save
        for item in items:
            if len(item) != 2:
                raise ValueError(f"Item {item} must be (name, cost).")
            name, cost = item
            name = str(name).strip()
            if not name:
                raise ValueError("Item name cannot be empty.")
            try:
                cost = float(cost)
            except (TypeError, ValueError):
                raise ValueError(f"Cost for '{name}' must be a number.")
            if cost < 0:
                raise ValueError(f"Cost for '{name}' cannot be negative.")
            clean_items.append((name, cost))

        self.items.extend(clean_items)
        self.total = self.requisition_details()
        return self.total

    def requisition_details(self):
        """Calculate and return the total cost of all items."""
        return round(sum(cost for _, cost in self.items), 2)

    # ------------------------------------------------------------------
    # Task 1.5b  Decision-making
    # ------------------------------------------------------------------
    def approve_requisition(self):
        """
        Auto-decide the status from the total:
          total < $500  -> Approved (reference number created)
          total >= $500 -> Pending (waits for a manager)
        """
        self.total = self.requisition_details()
        if self.total < AUTO_APPROVAL_LIMIT:
            self.status = STATUS_APPROVED
            self.approval_reference = self._generate_reference()
        else:
            self.status = STATUS_PENDING
            self.approval_reference = None
        return self.status
