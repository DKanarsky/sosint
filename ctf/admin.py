from django.contrib import admin

from .models import Flag, FlagChain, Submit

class FlagChainInline(admin.StackedInline):
    model = FlagChain
    extra = 0
    fk_name = "child"


class FlagAdmin(admin.ModelAdmin):
    inlines = [FlagChainInline]
    list_display = ('title', 'score', 'enabled')
    list_filter = ['score', 'enabled']


class FlagCahinAdmin(admin.ModelAdmin):
    list_display = ('child', 'parent', 'enabled')
    list_filter = ['child', 'parent', 'enabled']


class SubmitAdmin(admin.ModelAdmin):
    list_display = ('user', 'flag', 'value', 'captured', 'dt')
    list_filter = ['user', 'flag', 'captured', 'dt']


# Register your models here.
admin.site.register(Flag, FlagAdmin)
admin.site.register(FlagChain, FlagCahinAdmin)
admin.site.register(Submit, SubmitAdmin)
