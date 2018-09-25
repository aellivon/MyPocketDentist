from django.contrib import admin
from django.http import HttpResponseRedirect

from Disease.models import Disease


class DiseaseAdmin(admin.ModelAdmin):
    """
        This class changes the GUI of the Disease Administration
    """
    
    model = Disease
    list_display = ['name','details','advise']
    list_filter = ('archived',)
    search_fields = ('name','advise')
    
    def has_delete_permission(self, request, obj=None):
        """
            This function disables the 'delete' in the Disease GUI
        """
        return False

    def changelist_view(self, request, extra_context=None):
        """
            This function lets the adminstaration starts with the
                archived = False
        """
        try:
            if not request.META['QUERY_STRING'] and \
                not request.META.get('HTTP_REFERER', '').startswith(
                    request.build_absolute_uri()):
                return HttpResponseRedirect(request.path + "?archived__exact=0")
        except: pass # In case there is no referer
        return super(DiseaseAdmin,self).changelist_view(
                request, extra_context=extra_context)
    

admin.site.register(Disease,DiseaseAdmin)
admin.site.disable_action('delete_selected')

