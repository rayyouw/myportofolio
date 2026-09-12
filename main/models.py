import uuid

from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Award(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    name = models.CharField(max_length=255)
    npm = models.CharField(max_length=50)
    study_program = models.CharField(max_length=255)
    bio_intro = models.TextField()
    events_count = models.PositiveIntegerField(default=0)
    organizations_count = models.PositiveIntegerField(default=0)
    focus_areas = models.JSONField(default=list, blank=True)
    competitions = models.JSONField(default=list, blank=True)
    photo = models.URLField(blank=True)
    cv_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    gallery = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    degree = models.CharField(max_length=255)
    courses = models.JSONField(default=list, blank=True)
    thumbnail = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.institution


class SkillCategory(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    name = models.CharField(max_length=255)
    thumbnail = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title