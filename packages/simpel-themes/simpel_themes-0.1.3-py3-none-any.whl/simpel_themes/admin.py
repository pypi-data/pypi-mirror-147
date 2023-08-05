from django.contrib import admin

from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from .models import Category, FileModelTemplate, ModelTemplate, PathModelTemplate, ScreenShoot, StringModelTemplate
from .settings import themes_settings


class ScreenShootInline(admin.StackedInline):
    model = ScreenShoot
    extra = 0


@admin.register(Category)
class TemplateCategory(admin.ModelAdmin):
    list_display = ["name"]


class ModelTemplateAdmin(PolymorphicParentModelAdmin):
    child_models = [
        FileModelTemplate,
        PathModelTemplate,
        StringModelTemplate,
    ]


class FileModelTemplateAdmin(PolymorphicChildModelAdmin):
    index = False
    inlines = [ScreenShootInline]


class PathModelTemplateAdmin(PolymorphicChildModelAdmin):
    index = False
    inlines = [ScreenShootInline]


class StringModelTemplateAdmin(PolymorphicChildModelAdmin):
    index = False
    inlines = [ScreenShootInline]


admin.site.register(ModelTemplate, themes_settings.MODEL_TEMPLATE_ADMIN)
admin.site.register(FileModelTemplate, themes_settings.FILE_MODEL_TEMPLATE_ADMIN)
admin.site.register(PathModelTemplate, themes_settings.PATH_MODEL_TEMPLATE_ADMIN)
admin.site.register(StringModelTemplate, themes_settings.STRING_MODEL_TEMPLATE_ADMIN)
