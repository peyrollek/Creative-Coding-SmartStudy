import json
import os
from datetime import datetime

# SMARTSTUDY - UNIVERSITY ASSESSMENT PLANNER 

print("Welcome to Smartstudy!")
print("Your personal university assessment planner")

name = input("What is your name? ")
print("Nice to meet you;, " + name + "!")

course = input("What university course are you studying? ")
print("Let's organise your assessments for " + course + "!")

# Load previously saved assessments
file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assessments.json"
)

assessments = []

print("\nYour saved assessments:")
if assessments:
    for item in assessments:
        print(item["name"], "-", item["due_date"])
else:
    print("No assessments saved yet!")

#Add assessments
while True:
    assessment = input ("\nAssessment name: ").strip()

    if not assessment:
        print("Please enter an assessment name.")
        continue
    
    while True:
        due_date = input("Due date (DD/MM/YYYY): ").strip()
        
        try:
            datetime.strptime(due_date, "%d/%m/%Y")
            break
        except ValueError:
            print("Invalid date. Please use DD/MM/YYYY.")

# Avoid saving duplicate assessments
    duplicate = any(
        item["name"].lower() == assessment.lower()
        and item["due_date"] == due_date
        for item in assessments
    )

    if duplicate:
        print("This assessment is already saved!")
    else:
        assessments.append({
            "name": assessment,
            "due_date": due_date
        })
        print("Assessment added!")

    another = input(
        "Would you like to add another assessment? (yes/no): "
    ).strip().lower()

    while another not in ("yes", "no"):
        another = input("Please type yes or no: ").strip().lower()

    if another == "no":
        print("ALL assessments entered!")
        break

# Save assessments
with open(file_path, "w") as file:
    json.dump(assessments, file, indent=4)

# Sort assessments by deadline
assessments.sort(
    key=lambda item: datetime.strptime(
        item["due_date"], "%d/%m/%Y"
    )
)
print("\nYOUR ASSESSMENTS IN DEADLINE ORDER")
print("----------------------------------")

today = datetime.today().date()

for item in assessments:
    deadline = datetime.strptime(
        item["due_date"], "%d/%m/%Y"
    ).date()

    days_left = (deadline - today).days

    print("\nAssessment:", item["name"])
    print("Deadline:", item["due_date"])
    print("Days remaining:", days_left)

    if days_left < 0:
        print("OVERDUE!")
    elif days_left == 0:
        print("Your assessment is due TODAY!")
    elif days_left <= 7:
        print("URGENT! Prioritise this assessment!")
    else:
        print("You still have time!")

# Show top priority
print("\nYOUR TOP PRIOIRTY")

if assessments:
    first = assessments[0]
    print("You should work on:", first["name"])
    print("Deadline:", first["due_date"])
else:
    print("No assessments added yet!")

print("\nThank you for using SmartStudy!")