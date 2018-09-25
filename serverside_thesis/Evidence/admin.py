from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList
from django.forms.models import BaseInlineFormSet, BaseFormSet
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
import functools



from Evidence.models import Evidence


class EvidenceValidated(forms.ModelForm):

    """
        Evidence Validation
    """

    class Meta:
        model = Evidence
        fields = '__all__'

    def clean(self):
        """
            This function checks if the linked disease exists and it raises
                a validation error if it does.
        """
        ID = 0
        if self.cleaned_data['linked_disease'] != None:
            ID = self.cleaned_data['linked_disease'].id
            link_array = str(self.request).split("/")
            exists = ""
            # Checks if it's update or an add
            if link_array[4] == "add":
                exists = Evidence.objects.filter(
                    linked_disease__id=ID,archived=False)
            else:
                exists = Evidence.objects.filter(
                        linked_disease__id=ID,
                        archived=False).exclude(id=int(link_array[4]))

            if exists:
                string_error = "A linked {} already exists!".format(
                    exists[0].linked_disease.name)
                raise ValidationError({'linked_disease': [string_error]})


        if ID == 0:
            if self.cleaned_data['question'] == "":
                 raise ValidationError({'question': ["This field is \
                    required when the evidence is not linked to a disease."]})


class EvidenceAdmin(admin.ModelAdmin):

    
    # This class changes the GUI of the Evidence Administration
    
    
    form = EvidenceValidated
    list_display = ['name','question']
    list_filter = ('archived',)
    search_fields = ('name','question')

    def has_delete_permission(self, request, obj=None):
        # Disables the delete permission
        return False

    def get_form(self, request, *args, **kwargs):
        # Passes the request to the form so it can be used by the said form
        form = super(EvidenceAdmin, self).get_form(request, **kwargs)
        form.request = request
        return form

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
        return super(EvidenceAdmin,self).changelist_view(
                request, extra_context=extra_context)

admin.site.register(Evidence,EvidenceAdmin)