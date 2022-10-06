from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api import views

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # function based view
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_details, name='movie-details')

    # class based view
    path('list/', views.WatchListAv.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchListDetailsAV.as_view(), name='movie-details'),
    #path('stream/', StreamPlatformListAV.as_view(), name='stream-platform'),
    #path('stream/<int:pk>/', StreamPlatformDetailsAV.as_view(),name='stream-platform-details'),
    # mixins and generics
    # path('reviews/', ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'),
    path('<int:pk>/review-create/',
         views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/',
         views.ReviewDetails.as_view(), name='review-details'),
    # veiwset
    path('', include(router.urls)),

    path('reviews/', views.UserReview.as_view(),
         name='user-review-details'),
    path('list-two/', views.WatchListGAV.as_view(),
         name='watch-list'),
]
