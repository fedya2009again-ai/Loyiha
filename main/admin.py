from django.contrib import admin
from .models import Category, Book, Comment
from django.utils.safestring import mark_safe

admin.site.register([Category])

admin.site.site_title = "Liberty"
admin.site.site_header = "Admin Panel"
admin.site.index_title = "Admin Sahifasi"
admin.site.login_template = "admin/login.html"

class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('text', 'user')
    extra = 0
    can_delete = False

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'get_introduction', 'created', 'category', 'published', 'get_image')
    list_display_links = ('title',)
    list_editable = ('published', 'category', 'price')
    list_filter = ('category', 'published')
    search_fields = ('title', 'introduction', 'category__name', 'price')
    inlines = [
        CommentInline
    ]

    fieldsets = [
        (
            "Asosiy",
            {
                'fields':['title', 'introduction']
            }
        ),
        (
            "Narxlari",
            {
                'fields': ['price']
            }
        ),
        (
            "Media",
            {
                'fields': ['image']
            }
        ),
        (
            "Tanlov",
            {
                'fields': ['category', 'published']
            }
        )
    ]

    def get_image(self, book):
        if book.image:
            return mark_safe(f'<img src="{book.image.url}" width="130px">')
        return "-"

    def get_introduction(self, book):
        if len(book.introduction) > 50:
            return book.introduction[:50] + "...."
        return book.introduction










