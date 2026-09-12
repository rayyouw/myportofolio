from django.contrib import admin

from main.models import (
    Award,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
)

admin.site.register(Award)
admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(Project)
