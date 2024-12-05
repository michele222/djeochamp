from django.core.management.base import BaseCommand

from game.models import Country, Parameter, CountryParameter


class Command(BaseCommand):
    help = "For each parameter, counts the countries and returns the missing ones"

    def handle(self, *args, **options):
        countries = Country.objects.all().values_list('id', flat=True)
        for parameter in Parameter.objects.all():
            countries_with_parameter = CountryParameter.objects.filter(parameter=parameter.id).values_list('country',
                                                                                                           flat=True)
            self.stdout.write(f'Parameter {parameter.id}: {parameter}. Countries: {len(countries_with_parameter)}')
            countries_missing = list(set(countries) - set(countries_with_parameter))
            if len(countries_missing) > 0:
                self.stdout.write(f'Missing {len(countries_missing)}: {countries_missing}')
