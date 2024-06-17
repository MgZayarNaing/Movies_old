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
    replies = serializers.SerializerMethodField()

    class Meta:
        model = VideoComment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.replies.exists():
            return VideoCommentSerializer(obj.replies.all(), many=True).data
        return []
