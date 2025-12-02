from core.service import BudgetService, ReportService
from core.transforms import filter_month, sum_amounts, sum_by_category

def test_budget_service():
    data = [{"month": "2025-01", "amount": 100}, {"month": "2025-02", "amount": 50}]
    svc = BudgetService(
        validators=[lambda d: filter_month(d, "2025-01")],
        calculators=[sum_amounts]
    )
    result = svc.monthly_report(data, "2025-01")
    assert result == 100

def test_report_service():
    data = [{"cat_id": "food", "amount": 100}, {"cat_id": "tech", "amount": 50}]
    svc = ReportService(aggregators=[sum_by_category])
    result = svc.category_report(data, "food")
    assert result["food"] == 100

def test_multiple_validators():
    data = [{"month": "2025-01", "amount": 100}, {"month": "2025-01", "amount": 50}]
    svc = BudgetService(
        validators=[
            lambda d: filter_month(d, "2025-01"),
            lambda d: [t for t in d if t["amount"] > 50]
        ],
        calculators=[sum_amounts]
    )
    result = svc.monthly_report(data, "2025-01")
    assert result == 100

def test_multiple_aggregators():
    data = [{"cat_id": "food", "amount": 100}, {"cat_id": "food", "amount": 50}]
    svc = ReportService(
        aggregators=[sum_by_category, lambda total, cat_id: total * 2]
    )
    result = svc.category_report(data, "food")
    assert result["food"] == 300
