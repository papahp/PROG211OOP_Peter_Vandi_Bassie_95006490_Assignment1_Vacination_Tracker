# Community Vaccination Tracker

PROG211 Object-Oriented Programming 1 | Limkokwing University of Creative Technology, Sierra Leone
Student: Peter Vandi Bassie (ID 905006490) | Class: B.I.T 1101

A small Python program that helps a health worker record vaccine doses and see who is fully vaccinated and who is still due a dose. It is written with Object-Oriented Programming (OOP) and follows Digital Public Goods (DPG) standards.

## The problem

Paper vaccination registers are easy to lose and hard to total up. Health workers need a simple way to record doses, see the next due date and count coverage, without storing anything that identifies a person.

## How to run

Requires Python 3.8 or newer. No other packages.

```
python vaccination_tracker.py
```

## Files

| File | Purpose |
|---|---|
| `vaccination_tracker.py` | The program (source code) |
| `sample_output.txt` | Example input and output |
| `LICENSE` | MIT licence (open source) |
| `README.md` | This file |

## OOP concepts used

| Concept | Where |
|---|---|
| Classes with attributes | `Vaccine`, `Recipient` |
| Objects and interaction | A `Recipient` holds a `Vaccine` object |
| One data structure | A dictionary `registry`, keyed by record ID |
| Instance methods | `record_dose()`, `is_complete()`, `next_due_date()`, `display_info()` |
| Class methods (`@classmethod`) | `Recipient.from_text()`, `Recipient.count_records()` |
| Static method (`@staticmethod`) | `Recipient.is_valid_id()` |
| Tuples (optional) | `DISTRICTS`, `AGE_GROUPS` constants |

## How it meets the DPG standards

| DPG principle | How this project meets it |
|---|---|
| Open source | Code is public on GitHub under the MIT licence. Anyone can read, copy and improve it. |
| Inclusive and accessible | Plain numbered menu, plain English, no colour or mouse needed, input errors explained in words. Works on any computer that runs Python. |
| Privacy-respecting | No names, phone numbers or addresses. A record holds an anonymous code (VT-0001), an age group, a district and dose counts. |
| Modular and reusable | `Vaccine` and `Recipient` have no menu code inside them, so another program can import and reuse them. Schedules are data, so new vaccines are one line each. |

Vaccine schedules in the program are sample values for teaching. They are not medical guidance.

## Example usage

```
Choose an option: 3
  Record ID: VT-0001
  Dose recorded. 2 of 2 done.

Choose an option: 4
  Record ID: VT-0001
  Record ID : VT-0001
  Age group : 1-4 years
  District  : Bo
  Vaccine   : Measles-Rubella
  Doses     : 2 of 2
  Status    : COMPLETE
```

More examples are in `sample_output.txt`.

## Licence

MIT. See `LICENSE`.
