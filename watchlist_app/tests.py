from multiprocessing.connection import wait
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

    # def test_streamplatform_put_indiviual(self):
    #     data = {
    #         "name": "Netflix",
    #         "about": "#1 Streaming Platform - Updated!",
    #         "website": "https://www.netflix.com"
    #     }
    #     response = self.client.put(
    #         reverse('streamplatform-detail', args=(self.stream.id,)), data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_streamplatform_delete_indiviual(self):
    #     response = self.client.delete(
    #         reverse('streamplatform-detail', args=(self.stream.id,)))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='anas', password='anas@2257')
        self.token = Token.objects.get(user__username='anas')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", about="#1 Streaming Platform", website="https://www.netflix.com")
        self.watchlist = models.WatchList.objects.create(
            title="Batman", storyline="A story man called The Bat Man", active=True, platform=self.stream
        )

    def test_watchlist_create(self):
        data = {
            "title": "Batman",
            "storyline": "A story man called The Bat Man",
            "active": True,
            "platform": self.stream
        }

        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_individual(self):
        response = self.client.get(
            reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, "Batman")


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='anas', password='anas@2257')
        self.token = Token.objects.get(user__username='anas')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", about="#1 Streaming Platform", website="https://www.netflix.com")
        self.watchlist = models.WatchList.objects.create(
            title="Batman", storyline="A story man called The Bat Man", active=True, platform=self.stream
        )
        self.watchlist2 = models.WatchList.objects.create(
            title="Spiderman", storyline="A story man called The Spider Man", active=True, platform=self.stream
        )
        self.review = models.Review.objects.create(
            review_user=self.user, rating=5, description="Great Movie!", active=True, watchlist=self.watchlist2)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "active": True,
            "watchlist": self.watchlist
        }

        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,
                         status.HTTP_429_TOO_MANY_REQUESTS)

    def test_review_create_unathenticated_user(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "active": True,
            "watchlist": self.watchlist
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good Movie!",
            "active": False,
            "watchlist": self.watchlist
        }
        response = self.client.put(
            reverse('review-details', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list_in_watchlist(self):
        response = self.client.get(
            reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_indiviual_in_watchlist(self):
        response = self.client.get(
            reverse('review-details', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get(
            '/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
