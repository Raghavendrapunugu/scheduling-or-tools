from typing import List, Dict, Any
from ortools.sat.python import cp_model

def solve_wfm_schedule(
    num_employees: int,
    days: int,
    shifts_per_day: int,
    min_coverage: List[List[int]],
    preferences: List[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    Solves call center shift scheduling using OR-Tools CP-SAT.
    """
    model = cp_model.CpModel()
    
    # Decision Variables: shift_vars[(e, d, s)] == 1 if employee e works shift s on day d
    shift_vars = {}
    for e in range(num_employees):
        for d in range(days):
            for s in range(shifts_per_day):
                shift_vars[(e, d, s)] = model.NewBoolVar(f"shift_e{e}_d{d}_s{s}")

    # Constraint 1: Maximum 1 shift per day per employee
    for e in range(num_employees):
        for d in range(days):
            model.Add(sum(shift_vars[(e, d, s)] for s in range(shifts_per_day)) <= 1)

    # Constraint 2: Satisfy minimum shift coverage requirements
    for d in range(days):
        for s in range(shifts_per_day):
            required = min_coverage[d][s]
            model.Add(sum(shift_vars[(e, d, s)] for e in range(num_employees)) >= required)

    # Constraint 3: Maximum 5 days per rolling 6-day window
    for e in range(num_employees):
        for d_start in range(days - 5):
            model.Add(
                sum(
                    shift_vars[(e, d, s)]
                    for d in range(d_start, d_start + 6)
                    for s in range(shifts_per_day)
                ) <= 5
            )

    # Objective Function: Soft optimization for employee preferences
    objective_terms = []
    if preferences:
        for pref in preferences:
            e, d, s, weight = pref['employee'], pref['day'], pref['shift'], pref['weight']
            objective_terms.append(shift_vars[(e, d, s)] * weight)
            
    if objective_terms:
        model.Maximize(sum(objective_terms))

    # Solver Execution
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule = []
        for d in range(days):
            day_schedule = {"day": d, "shifts": []}
            for s in range(shifts_per_day):
                assigned = [
                    e for e in range(num_employees)
                    if solver.BooleanValue(shift_vars[(e, d, s)])
                ]
                day_schedule["shifts"].append({"shift": s, "assigned_employees": assigned})
            schedule.append(day_schedule)
            
        return {
            "status": solver.StatusName(status),
            "is_feasible": True,
            "schedule": schedule
        }
    
    return {"status": solver.StatusName(status), "is_feasible": False, "schedule": []}