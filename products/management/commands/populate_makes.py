from django.core.management.base import BaseCommand
from products.models import Make

class Command(BaseCommand):
    help = 'Populates the database with car, truck, and SUV makes in the USA'

    def handle(self, *args, **kwargs):
        makes = [
            "Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Buick", "Cadillac", 
            "Chevrolet", "Chrysler", "Dodge", "Ferrari", "Fiat", "Ford", "Genesis", "GMC", 
            "Honda", "Hyundai", "Infiniti", "Jaguar", "Jeep", "Kia", "Lamborghini", "Land Rover", 
            "Lexus", "Lincoln", "Lotus", "Maserati", "Mazda", "McLaren", "Mercedes-Benz", "Mini", 
            "Mitsubishi", "Nissan", "Porsche", "Ram", "Rolls-Royce", "Subaru", "Tesla", "Toyota", 
            "Volkswagen", "Volvo"
        ]

        for make in makes:
            Make.objects.get_or_create(name=make)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {make}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated makes'))