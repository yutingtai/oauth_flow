from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .constants import GITHUB_OAUTH_URL


# Create your tests here.

class GetExchangeCodeTest(TestCase):
    def test_home_page_without_token_in_session(self):
        # GIVEN no access_token in session
        client_without_session = APIClient()

        # WHEN home page is open
        url = reverse('oauth_flow.github:home_page')
        response = client_without_session.get(url)

        # THEN return ok response with home template and github oauth url as button link
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'github/home.html')
        self.assertEqual(response.context['destination'], GITHUB_OAUTH_URL)

    def test_get_exchange_code_with_token(self):
        # GIVEN client with access_token in session
        client_with_session = APIClient()
        session = client_with_session.session
        session['access_token'] = "I'm a fake token 唷"
        session.save()

        # WHEN home page is called
        url = reverse('oauth_flow.github:home_page')
        response = client_with_session.get(url)

        # THEN return ok response with home template and 'show github repos' as button link
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'github/home.html')
        self.assertEqual(response.context['destination'], reverse('oauth_flow.github:repo'))


def side_effect_access_token_ok(*args, **kwargs):
    return create_response(
        json_body={'access_token': 'mock_access_token'},
        code=200
    )


def side_effect_401(*args, **kwargs):
    return create_response(
        json_body={},
        code=401
    )


def create_response(code, json_body):
    response = MagicMock()
    response.json = MagicMock(return_value=json_body)
    response.response_code = code
    return response


class GetAccessTokenTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('oauth_flow.github.views.requests.post', side_effect=side_effect_access_token_ok)
    def test_access_token_require(self, mock_post: MagicMock):
        # GIVEN GitHub can exchange code to token

        # WHEN get github_oauth_callback with code
        response = self.client.get(reverse('oauth_flow.github:access_token'), {'code': 'mock_exchange_code'})

        # THEN session have access token, and we should be redirected to repos
        self.assertEqual(self.client.session['access_token'], 'mock_access_token')

        expected_url = reverse('oauth_flow.github:repo')
        self.assertEqual(response.url, expected_url)

        mock_post.assert_called_once()
