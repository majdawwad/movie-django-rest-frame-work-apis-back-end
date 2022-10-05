from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='anas', password='anas@2257')
        self.token = Token.objects.get(user__username='anas')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", about="#1 Streaming Platform", website="https://www.netflix.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://www.netflix.com"
        }

        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_indiviual(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_put_indiviual(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform - Updated!",
            "website": "https://www.netflix.com"
        }
        response = self.client.put(
            reverse('streamplatform-detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_delete_indiviual(self):
        response = self.client.delete(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
