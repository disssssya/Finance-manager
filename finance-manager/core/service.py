from core.transforms import filter_month, sum_by_category, sum_amounts

class BudgetService:
    def __init__(self, validators=None, calculators=None):
        self.validators = validators or []
        self.calculators = calculators or []

    def monthly_report(self, data, month):
        for validator in self.validators:
            data = validator(data)
        data_month = filter_month(data, month)
        report = 0  
        for t in data_month:
            cat_id = t.get("cat_id")
            if cat_id is None:
                for calc in self.calculators:
                    report += calc([t])
            else:
                if not isinstance(report, dict):
                    report = {}
                if cat_id not in report:
                    report[cat_id] = 0
                for calc in self.calculators:
                    report[cat_id] += calc([t], cat_id)
        return report

class ReportService:
    def __init__(self, aggregators=None):
        self.aggregators = aggregators or []

    def category_report(self, data, cat_id):
        report = {}
        for agg in self.aggregators:
            if agg.__name__ == "sum_by_category":
                report[cat_id] = agg(data, cat_id)
            else:
                report[cat_id] = agg(report.get(cat_id, 0), cat_id)
        return report
