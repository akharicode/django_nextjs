from django.contrib import admin
from django import forms
from .models import Category, Post, Heading
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget

# --- Category ---
class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Descripción breve…"}),
            "title": forms.TextInput(attrs={"size": 60}),
            "name": forms.TextInput(attrs={"size": 60}),
        }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ("name", "title", "parent", "slug")
    search_fields = ("name", "title", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent",)
    ordering = ("name",)
    readonly_fields = ("id",)


# --- Post ---
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(
                config_name='default',
                attrs={'class': 'django_ckeditor_5'},
            )
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("title", "category", "status", "created_at", "updated_at")
    search_fields = ("title", "description", "content", "keywords", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("status", "category", "updated_at")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        ("General Information", {
            "fields": ("title", "description", "content", "thumbnail", "keywords", "slug", "category")
        }),
        ("Status & Dates", {
            "fields": ("status", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    # Sugerencia: autocompletado para FK (usa un widget de admin muy cómodo)
    autocomplete_fields = ("category",)  # CategoryAdmin ya tiene search_fields: OK


# --- Heading ---
class HeadingAdminForm(forms.ModelForm):
    class Meta:
        model = Heading
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"size": 60}),
            "order": forms.NumberInput(attrs={"min": 1}),
        }

@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    form = HeadingAdminForm
    list_display = ("title", "level", "post", "order")
    search_fields = ("title", "post__title")
    list_filter = ("level", "post")
    ordering = ("post", "order")
    prepopulated_fields = {"slug": ("title",)}
