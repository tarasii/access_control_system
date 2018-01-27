# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class RegistrationAdminInLine(admin.TabularInline):
    #list_display = ['datetime', 'card', 'group', 'action', 'direction']
    #list_filter = ('group',)
    model = Registration
    fields = ( 'datetime', 'card', 'group', 'image_tag', 'action', 'direction', )
    readonly_fields = ('datetime', 'card', 'group', 'image_tag', 'action', 'direction', )
    ordering = ('-datetime',)

class CardAdminInLine(admin.TabularInline):
    model = Card
    fields = ('label',)
    readonly_fields = ('label',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ["label", "max"]
    model = Group

    inlines = (CardAdminInLine, )

class CardAdmin(admin.ModelAdmin):
    list_display = ["label", "group"]
    list_filter = ('group',)
    model = Card

    inlines = (RegistrationAdminInLine, )

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'card', 'group', 'image_tag', 'action', 'direction']
    list_filter = ('group', 'card', 'action', 'direction',)
    model = Registration
    fields = ( 'datetime', 'card', 'group', 'image_tag', 'action', 'direction', )
    readonly_fields = ('datetime', 'card', 'group', 'image_tag', 'action', 'direction', )

# Register your models here.
admin.site.register(Group, GroupAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Device)
admin.site.register(Duration)
