import pytest

from .factories import UserFactory, GameFactory

@pytest.fixture
def logged_user(client):
    user = UserFactory()
    client.login(username=user.username, password='password')
    return user

@pytest.mark.django_db
def test_list_endpoint_returns_user_games(client, logged_user):
    game = GameFactory(user=logged_user)
    second_game = GameFactory(user=logged_user)

    response = client.get('/game/')
    content = str(response.content)

    assert 200 == response.status_code
    assert game.title in content
    assert second_game.title in content
    assert 2 == content.count('<h3>')

@pytest.mark.django_db
def test_list_endpoint_only_returns_games_from_authenticated_user(client, logged_user):
    another_user_game = GameFactory()

    game = GameFactory(user=logged_user)
    second_game = GameFactory(user=logged_user)

    response = client.get('/game/')
    content = str(response.content)

    assert 200 == response.status_code
    assert game.title in content
    assert second_game.title in content
    assert another_user_game.title not in content
    assert 2 == content.count('<h3>')