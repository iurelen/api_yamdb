import csv
import os
import re
import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import data from CSV file"

    def handle(self, *args, **kwargs):
        csv_files_path = os.path.normpath(kwargs['csv_files_path'])
        csv_files = self._get_csv_files(csv_files_path)
        conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
        cursor = conn.cursor()
        for name, path in csv_files:
            with open(path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                columns = tuple(next(csv_reader, None))
                for row in csv_reader:
                    query = f"INSERT INTO {name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
                    try:
                        cursor.execute(query, row)
                    except sqlite3.IntegrityError:
                        continue
        conn.commit()
        conn.close()


    def add_arguments(self, parser):
        parser.add_argument(
            'csv_files_path',
            type=str,
            help='Path to the CSV file'
        )

    def _get_csv_files(self, csv_files_path):
        files_list =[]
        path = os.path.join(settings.BASE_DIR, csv_files_path)
        for file in os.listdir(path):
            file_name = file.split('.')[0]
            path_to_file = os.path.join(path, file)
            if os.path.isfile(path_to_file) and file.endswith('csv'):
                files_list.append((file_name, path_to_file, ))
        return files_list
