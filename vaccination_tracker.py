"""
Community Vaccination Tracker
PROG211 - Object-Oriented Programming 1 (Assignment: DPG Standards)

Domain : Health (Vaccination Tracker)
Author : Peter Vandi Bassie

What it does
------------
Health workers record vaccine doses given to people in a district and see
who is fully vaccinated, who is still due a dose, and when that dose is due.

Digital Public Goods (DPG) notes
--------------------------------
* Privacy-respecting : no names, phone numbers or addresses are stored.
  Each person is an anonymous record code such as VT-0001.
* Inclusive          : plain menu, plain English, no colour or mouse needed.
* Modular / reusable : Vaccine and Recipient can be imported into other code.
* Open source        : released under the MIT licence (see LICENSE).
"""

from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Constants (tuples: fixed lists that the program never changes)
# ---------------------------------------------------------------------------
DISTRICTS = (
    "Bo", "Bombali", "Bonthe", "Falaba", "Kailahun", "Kambia", "Karene",
    "Kenema", "Koinadugu", "Kono", "Moyamba", "Port Loko", "Pujehun",
    "Tonkolili", "Western Area Rural", "Western Area Urban",
)

AGE_GROUPS = ("0-11 months", "1-4 years", "5-14 years", "15-49 years", "50+ years")


# ---------------------------------------------------------------------------
# Task 1 - Classes, attributes and objects
# ---------------------------------------------------------------------------
class Vaccine:
    """A vaccine and the schedule it follows (illustrative values only)."""

    def __init__(self, name, doses_required, days_between_doses):
        self.name = name
        self.doses_required = doses_required
        self.days_between_doses = days_between_doses

    def describe(self):
        """Return a one-line description of the vaccine schedule."""
        return (f"{self.name}: {self.doses_required} dose(s), "
                f"{self.days_between_doses} days apart")


class Recipient:
    """One anonymous person who is receiving a vaccine."""

    total_records = 0   # class attribute shared by every Recipient

    def __init__(self, record_id, age_group, district, vaccine):
        self.record_id = record_id          # anonymous code, e.g. VT-0001
        self.age_group = age_group          # a group, never an exact age
        self.district = district
        self.vaccine = vaccine              # a Vaccine object (object interaction)
        self.doses_received = 0
        self.last_dose_date = None
        Recipient.total_records += 1

    # ---- Task 3: instance methods ----------------------------------------
    def record_dose(self, given_on=None):
        """Record one dose. Returns False when the course is already complete."""
        if self.is_complete():
            return False
        self.doses_received += 1
        self.last_dose_date = given_on or date.today()
        return True

    def is_complete(self):
        """True when the person has had every dose the vaccine needs."""
        return self.doses_received >= self.vaccine.doses_required

    def next_due_date(self):
        """Date the next dose is due, or None if complete or not started."""
        if self.is_complete() or self.last_dose_date is None:
            return None
        return self.last_dose_date + timedelta(days=self.vaccine.days_between_doses)

    def display_info(self):
        """Print the record in a readable block."""
        if self.is_complete():
            status = "COMPLETE"
        elif self.doses_received == 0:
            status = "NOT STARTED"
        else:
            status = f"IN PROGRESS, next dose due {self.next_due_date()}"
        print(f"  Record ID : {self.record_id}")
        print(f"  Age group : {self.age_group}")
        print(f"  District  : {self.district}")
        print(f"  Vaccine   : {self.vaccine.name}")
        print(f"  Doses     : {self.doses_received} of {self.vaccine.doses_required}")
        print(f"  Status    : {status}")

    # ---- Task 3: class method and static method --------------------------
    @classmethod
    def from_text(cls, text, vaccine):
        """Build a Recipient from 'VT-0001,5-14 years,Bo'. Class method."""
        record_id, age_group, district = [part.strip() for part in text.split(",")]
        return cls(record_id, age_group, district, vaccine)

    @classmethod
    def count_records(cls):
        """How many Recipient objects have been created. Class method."""
        return cls.total_records

    @staticmethod
    def is_valid_id(record_id):
        """True for codes shaped like VT-0001. Static method (no self/cls)."""
        return (len(record_id) == 7 and record_id.startswith("VT-")
                and record_id[3:].isdigit())


