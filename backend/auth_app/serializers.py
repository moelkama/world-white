from rest_framework import serializers

from .models import CustomUser ,all_Match

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'display_name', 'username', 'email', 'photo_profile', 'score', 'win', 'lose', 'ranking', 'total_match', 'is_online']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = all_Match
        fields = ['winner', 'loser', 'date','score1','score2']