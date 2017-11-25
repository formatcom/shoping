from django.contrib import admin
from .models import Item

@admin.register(Item)
class  ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('preview', )
    list_display = ('name', 'price', 'preview')
    ordering = ('price',)

    def preview(self, obj):
        return '''
        <a href="{0}" target="_blank"><img src={0} width=20% /></a>
        '''.format(obj.cover)

    preview.allow_tags = True