# ---------------------------------------------------------------------------
# Task 2 - One data structure: a dictionary keyed by record ID
# ---------------------------------------------------------------------------
def add_record(registry, recipient):
    """Add a Recipient to the registry dictionary. Returns True if added."""
    if recipient.record_id in registry:
        return False                         # IDs must be unique
    registry[recipient.record_id] = recipient
    return True


def display_records(registry):
    """Loop through the dictionary and show every record."""
    if not registry:
        print("  No records yet.")
        return
    for record_id in sorted(registry):
        registry[record_id].display_info()
        print("  " + "-" * 40)


def coverage_summary(registry):
    """Print how many records are complete and how many are still open."""
    total = len(registry)
    complete = sum(1 for r in registry.values() if r.is_complete())
    print(f"  Records in registry : {total}")
    print(f"  Fully vaccinated    : {complete}")
    print(f"  Still due a dose    : {total - complete}")
    if total:
        print(f"  Coverage            : {complete / total * 100:.0f}%")


# ---------------------------------------------------------------------------
# Menu helpers (input and output)
# ---------------------------------------------------------------------------
def pick_from(title, options):
    """Show a numbered list and return the chosen item."""
    print(title)
    for number, option in enumerate(options, start=1):
        label = option.name if isinstance(option, Vaccine) else option
        print(f"    {number}. {label}")
    while True:
        choice = input("  Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("  Please enter a number from the list.")


def menu_add(registry, vaccines):
    print("\n--- Add a record ---")
    record_id = input("  New record ID (format VT-0001): ").strip().upper()
    if not Recipient.is_valid_id(record_id):
        print("  Invalid ID. Use the format VT-0001.")
        return
    if record_id in registry:
        print(f"  Record {record_id} already exists. Nothing saved.")
        return
    age_group = pick_from("  Age group:", AGE_GROUPS)
    district = pick_from("  District:", DISTRICTS)
    vaccine = pick_from("  Vaccine:", vaccines)
    add_record(registry, Recipient(record_id, age_group, district, vaccine))
    print(f"  Saved record {record_id}.")


def menu_dose(registry):
    print("\n--- Record a dose ---")
    record_id = input("  Record ID: ").strip().upper()
    person = registry.get(record_id)
    if person is None:
        print("  No record with that ID.")
        return
    if person.record_dose():
        print(f"  Dose recorded. {person.doses_received} of "
              f"{person.vaccine.doses_required} done.")
    else:
        print("  This person has already completed the course.")


def menu_search(registry):
    print("\n--- Find a record ---")
    record_id = input("  Record ID: ").strip().upper()
    person = registry.get(record_id)
    if person is None:
        print("  No record with that ID.")
    else:
        person.display_info()


def main():
    vaccines = [
        Vaccine("Measles-Rubella", 2, 180),
        Vaccine("Pentavalent", 3, 28),
        Vaccine("Yellow Fever", 1, 0),
    ]
    registry = {}

    # Two starter records so the program has something to show
    start = Recipient.from_text("VT-0001,1-4 years,Bo", vaccines[0])
    add_record(registry, start)
    start.record_dose(date.today() - timedelta(days=30))
    second = Recipient.from_text("VT-0002,0-11 months,Kenema", vaccines[2])
    add_record(registry, second)

    print("=" * 46)
    print("  COMMUNITY VACCINATION TRACKER")
    print("  No names or contact details are stored.")
    print("=" * 46)

    while True:
        print("\n1. Add a record")
        print("2. Show all records")
        print("3. Record a dose")
        print("4. Find a record by ID")
        print("5. Coverage summary")
        print("6. Show vaccine schedules")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            menu_add(registry, vaccines)
        elif choice == "2":
            print("\n--- All records ---")
            display_records(registry)
        elif choice == "3":
            menu_dose(registry)
        elif choice == "4":
            menu_search(registry)
        elif choice == "5":
            print("\n--- Coverage summary ---")
            coverage_summary(registry)
            print(f"  Recipient objects created: {Recipient.count_records()}")
        elif choice == "6":
            print("\n--- Vaccine schedules ---")
            for vaccine in vaccines:
                print("  " + vaccine.describe())
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Please choose 0 to 6.")


if __name__ == "__main__":
    main()
