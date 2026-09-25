import pytest
from app.solver import solve_wfm_schedule

def test_solver_feasible_schedule():
    min_coverage = [[2, 2, 1] for _ in range(7)]
    
    result = solve_wfm_schedule(
        num_employees=10,
        days=7,
        shifts_per_day=3,
        min_coverage=min_coverage,
        preferences=[]
    )
    
    assert result["is_feasible"] is True
    assert result["status"] in ("OPTIMAL", "FEASIBLE")
    assert len(result["schedule"]) == 7

def test_solver_infeasible_schedule():
    min_coverage = [[10, 10, 10] for _ in range(7)]
    
    result = solve_wfm_schedule(
        num_employees=1,
        days=7,
        shifts_per_day=3,
        min_coverage=min_coverage,
        preferences=[]
    )
    
    assert result["is_feasible"] is False
    assert result["status"] == "INFEASIBLE"