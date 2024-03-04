import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from collects.models import Collect, Payment


class Command(BaseCommand):
    help = 'Loads data from .csv files to DB'

    def handle(self, *args, **options):

        MODELS_FILES = {
            Collect: 'collect.csv',
            # Payment: 'payment.csv',  # по неведомым причинам не импортирует
        }

        for model, file in MODELS_FILES.items():
            with open(f'./static/data/{file}', encoding='utf-8') as csv_data:
                csv_reader = csv.DictReader(csv_data, delimiter=',')
                rows = []

                for row in csv_reader:
                    for mod in MODELS_FILES.keys():
                        mod_name = mod.__name__.lower()
                        for field, value in row.items():
                            if mod_name == field or (
                                mod_name == 'user' and field == 'author'
                            ):
                                row[field] = get_object_or_404(mod, id=value)
                    item = model(**row)
                    rows.append(item)

                model.objects.bulk_create(rows, ignore_conflicts=True)
                print('Data uploaded to models succesful.')
