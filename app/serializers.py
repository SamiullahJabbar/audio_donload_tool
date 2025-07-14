# # api/serializers.py

# from rest_framework import serializers

# class VideoURLSerializer(serializers.Serializer):
#     url = serializers.URLField()

# from rest_framework import serializers

# class FormatSerializer(serializers.Serializer):
#     url = serializers.CharField(required=True)
#     format_id = serializers.CharField(required=True)
#     has_audio = serializers.BooleanField(required=True)




from rest_framework import serializers

class YouTubeURLSerializer(serializers.Serializer):
    url = serializers.URLField()