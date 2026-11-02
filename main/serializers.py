from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)
    tech_stack = serializers.CharField(required=True)
    star_count = serializers.IntegerField(source="starred_by.count", read_only=True)
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
            "image",
            "tags",
            "year",
            "highlights",
            "link",
            "order",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = [
            "id",
            "image",
            "tags",
            "year",
            "highlights",
            "link",
            "order",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_title(self, value):
        cleaned = strip_tags(value).strip()
        if cleaned != value.strip() or not cleaned:
            raise serializers.ValidationError(
                "Project name must contain visible text without HTML tags."
            )
        return cleaned

    def validate_description(self, value):
        cleaned = strip_tags(value).strip()
        if cleaned != value.strip():
            raise serializers.ValidationError("Description must not contain HTML tags.")
        return cleaned

    def validate_tech_stack(self, value):
        return strip_tags(value).strip()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(obj.starred_by.values_list("username", flat=True))
