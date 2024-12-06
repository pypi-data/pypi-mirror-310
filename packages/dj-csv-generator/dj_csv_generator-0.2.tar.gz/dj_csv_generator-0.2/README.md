Django CSV Generator
====================

A Django application containing CsvGenerator base class to be used with
Django QuerySet to generate CSV report for list of objects, preferably
Django models.

Features
--------

* Can return HTTP response containing generated CSV file.
* Convenient to use with Django admin actions.

Installation
------------

1. Install package in your project: `pip install dj-csv-generator`
2. Add `'csv_generator'` to `INSTALLED_APPS` in your `settings.py`
3. In your code import base generator class: `from csv_generator.generator import CsvGenerator`
4. Create your own CSV generator class derived from `CsvGenerator` and customize it. You can use `project/example` as reference.
5. Use your generator to generate CSV file:
```
generator = YourCsvGeneratorClass()

# if you need plain text data, use:
rows = generator.process_data(YourDjangoModel.objects.all())

# if you need HttpResponse, for example to return in your view, use:
response = generator.get_response(YourDjangoModel.objects.all())
```

Generator options and use cases
---------
...In progress...