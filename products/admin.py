from django.contrib import admin

from .models import Product, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'active', ]


@admin.register(Comment)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'body', 'stars', 'active', ]
