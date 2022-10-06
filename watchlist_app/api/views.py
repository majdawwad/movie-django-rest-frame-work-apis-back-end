from django.shortcuts import get_object_or_404

# from rest_framework.decorators import api_view
#from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, response, views, viewsets, status, generics, exceptions, permissions, throttling

from watchlist_app import models
from watchlist_app.api import permissions, serializers, throttling, pagination


# function based view
# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return response.Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):

#     if request.method == 'GET':

#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return response.Response({'error message': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
#         else:
#             return response.Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return response.Response(status=status.HTTP_204_NO_CONTENT)

# class based view

class StreamPlatformListAV(views.APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        platform = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return response.response.Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailsAV(views.APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            stream = models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return response.Response({'error message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StreamPlatformSerializer(
            stream, context={'request': request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        stream = models.StreamPlatform.objects.get(pk=pk)
        serializer = serializers.StreamPlatformSerializer(
            stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return response.Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        stream = models.StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAv(views.APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailsAV(views.APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return response.Response({'error message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListSerializer(movie)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = models.WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return response.Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        movie = models.WatchList.objects.get(pk=pk)
        movie.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

# mixins


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# generic concrete class-based views
class ReviewList(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    #permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewListThrottle,
                        throttling.AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'review-details'


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return models.Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = models.WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = models.Review.objects.filter(
            watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            raise exceptions.ValidationError(
                "You have already reviewed this movie!")

        if movie.number_ratings == 0:
            movie.avg_ratings = serializer.validated_data['rating']
        else:
            movie.avg_ratings = (
                movie.avg_ratings + serializer.validated_data['rating']) / 2

        movie.number_ratings = movie.number_ratings + 1
        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)

# veiwaets


# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return response.Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         movie = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(movie)
#         return response.Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
#         else:
#             return response.Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         stream.delete()
#         return response.Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer

# filtering , searching, ordering
class UserReview(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return models.Review.objects.filter(review_user__username=username)


class WatchListGAV(generics.ListAPIView):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    #filter_backends = [filters.SearchFilter]
    #search_fields = ['title', 'platform__name']
    #search_fields = ['=title', 'platform__name']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_ratings']

    #pagination_class = WatchListPaginationNumber
    #pagination_class = WatchListPaginationLimitOffset
    pagination_class = pagination.WatchListPaginationCursor
