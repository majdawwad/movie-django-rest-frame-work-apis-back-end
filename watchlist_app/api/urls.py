from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import MovieListAv, MovieDetailsAV
urlpatterns = [
    # function based view
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_details, name='movie-details')

    # class based view
    path('list/', MovieListAv.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailsAV.as_view(), name='movie-details')
]
