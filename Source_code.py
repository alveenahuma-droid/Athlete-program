from tkinter import *

# Constants
PLAN_FEES   = {1: 25.00, 2: 30.00, 3: 35.00}
PLAN_NAMES  = {1: 'Beginner', 2: 'Intermediate', 3: 'Elite'}
PRIVATE_RATE   = 9.50
COMPETITION_FEE = 22.00
WEEKS_PER_MONTH = 4
MAX_PRIVATE_HRS = 5
COMPETITION_ELIGIBLE = {2, 3}

WEIGHT_LIMITS = [
    (66,  'Flyweight'),
    (73,  'Lightweight'),
    (81,  'Light-Middleweight'),
    (90,  'Middleweight'),
    (100, 'Light-Heavyweight'),
]

def fmt(amount: float) -> str:
    return f'£{amount:.2f}'

# get category based on competition weight
def get_category(weight: float):
    for limit, name in WEIGHT_LIMITS:
        if weight <= limit:
            return limit, name
    return None, 'Heavyweight'  

# OOP Classes
class Athlete:
    def __init__(self, name, plan_id, current_wt, comp_wt, competitions, priv_hours):
        self.name = name
        self.plan_id = plan_id
        self.current_wt = current_wt
        self.comp_wt = comp_wt
        self.competitions = competitions
        self.priv_hours = priv_hours

    def get_weekly_fee(self):
        return PLAN_FEES[self.plan_id]

class CostCalculator:
    def __init__(self, athlete):
        self.athlete = athlete

    def calculate_total(self):
        training = self.athlete.get_weekly_fee() * WEEKS_PER_MONTH

        # eligibility check
        if self.athlete.plan_id in COMPETITION_ELIGIBLE:
            comp_cost = self.athlete.competitions * COMPETITION_FEE
        else:
            comp_cost = 0

        priv_cost = self.athlete.priv_hours * PRIVATE_RATE * WEEKS_PER_MONTH

        return training + comp_cost + priv_cost

# GUI functions
def toggle_private():
    if private_var.get():
        priv_entry.config(state='normal')
    else:
        priv_entry.config(state='disabled')
        priv_entry.delete(0, END)

def on_calculate_click():
    try:
        # Private coaching optional
        priv_hours = float(priv_entry.get()) if private_var.get() else 0.0

        name = name_entry.get().strip()
        if not name:
            result_label.config(text='Enter name')
            return

        plan_id = int(plan_entry.get())
        if plan_id not in PLAN_FEES:
            result_label.config(text='Plan must be 1, 2 or 3')
            return

        athlete = Athlete(
            name=name,
            plan_id=plan_id,
            current_wt=float(curr_weight_entry.get()),
            comp_wt=float(comp_weight_entry.get()),
            competitions=int(comp_entry.get()),
            priv_hours=priv_hours
        )

        calculator = CostCalculator(athlete)
        total = calculator.calculate_total()
        

        limit, cat = get_category(athlete.comp_wt)

        
        if athlete.plan_id in COMPETITION_ELIGIBLE:
            comp_cost = athlete.competitions * COMPETITION_FEE
        else:
            comp_cost = 0
    
        report = f"Selected Plan: {PLAN_NAMES[athlete.plan_id]} (£{PLAN_FEES[athlete.plan_id]:.2f}/week)\n"
        report += f"\nTraining Cost: £{athlete.get_weekly_fee() * WEEKS_PER_MONTH:.2f}\n"
        report += f"Competition Cost: £{comp_cost:.2f}\n"
        report += f"Private Cost: £{athlete.priv_hours * PRIVATE_RATE * WEEKS_PER_MONTH:.2f}\n"
        report += f"TOTAL: £{total:.2f}\n"

        # Weight message
        if limit is None:
            wt_msg = f'Heavyweight (no upper limit). Current: {athlete.current_wt} kg'
        elif athlete.current_wt > limit:
            wt_msg = f'OVER limit by {athlete.current_wt - limit:.1f} kg (limit: {limit} kg)'
        else:
            wt_msg = f'Within {cat} limit ({limit} kg). {limit - athlete.current_wt:.1f} kg below limit'

        report += f"Weight: {wt_msg}"

        result_label.config(text=report)

    except ValueError:
        result_label.config(text="Invalid input. Please enter numbers correctly.")

# GUI SETUP
root = Tk()
root.title("North Sussex Judo – Cost Calculator")

plans_text = "Plans Available:\n"
for k, v in PLAN_NAMES.items():
    plans_text += f"  {k} – {v} (£{PLAN_FEES[k]:.2f}/week)\n"

Label(root, text=plans_text, justify=LEFT).pack()

Label(root, text="Name").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root, text="Plan (1-3)").pack()
plan_entry = Entry(root)
plan_entry.pack()

Label(root, text="Current Weight (kg)").pack()
curr_weight_entry = Entry(root)
curr_weight_entry.pack()

Label(root, text="Competition Weight (kg)").pack()
comp_weight_entry = Entry(root)
comp_weight_entry.pack()

Label(root, text="Competitions").pack()
comp_entry = Entry(root)
comp_entry.pack()

private_var = BooleanVar()
Checkbutton(root, text="Add Private Coaching?", variable=private_var, command=toggle_private).pack()

Label(root, text="Private Hours per Week (0-5)").pack()
priv_entry = Entry(root)
priv_entry.pack()
priv_entry.config(state='disabled')

Button(root, text="Calculate", command=on_calculate_click).pack()

result_label = Label(root, text="", justify=LEFT)
result_label.pack()

root.mainloop()


    