from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (ReviewDetails, ReviewList, WatchListAv,
                                     WatchListDetailsAV, StreamPlatformListAV, StreamPlatformDetailsAV, ReviewCreate, StreamPlatformVS)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='stream-platform')

urlpatterns = [
    # function based view
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_details, name='movie-details')

    # class based view
    path('list/', WatchListAv.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailsAV.as_view(), name='movie-details'),
    #path('stream/', StreamPlatformListAV.as_view(), name='stream-platform'),
    #path('stream/<int:pk>/', StreamPlatformDetailsAV.as_view(),name='stream-platform-details'),
    # mixins and generics
    # path('reviews/', ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'),
    path('stream/<int:pk>/reviews-create/',
         ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('stream/reviews/<int:pk>/',
         ReviewDetails.as_view(), name='review-details'),
    # veiwset
    path('', include(router.urls))
]
