from django.contrib import admin
from django.shortcuts import redirect, render
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Tag)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

    fieldsets = (
        ('Información del producto', {
            'fields': ('name', 'description', 'category', 'price', 'is_active', 'image', 'tag')
        }),
    )

    ordering = ('-created_at', )

    filter_horizontal = ('tag', )

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'Productos desactivados {queryset.count()}')
    make_inactive.short_description = "Marcar como inactivo"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Productos activados')
    make_active.short_description = "Marcar como activo"

    def set_price(self, request, queryset):
        if 'apply' in request.POST:
            price = request.POST.get('price')
            queryset.update(price=price)
            self.message_user(request, 'Precio actualizado')
            return redirect(request.get_full_path())
        return render(request, 'admin/set_price.html', context={'products': queryset})

    actions = [make_inactive, make_active, set_price]

class CartItemInLine(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_items', 'total_price')
    inlines = [CartItemInLine]