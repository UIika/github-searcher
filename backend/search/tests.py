import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest import mock


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def redis_mock(monkeypatch):
    class FakeRedis:
        _cache = {}

        def get(self, key):
            return self._cache.get(key)

        def setex(self, key, timeout, value):
            self._cache[key] = value

        def keys(self, pattern):
            return list(self._cache.keys())

        def delete(self, *keys):
            for key in keys:
                self._cache.pop(key, None)

    fake_redis = FakeRedis()
    monkeypatch.setattr('search.views.redis_client', fake_redis)
    return fake_redis

@pytest.fixture
def github_mock():
    with mock.patch('search.views.fetch_from_github') as github_mock:
        yield github_mock


def test_search_github_valid_query(github_mock, api_client: APIClient, redis_mock):
    mock_response = {'items': [{'id': 1, 'name': 'test-repo'}]}
    github_mock.return_value = mock_response

    response = api_client.post(reverse('search-github'), {
        'type': 'repositories',
        'query': 'test'
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == mock_response


def test_search_github_invalid_input(github_mock, api_client: APIClient):
    response = api_client.post(reverse('search-github'), {
        'type': 'invalid_type',
        'query': 'test'
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data
    github_mock.assert_not_called()


def test_search_github_cache_hit(github_mock, api_client: APIClient, redis_mock):
    key = 'gh_search:' + 'dummyhash'
    redis_mock.setex(key, 7200, str({'items': [{'id': 99, 'cached': True}]}))

    with mock.patch('search.views.get_cache_key', return_value=key):
        response = api_client.post(reverse('search-github'), {
            'type': 'users',
            'query': 'cached-user'
        }, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['items'][0]['cached'] is True
    github_mock.assert_not_called()


def test_clear_cache(api_client: APIClient, redis_mock):
    redis_mock.setex('gh_search:test1', 7200, 'value1')
    redis_mock.setex('gh_search:test2', 7200, 'value2')

    assert len(redis_mock.keys('gh_search:*')) == 2

    response = api_client.post(reverse('clear-cache'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'Cache cleared.'
    assert len(redis_mock.keys('gh_search:*')) == 0
