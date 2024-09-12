from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Year

class Command(BaseCommand):
    help = 'Populates the Year model with years from 1886 to the next year'

    def add_arguments(self, parser):
        parser.add_argument('--start-year', type=int, default=1886, help='Starting year (default: 1886)')
        parser.add_argument('--end-year', type=int, help='Ending year (default: next year)')

    def handle(self, *args, **options):
        start_year = options['start_year']
        end_year = options['end_year'] or (timezone.now().year + 1)

        if start_year > end_year:
            self.stderr.write(self.style.ERROR('Starting year cannot be greater than ending year.'))
            return

        existing_years = set(Year.objects.values_list('year', flat=True))
        years_to_create = []

        for year in range(start_year, end_year + 1):
            if year not in existing_years:
                years_to_create.append(Year(year=year))

        Year.objects.bulk_create(years_to_create)

        created_count = len(years_to_create)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new years.'))