from django.contrib import admin

from api.models import ExchangeRate, Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'symbol']
    search_fields = ['code', 'name']


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['source', 'target', 'rate']
    list_filter = ['source', 'target']
    list_display_links = ['source', 'target']

    # Readonly only if edit
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('source', 'target')
        return self.readonly_fields


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeAdmin)
