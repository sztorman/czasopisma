from django.contrib import admin
from metadane.models import *

class czasAdmin(admin.ModelAdmin):
	list_display = ['tytul', 'data_wydania', 'miejsce_wydania', 'temat_i_slowa', 'kod_jezyka']
	list_filter = ['tytul', 'kod_jezyka']
	search_fields = ['tytul', 'data_wydania', 'miejsce_wydania', 'temat_i_slowa', 'kod_jezyka']

admin.site.register(Czasopismo, czasAdmin)
