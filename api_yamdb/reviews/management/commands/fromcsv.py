import glob

import pandas as pd
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads data from csv into database'

    def handle(self, *args, **options):
        all_files = glob.glob('*.csv')

        for filename in all_files:
            pd.read.csv(filename, index_col=None, header=0)
