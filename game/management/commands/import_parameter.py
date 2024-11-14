from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from game.models import Country, Parameter, CountryParameter


class Command(BaseCommand):
    help = "Imports parameter file from comma separated csv"

    def add_arguments(self, parser):
        parser.add_argument("file", nargs="+")

    def handle(self, *args, **options):
        all_countries = Country.objects.all().values_list('id', flat=True)
        n_entries = 0
        for file_name in options["file"]:
            try:
                with open(Path(__file__).parent.parent.parent.joinpath('fixtures').joinpath(file_name), 'r') as file:
                    for line in file:
                        entry = line.strip().split(';')
                        if entry[0] in all_countries:
                            country_fk = Country.objects.get(id=entry[0])
                            parameter_fk = Parameter.objects.get(id=entry[1])
                            country_parameter = CountryParameter(country=country_fk,parameter=parameter_fk,value=entry[2])
                            country_parameter.save()
                            self.stdout.write(self.style.SUCCESS(entry[0]))
                            n_entries += 1
                        else:
                            self.stdout.write(self.style.ERROR(entry[0]))
                    self.stdout.write(self.style.SUCCESS(f'{n_entries} entries imported'))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f'File {file_name} not found'))