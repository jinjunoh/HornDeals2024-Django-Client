from rest_framework import serializers
from .models import Post


# The Serializer is what converts data to JSON so that the frontend or client
# understands the Django model instances or querysets
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' 