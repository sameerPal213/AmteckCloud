# skillAssessments/management/commands/create_users_from_employees.py
from sys import stdout
from django.core.management.base import BaseCommand
from skillAssessments.models import User
from coins.models import Employee

class Command(BaseCommand):
    help = 'Create users from employees'

    def handle(self, *args, **options):
        for employee in Employee.objects.all():
            try:
                User.objects.get(employee_ptr=employee)
                stdout.write(f'A User record for {employee.first_name} {employee.last_name} already exists.\n')
                continue
            except:
                new_user = User(employee_ptr_id = employee.pk)
                new_user.__dict__.update(employee.__dict__)
                new_user.save()
                stdout.write(f'User Record {new_user.pk} created for {employee.first_name} {employee.last_name}\n')

