import json
from app.solver import solve_wfm_schedule

def main():
    # Define test parameters
    num_employees = 10
    days = 7
    shifts_per_day = 3  # 0: Morning, 1: Evening, 2: Night
    
    # Required staff per shift matrix [7 days x 3 shifts]
    min_coverage = [
        [3, 2, 1],  # Day 1
        [3, 2, 1],  # Day 2
        [3, 2, 1],  # Day 3
        [3, 2, 1],  # Day 4
        [3, 2, 1],  # Day 5
        [2, 1, 1],  # Day 6
        [2, 1, 1],  # Day 7
    ]

    # Optional employee shift preference requests
    # Format: {'employee': int, 'day': int, 'shift': int, 'weight': int}
    preferences = [
        {"employee": 0, "day": 0, "shift": 0, "weight": 5},  # Emp 0 wants Morning shift on Day 1
        {"employee": 1, "day": 0, "shift": 2, "weight": -5}, # Emp 1 avoids Night shift on Day 1
    ]

    print("Running OR-Tools CP-SAT Shift Scheduler...")
    
    result = solve_wfm_schedule(
        num_employees=num_employees,
        days=days,
        shifts_per_day=shifts_per_day,
        min_coverage=min_coverage,
        preferences=preferences
    )

    print("\n--- Solver Result ---")
    print(f"Status: {result['status']}")
    print(f"Feasible: {result['is_feasible']}\n")

    if result["is_feasible"]:
        print("Generated Schedule:")
        print(json.dumps(result["schedule"], indent=2))

if __name__ == "__main__":
    main()