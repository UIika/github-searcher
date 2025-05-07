from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import redis
import hashlib
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)

GITHUB_API_URL = 'https://api.github.com/search/'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
CACHE_TIMEOUT = 7200  # 2 hours


def get_cache_key(search_type: str, query: str):
    hash_key = hashlib.sha256(f'{search_type}:{query}'.encode()).hexdigest()
    return f'gh_search:{hash_key}'


def fetch_from_github(search_type: str, query: str):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    url = f'{GITHUB_API_URL}{search_type}?q={query}&per_page=10'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'GitHub API error: {response.status_code}')
    return response.json()

search_type_param = openapi.Parameter(
    'type',
    openapi.IN_BODY,
    description='Type of entity to search ("users" or "repositories")',
    type=openapi.TYPE_STRING
)
query_param = openapi.Parameter('query', openapi.IN_BODY, description='Search term', type=openapi.TYPE_STRING)


@swagger_auto_schema(
    method='post',
    operation_description='Search GitHub for users or repositories. Results are cached for 2 hours.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['type', 'query'],
        properties={
            'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['users', 'repositories']),
            'query': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={200: 'Search results', 400: 'Invalid input', 500: 'GitHub API error'}
)
@api_view(['POST'])
def search_github(request):
    data = request.data
    search_type = data.get('type')
    query = data.get('query')

    if not search_type or not query or search_type not in ['users', 'repositories']:
        return Response({'error': 'Invalid search parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = get_cache_key(search_type, query)
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return Response(eval(cached_data))

    try:
        result = fetch_from_github(search_type, query)
        redis_client.setex(cache_key, CACHE_TIMEOUT, str(result))
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    operation_description='Clear the Redis cache of all stored GitHub search results.',
    responses={200: 'Cache cleared', 500: 'Cache clearing error'}
)
@api_view(['POST'])
def clear_cache(request):
    try:
        keys = redis_client.keys('gh_search:*')
        if keys:
            redis_client.delete(*keys)
        return Response({'status': 'Cache cleared.'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
