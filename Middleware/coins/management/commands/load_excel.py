# coins/management/commands/load_excel.py
# vim: ai ts=4 sts=4 et sw=4

from django.db.models.fields.related import RelatedField
import openpyxl
import locale
from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db.models import (
        DateField, BooleanField, DecimalField, CharField, IntegerField, 
        DateTimeField)
from django.apps import apps
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

locale.setlocale(locale.LC_ALL, '')

class Command(BaseCommand):
    """
    A Django management command to load data from an excel file into a Django model.
    """

    help = 'Load data from an excel file into a Django model'
    true_values = ['yes','y']
    false_values = ['no','n']

    def add_arguments(self, parser):
        """
        Add command line arguments for the file path, app and model name.
        """
        parser.add_argument('file_path', type=str, 
                            help='Path to the Excel File')
        parser.add_argument('model_name', type=str,
                            help='Name of the model being loaded')
        parser.add_argument('app_name', type=str,
                            help='Name of the app containing the model')

    def process_field(self, field, field_value):
        """
        Handles the conversion of the source data to a format that can be used.

        Args:
            field: The field object representing the model field.
            field_value: The value of the field from the excel sheet.

        Returns:
            The processed value of the field.
        """
        # Convert Date Fields 
        if isinstance(field, DateField):
            try:
                if type(field) == DateField:
                    return self.convert_date(field_value)
                else:
                    return self.convert_datetime(field_value)

            except:
                raise ValueError(f'Could not convert "{field_value}" to date in column {field}')

        # Convert Boolean Fields
        elif isinstance(field, BooleanField):
            try:
                if field_value is None:
                    return False
                elif field_value == 1:
                    return True
                elif field_value ==0:
                    return False
                elif field_value.lower() in self.true_values:
                    return True
                elif field_value.lower() in self.false_values:
                    return False
            except:
                raise ValueError(f'Could not convert "{field_value}" to boolean in column {field}')
        # Convert Decimal Fields
        elif isinstance(field, DecimalField):
            try:
                if field_value == None:
                    return 0
                else:
                    return locale.atof(str(field_value))
            except:
                raise ValueError(f'Could not convert "{field_value}" to decimal in column {field}')
        # Convert Character Fields
        elif isinstance(field, CharField):
            try:
                return str(field_value)
            except:
                raise ValueError(f'Could not convert "{field_value}" to string in column {field}')
        # Convert Integer Fields
        elif isinstance(field, IntegerField):
            try:
                if field_value == '' or field_value == None:
                    return 0
                else:
                    return int(field_value)
            except:
                raise ValueError(f'Could not convert "{field_value}" to integer in column {field}')
        # Get object from id for keys
        elif isinstance(field, RelatedField):
            try:
                # if the value is the related objects id
                if isinstance(field_value, int):
                    model = field.related_model
                    related = model.objects.get(id=field_value)
                    return related
                else:
                    return None
            except:
                raise ValueError(f'Could not find instance of {model} with key "{field_value}"')
        # Catch other field types
        else:
            return field_value

    def process_row(self, row):
        """
        Takes a row from the excel sheet and converts it to a dict of column names and values.

        Args:
            row: The row from the excel sheet.

        Returns:
            A dictionary containing the column names and values.
        """
        # Create empty dict to store the row values
        data_dict = {}

        # Loop over each field of the model and then check if it exists in the import sheet
        # This enables the import sheet to not have all columns.
        for field in self.model_fields:
            field_name = field.name
            if field_name in self.headers:
                data_dict[field_name] = self.process_field(
                        field, 
                        row[self.headers.index(field_name)])

        return data_dict

    def convert_date(self, value):
        """
        Converts a date value to a Python date object.

        Args:
            value: The date value to be converted.

        Returns:
            The converted Python date object.

        Raises:
            ValueError: If no valid date format is found.
        """
        if value:
            for format in ('%m/%d/%y', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y', ):
                try:
                    return datetime.strptime(str(value), format).date()
                except ValueError:
                    pass
            raise ValueError(f'no valid date format found for {value}')

    def convert_datetime(self, value):
        """
        Converts a datetime value to a Python datetime object.

        Args:
            value: The datetime value to be converted.

        Returns:
            The converted Python datetime object.

        Raises:
            ValueError: If no valid datetime format is found.
        """
        if value:
            for format in ("%Y%m%d", "%m/%d/%Y %H:%M:%S"):
                try:
                    date = datetime.strptime(str(value).split(".")[0], format)
                    if date.minute == 0 and date.hour == 0:
                        time = timedelta(
                                seconds = int(str(value).split(".",1)[1]))
                        return make_aware(date + time)
                    else:
                        return make_aware(date)
                except ValueError:
                    pass
            raise ValueError('no valid datetime format found')
        
    def handle(self, *args, **kwargs):
        """
        Handles the execution of the command.

        Args:
            args: The command line arguments.
            kwargs: The keyword arguments.

        Raises:
            Exception: If an error occurs during the execution.
        """
        # Pull in arguments
        file_path = kwargs['file_path']
        app_name = kwargs['app_name']
        model_name = kwargs['model_name']

        try:
            # Load the excel workbook
            workbook = openpyxl.load_workbook(file_path)
            self.sheet = workbook.active

            # Get the model
            self.model = apps.get_model(app_label=app_name, model_name=model_name)

            # get workbook headers
            self.headers = [cell.value for cell in self.sheet[1]]

            # Get the model field names
            self.model_fields = self.model._meta.get_fields()

            # Iterate over rows starting from the second row (skip header row)
            for row in tqdm(
                    self.sheet.iter_rows( min_row=2, values_only=True), 
                    total=self.sheet.max_row-1,
                    desc='Inserting Rows'):
                # Create a model with the dynamically collected fields
                self.data_dict = self.process_row(row)
                self.model.objects.create(**self.data_dict)
            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
