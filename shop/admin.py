from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('preview', )
    list_display = ('name', 'price', 'price_type', 'preview')
    ordering = ('price',)

    def price_type(self, obj):
        return obj.price == Decimal('160000.00')

    def preview(self, obj):
        return '''
        <a href="{0}" target="_blank"><img src={0} width=20% /></a>
        '''.format(obj.cover)

    preview.allow_tags = True
