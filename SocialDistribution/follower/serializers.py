from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from SocialDistribution.authors.models import Author
from SocialDistribution.authors.serializers import AuthorSerializer
from SocialDistribution.follower.models import FollowRequest, Follower


class FollowerSerializer(ModelSerializer):

    class Meta:
        model = Follower
        fields = ['type', 'user', 'item']


class FollowerRequestSerializer(serializers.ModelSerializer):
    actor = AuthorSerializer(many=False, required=True)
    object = AuthorSerializer(many=False, required=True)

    class Meta:
        model = FollowRequest
        fields = ("type", "summary", "actor", "object")
