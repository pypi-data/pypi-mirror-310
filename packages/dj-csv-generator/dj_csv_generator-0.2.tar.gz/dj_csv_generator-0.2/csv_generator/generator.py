import csv
import typing

from io import StringIO
from enum import Enum

from datetime import datetime, date

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import formats
from django.utils.translation import gettext_lazy as _


class CsvGenerator:
    """
    Base CSV generator class which is able to return http response.
    Intended to work with QuerySets of Django models.
    """
    # names of the fields which will be added to CSV file as columns
    # - set in derived class
    field_names = []

    # cols mapped to their names - set in derived class
    header_row = {}

    # default file name of the generated CSV file - can be overridden
    file_name = ('{name}.csv'.format(name=_('report')))

    class Const:
        
        class BomMode(Enum):
            NO_BOM = 'NO_BOM'  # to omit BOM prefix in a file
            SINGLE_BOM = 'SINGLE_BOM'  # standard BOM prefix
            DOUBLE_BOM = 'DOUBLE BOM'  # to ensure that browser won't cut the BOM prefix off the file

        TRUE_VAL = _('YES')
        FALSE_VAL = _('NO')
        DEFAULT_BOM_VALUE = b'\xef\xbb\xbf'
        DEFAULT_BOM_MODE = BomMode.DOUBLE_BOM

    # Override this in derived class to change BOM value and BOM mode
    BOM_MODE = Const.DEFAULT_BOM_MODE
    BOM_VALUE = Const.DEFAULT_BOM_VALUE

    def __init__(self):
        pass

    def get_field_names(self) -> list:
        """
        Override this method to add dynamic columns to the CSV file along with
        get_header_row method.
        """
        return self.field_names

    def get_header_row(self) -> dict:
        """
        Override this method to add dynamic columns to the CSV file along with
        get_field_names method.
        """
        return self.header_row

    def get_val(self, name: str, obj: models.Model) -> typing.Any:
        """
        Tries to return value of obj by given attribute name.
        Supports nesting of objects by using "double underscore" notation:
            e.g.: "obj__obj_attr__nested_attr__further_nested_attr"
            will be considered as: obj.obj_attr.nested_attr.further_nested_attr
            Returns None if any of the parts doesn't exist.
        """
        parts = name.split('.')
        fn_name = f'get_{name}'
        if hasattr(self, fn_name):
            val = getattr(self, fn_name)(obj)
        else:
            val = obj
            for part in parts:
                try:
                    val = getattr(val, part)
                except ObjectDoesNotExist:
                    val = None
                if callable(val):
                    val = val()
                if val is None:
                    break
        return val

    @classmethod
    def format_val(cls, val: typing.Any) -> str:
        """
        Converts object's value to it's string representation.
        """
        Const = cls.Const
        if isinstance(val, bool):
            val = Const.TRUE_VAL if val else Const.FALSE_VAL
        elif isinstance(val, datetime):
            val = formats.date_format(val, 'SHORT_DATETIME_FORMAT')
        elif isinstance(val, date):
            val = formats.date_format(val, 'SHORT_DATE_FORMAT')
        return '{0}'.format(val or '')

    def get_file_name(self, context: dict = None) -> str:
        return self.file_name

    def get_context_data(self, data: typing.Iterable) -> dict:
        return {
            'field_names': self.get_field_names(),
            'header_row': self.get_header_row(),
            'rows': self.process_data(data)
        }

    def process_row(self, obj: object) -> dict:
        row = {}
        for f_name in self.get_field_names():
            row[f_name] = self.get_val(f_name, obj)
        return row

    def process_data(self, data: typing.Iterable) -> list:
        return [self.process_row(row) for row in data]

    def get_file_obj(self, data, delimiter: str = ';') -> StringIO:
        context = self.get_context_data(data)
        file_obj = StringIO()

        # Adding BOM bytes to be friendly for MS Excel
        bom_value = self.BOM_VALUE.decode('utf-8')
        if self.BOM_MODE != self.Const.BomMode.NO_BOM:
            file_obj.write(bom_value)
        if self.BOM_MODE == self.Const.BomMode.DOUBLE_BOM:
            file_obj.write(bom_value)

        writer = csv.DictWriter(
            file_obj,
            delimiter=delimiter,
            dialect=csv.excel,
            fieldnames=context['field_names']
        )
        writer.writerow(
            {k: v for k, v in context['header_row'].items()}
        )
        for row in context['rows']:
            writer.writerow({k: self.format_val(v) for k, v in row.items()})
        file_obj.seek(0)
        return file_obj

    def get_response(
        self, data: typing.Iterable, delimiter: str = ';'
    ) -> HttpResponse:
        """
        Call this method passing data iterable (preferably Django Model
        QuerySet) to get HTTP response containing CSV report file.
        """
        context = self.get_context_data(data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            self.get_file_name(context)
        )
        with self.get_file_obj(data) as file_obj:
            for line in file_obj.readlines():
                response.write(line)
        return response
