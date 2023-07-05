from django.shortcuts import render, redirect
import requests
from django.urls import reverse

from .constants import GITHUB_OAUTH_URL
from .serializer import RepositoryInfoSerializer
from dotenv import load_dotenv, find_dotenv
import os


# request.session.get will set the default value = None is key doesn't exist.
def home_page(request):
    if request.session.get('access_token') is None:
        context = {
            "destination": GITHUB_OAUTH_URL
        }
        return render(request, 'github/home.html', context=context)
    else:
        context = {
            "destination": reverse('oauth_flow.github:repo')
        }
        return render(request, 'github/home.html', context=context)


def github_oauth_callback(request):
    load_dotenv(find_dotenv())
    client_secret = os.environ['client_secret']
    exchange_code = request.GET.get('code')
    params = {
        "client_id": "89f6bf27704fa92ade50",
        "client_secret": client_secret,
        "code": exchange_code
    }

    response = requests.post(
        'https://github.com/login/oauth/access_token',
        params=params,
        headers={"Accept": "application/json"}
    )

    if response.status_code == 200:
        pass

    access_token_response = response.json()

    access_token = access_token_response['access_token']
    request.session['access_token'] = access_token

    return redirect(reverse('oauth_flow.github:repo'))


def repo_page(request):
    access_token = request.session.get('access_token')
    repos_url = 'https://api.github.com/user/repos'
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    repo_info_response = requests.get(repos_url, headers=header)
    if repo_info_response.status_code == 401:
        return redirect(GITHUB_OAUTH_URL)
    else:
        repo_info_response = repo_info_response.json()
        serializer = RepositoryInfoSerializer(data=repo_info_response, many=True)
        serializer.is_valid(raise_exception=True)
        all_repo_info = serializer.save()

        context = {
            "all_repo_info": all_repo_info
        }
        return render(request, 'github/show_repo.html', context)
