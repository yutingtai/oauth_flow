from unittest.mock import patch, MagicMock

from django.test import TestCase, RequestFactory, Client
from unittest import mock
from django.urls import reverse
from rest_framework.test import APIClient, RequestsClient
from .views import access_token_require


# Create your tests here.

class GetExchangeCodeTest(TestCase):
    def setUp(self):
        self.client_without_session = APIClient()
        self.client_with_session = APIClient()
        session = self.client_with_session.session
        session['access_token'] = "I'm a fake token 唷"
        session.save()

    def test_get_exchange_code_without_token(self):
        authenticated_url = 'https://github.com/login/oauth/authorize?client_id=89f6bf27704fa92ade50&scope=repo%20user3Astatus'
        url = reverse('oauth_flow.github:home_page')
        response = self.client_without_session.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'github/home.html')
        self.assertEqual(response.context['destination'], authenticated_url)

    def test_get_exchange_code_with_token(self):
        url = reverse('oauth_flow.github:home_page')
        response = self.client_with_session.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'github/home.html')
        self.assertEqual(response.context['destination'], reverse('oauth_flow.github:repo'))


class GetAccessTokenTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    @patch('oauth_flow.github.views.redirect')
    @patch('oauth_flow.github.views.requests')
    def test_access_token_require(self, mock_redirect, mock_post):
        mock_access_token_response = {
            'access_token': 'mock_access_token'
        }

        mock_post.return_value = mock_access_token_response

        request = self.client.get(reverse('oauth_flow.github:access_token'), {'code': 'mock_exchange_code'})
        response = access_token_require(request)
        self.assertEqual(request.session['access_token'], 'mock_access_token')

        expected_url = reverse('oauth_flow.github:repo')
        mock_redirect.assert_called_once_with(expected_url)

        self.assertEqual(response, mock_redirect.return_value)

        mock_post.assert_called_once_with('https://github.com/login/oauth/access_token')
