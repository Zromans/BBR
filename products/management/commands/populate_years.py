from django.core.management.base import BaseCommand
from products.models import Year
import datetime

class Command(BaseCommand):
    help = 'Populates the Year model with years from 1950 to next year'

    def handle(self, *args, **kwargs):
        current_year = datetime.date.today().year
        for year in range(1886, current_year + 2):
            Year.objects.get_or_create(year=year)
        self.stdout.write(self.style.SUCCESS('Successfully populated years'))
