import pytest

from .factories import UserFactory, GameFactory, CountryFactory, ParameterFactory, CountryParameterFactory

@pytest.fixture
def logged_user(client):
    user = UserFactory()
    client.login(username=user.username, password='password')
    return user

@pytest.mark.django_db
def test_game_with_100_countries(client, logged_user):
    countries = CountryFactory.create_batch(100)
    parameters = ParameterFactory.create_batch(10)

    response = client.get('/game/countries/')
    content = str(response.content)
    assert 200 == response.status_code
    for country in countries:
        assert 1 == content.count(country.name)
        for parameter in parameters:
            CountryParameterFactory.create(country=country, parameter=parameter)

    response = client.get('/game/parameters/')
    content = str(response.content)
    assert 200 == response.status_code
    for parameter in parameters:
        assert 1 == content.count(parameter.name)

    game = GameFactory(user=logged_user)

    response = client.get(f'/game/{game.id}/details/')
    content = str(response.content)
    assert 200 == response.status_code
    assert 0 == content.count(countries[0].name)

    game.create_round()
    response = client.get(f'/game/{game.id}/details/')
    content = str(response.content)
    assert 200 == response.status_code
    for country in countries:
        assert 1 == content.count(country.name)

    assert game.title in content
    assert not game.winner

    num_participants = len(countries)

    while not game.winner:
        game.create_round()
        response = client.get(f'/game/{game.id}/details/')
        content = str(response.content)
        assert 200 == response.status_code
        countries = []
        for round in game.rounds.all():
            if round.is_latest:
                for match in round.matches.all():
                    countries.extend(list(match.countries.all()))
        assert len(countries) >= num_participants / 2
        num_participants = len(countries)

    assert game.winner in countries