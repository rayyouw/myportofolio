from django.contrib import admin

from main.models import (
    Award,
    Certificate,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "order")
    search_fields = ("title", "description", "tech_stack")
    filter_horizontal = ("starred_by",)


admin.site.register(Award)
admin.site.register(Certificate)
admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(SkillCategory)
admin.site.register(Skill)
