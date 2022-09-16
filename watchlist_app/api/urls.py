from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import WatchListAv, WatchListDetailsAV, StreamPlatformListAV, StreamPlatformDetailsAV
urlpatterns = [
    # function based view
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_details, name='movie-details')

    # class based view
    path('list/', WatchListAv.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailsAV.as_view(), name='movie-details'),
    path('stream/', StreamPlatformListAV.as_view(), name='stream-platform'),
    path('stream/<int:pk>/', StreamPlatformDetailsAV.as_view(),
         name='stream-platform-details'),
]
