from django.contrib import admin
from .models import Book, CustomUser, CustomUserManager

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ['publication_year']
    search_fields = ('title', 'author')

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser)
admin.site.register(CustomUserManager)