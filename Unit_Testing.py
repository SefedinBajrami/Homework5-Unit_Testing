import unittest

def calculate_bonus(employee_table, department_table):
    if not employee_table or not department_table:
        return 1 

    max_sales = max(department_table.values(), default=0)
    eligible_departments = [dept for dept, sales in department_table.items() if sales == max_sales]

    if not eligible_departments or len(eligible_departments) == len(department_table):
        return 2 

    has_eligible_employees = any(
        employee['department'] in eligible_departments for employee in employee_table
    )

    if not has_eligible_employees:
        return 2 

    for employee in employee_table:
        if employee['department'] in eligible_departments:
            if employee['salary'] >= 15000 or employee['is_manager']:
                employee['salary'] += 100
            else:
                employee['salary'] += 200

    return 0  # Success

class TestBonusModule(unittest.TestCase):

    def test_no_entries_in_tables(self):
        """Test case where both tables are empty."""
        employee_table = []
        department_table = {}
        result = calculate_bonus(employee_table, department_table)
        self.assertEqual(result, 1)

    def test_no_employees_in_eligible_department(self):
        """Test case where no employees are in the department with maximum sales."""
        employee_table = [
            {'id': 1, 'department': 'D1', 'salary': 14000, 'is_manager': False}
        ]
        department_table = {'D1': 1000, 'D2': 2000}
        result = calculate_bonus(employee_table, department_table)
        self.assertEqual(result, 2)

    def test_salary_update_for_eligible_employees(self):
        """Test case where eligible employees receive the correct bonus."""
        employee_table = [
            {'id': 1, 'department': 'D2', 'salary': 14000, 'is_manager': False},
            {'id': 2, 'department': 'D2', 'salary': 15000, 'is_manager': False},
            {'id': 3, 'department': 'D2', 'salary': 16000, 'is_manager': True}
        ]
        department_table = {'D1': 1000, 'D2': 2000}
        result = calculate_bonus(employee_table, department_table)
        self.assertEqual(result, 0)
        self.assertEqual(employee_table[0]['salary'], 14200)  # $200 bonus
        self.assertEqual(employee_table[1]['salary'], 15100)  # $100 bonus
        self.assertEqual(employee_table[2]['salary'], 16100)  # $100 bonus

    def test_maximum_entries(self):
        """Test case with maximum entries in the tables."""
        employee_table = [
            {'id': i, 'department': 'D1', 'salary': 14000, 'is_manager': False}
            for i in range(65535)
        ]
        department_table = {'D1': 2000, 'D2': 1000}
        result = calculate_bonus(employee_table, department_table)
        self.assertEqual(result, 0)

    def test_all_departments_have_same_sales(self):
        """Test case where all departments have the same sales."""
        employee_table = [
            {'id': 1, 'department': 'D1', 'salary': 14000, 'is_manager': False},
            {'id': 2, 'department': 'D2', 'salary': 12000, 'is_manager': False},
            {'id': 3, 'department': 'D1', 'salary': 15000, 'is_manager': True},
            {'id': 4, 'department': 'D2', 'salary': 15500, 'is_manager': False}
        ]
        department_table = {'D1': 1000, 'D2': 1000}
        result = calculate_bonus(employee_table, department_table)
        self.assertEqual(result, 2)  # No unique maximum-sales department

if __name__ == '__main__':
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestBonusModule))
