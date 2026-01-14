from django.contrib import admin
from .models import Lawyer, Comment, Law, LawHistory, LawComment, FavoriteLaw


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "rating", "com", "created_at")
    list_editable = ("status", "rating", "com")
    search_fields = ("name", "description")
    list_filter = ("status", "created_at")
    readonly_fields = ("slug", "created_at")

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("name", "description", "status", "image_url")},
        ),
        ("Статистика", {"fields": ("rating", "com", "closed", "succses", "stazh")}),
        ("Контакты", {"fields": ("phone",)}),
        (
            "Служебные поля",
            {"fields": ("slug", "created_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "lawyer", "created_at")
    list_filter = ("lawyer", "created_at")
    search_fields = ("text", "author__username")
    readonly_fields = ("created_at",)


@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "title",
        "category",
        "status",
        "is_active",
        "views_count",
        "date_published",
    )
    list_editable = ("status", "is_active")
    list_filter = ("category", "status", "is_active", "date_published")
    search_fields = ("title", "number", "description", "full_text")
    readonly_fields = ("slug", "views_count", "date_updated", "created_at")
    date_hierarchy = "date_published"

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("title", "number", "category")},
        ),
        ("Текст закона", {"fields": ("description", "full_text")}),
        (
            "Статус и даты",
            {"fields": ("status", "is_active", "date_published", "date_updated")},
        ),
        ("Статистика", {"fields": ("views_count",)}),
        (
            "Служебные поля",
            {"fields": ("slug", "created_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(LawHistory)
class LawHistoryAdmin(admin.ModelAdmin):
    list_display = ("law", "changed_by", "created_at")
    list_filter = ("law", "created_at", "changed_by")
    search_fields = ("law__title", "change_description")
    readonly_fields = ("created_at",)


@admin.register(LawComment)
class LawCommentAdmin(admin.ModelAdmin):
    list_display = ("author", "law", "created_at")
    list_filter = ("law", "created_at", "author")
    search_fields = ("text", "author__username", "law__title")
    readonly_fields = ("created_at",)


@admin.register(FavoriteLaw)
class FavoriteLawAdmin(admin.ModelAdmin):
    list_display = ("user", "law", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "law__title")
