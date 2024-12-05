from django.core.management.base import BaseCommand, CommandError
from game.models import Country, Parameter, CountryParameter


class Command(BaseCommand):
    help = "Executes the code. Used for quick checks"

    def handle(self, *args, **options):
        all_countries = Country.objects.all().values_list('id', flat=True)
        countries_medals = CountryParameter.objects.filter(parameter=4).values_list('country', flat=True)
        for country in all_countries:
            if country in countries_medals:
                self.stdout.write(self.style.SUCCESS(country))
            else:
                self.stdout.write(self.style.ERROR(country))
