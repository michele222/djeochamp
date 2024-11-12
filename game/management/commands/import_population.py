from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from game.models import Country, Parameter, CountryParameter


class Command(BaseCommand):
    help = "Imports population file"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        all_countries = Country.objects.all().values_list('id', flat=True)
        success = 0
        with open(Path(__file__).parent.parent.parent.joinpath('fixtures').joinpath('countries_population.csv'), 'r') as file:
            for line in file:
                entry = line.strip().split(',')
                if entry[0] in all_countries:
                    country_fk = Country.objects.get(id=entry[0])
                    parameter_fk = Parameter.objects.get(id=entry[1])
                    country_parameter = CountryParameter(country=country_fk,parameter=parameter_fk,value=entry[2])
                    country_parameter.save()
                    self.stdout.write(self.style.SUCCESS(entry[0]))
                    success += 1
                else:
                    self.stdout.write(self.style.ERROR(entry[0]))
        self.stdout.write(self.style.SUCCESS(f'{success=}'))