from rest_framework import serializers
from .models import Question, Option, UserSubmission

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']
        extra_kwargs = {
            'is_correct': {'write_only': True}  # Hide is_correct in GET requests for users
        }

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'positive_points', 'negative_points', 'options']

class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = ['id', 'question', 'selected_option', 'score', 'created_at']
        read_only_fields = ['score']  # Score will be calculated automatically

class QuestionDetailAdminSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'positive_points', 'negative_points', 'options', 'created_at', 'updated_at']
