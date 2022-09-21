# from wsgiref.validate import validator
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


# serializers.Serializer class :
# validators ..


# def validate_name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name length must not be short")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[validate_name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     # field level validation
#     # def validate_name(self, value):

#     #     if len(value) < 3:
#     #         raise serializers.ValidationError('name is too short!')
#     #     else:
#     #         return value

#     # object level validation
#     def validate(self, data):

#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'name and description should not be the same!')
#         else:
#             return data

# -----------------------------------------------------------------------------------------
# serializers.ModelSerializer class :

class ReviewSerializer(serializers.ModelSerializer):

    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        #fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):

    # length_title = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        # fields = ['id', 'title', 'storyline', 'created']
        fields = "__all__"
        # exclude = ['active']  # access to all fields except active

    # def get_length_title(self, object):
    #     return len(object.title)

    # # field level validation
    # def validate_title(self, value):

    #     if len(value) < 3:
    #         raise serializers.ValidationError('title is too short!')
    #     else:
    #         return value

    # # object level validation
    # def validate(self, data):

    #     if data['title'] == data['storyline']:
    #         raise serializers.ValidationError(
    #             'title and storyline should not be the same!')
    #     else:
    #         return data


class StreamPlatformSerializer(serializers.ModelSerializer):

    # Nested relationships return all fields for a object
    watchlist = WatchListSerializer(many=True, read_only=True)
    # StringRelatedField return single field (name or title) of a object
    # watchlist = serializers.StringRelatedField(many=True)
    # PrimaryKeyRelatedField return pk field of a object
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # HyperlinkedRelatedField return hyper link field of a object
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-details')
    # SlugRelatedField return slug field of a object
    # watchlist = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    # HyperlinkedIdentityField return hyperlinked identity field of a object
    # watchlist = serializers.HyperlinkedIdentityField(view_name='movie-details')

    class Meta:
        model = StreamPlatform
        fields = "__all__"


# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):

#     # Nested relationships return all fields for a object
#     watchlist = WatchListSerializer(many=True, read_only=True)

#     class Meta:
#         model = StreamPlatform
#         fields = "__all__"
