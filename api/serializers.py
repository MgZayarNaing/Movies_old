from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__' 

class VideoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = '__all__'

    def create(self, validated_data):
        # Remove 'user' from validated_data if it's already included
        user = validated_data.pop('user', None)

        # If not provided, use the user from the request context
        if not user:
            user = self.context['request'].user

        return VideoComment.objects.create(user=user, **validated_data)
