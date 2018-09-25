from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList
from django.forms.models import BaseInlineFormSet, BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

from Rules.models import (
        Rule,
        RulesEvidence
    )


class RuleValidatedForm(forms.ModelForm):
    """
        Rule validation form
    """

    class Meta:
        model = Rule
        fields = '__all__'

    def clean(self):
        # Validating the Condition Order.

        Condition_Order = self.cleaned_data['Condition_Order']
        # Remove All Spaces that are more than one.
        Condition_Order = ' '.join(Condition_Order.split())

        # Preparing for condition order validation
        expected = ""

        # Elements that are allowed in the Condition Order
        allowed = [
                '(',')','a','n','d','o','r','1','2','3', \
                '4','5','6','7','8','9','0',' ']

        index = 0

        for character in Condition_Order:

            if expected == "":
                if character.lower() not in allowed:
                    raise ValidationError(
                        {'Condition_Order': ["Unexpected letter/symbol \
                         detected."]})
                
                # Makes sures that the word will be an "and" or an "or"
                if character.lower() == "a":
                    expected = "n"
                elif character.lower() == "o":
                    expected == "r"
                
            else:
                # Makes sures that the word will be an "and" or an "or"
                if character.lower() == "n" and expected == "n":
                    expected = "d"
                elif (character.lower() == "d" and expected == "d") or \
                        (character.lower() == "r" and expected == "r"):
                    expected = " "
                elif expected == " " and character == " ":
                    expected = ""
                else:
                    raise ValidationError({'Condition_Order': ["Unexpected \
                         word detected."]})
            index += 1
        Condition_Order = Condition_Order.lower()
        try:
            # Evaluates the condition order, if it's acceptable by the python
            if(Condition_Order != ""):
                eval(Condition_Order)
                self.cleaned_data['Condition_Order'] = Condition_Order
        except Exception as e:
            raise ValidationError({'Condition_Order': ["Something's wrong \
                 with your condition."]})


class BaseEvidenceAdminInlineSet(BaseInlineFormSet):
    """
        Inline Evidence Validation Form
    """

    def clean(self):
        repetition = []
        all_evidence_count = len(self.forms)
        delete_count = 0
        for form in self.forms:




            string_error = "Please fill up the disease and the evidence."
            try:
                FormId = form.cleaned_data['id'].id
            except:
                FormId = 0

            try:

                if not form.is_valid():
                    return #other errors exist, so don't bother

                # Ensures that the admin doesn't delete every evidence
                if form.cleaned_data['DELETE'] == True:
                    delete_count += 1
                if delete_count == all_evidence_count:
                    string_error = "You cannot delete all the evidence!"
                    raise forms.ValidationError(string_error)

                EvidenceID =  form.cleaned_data['evidence'].id

                # Ensures that a linked disease with an evidence has a 
                #   "base evidence"
                LinkedID = 0
                if form.cleaned_data['evidence'].linked_disease != None:
                    LinkedID =  form.cleaned_data['evidence'].linked_disease.id

                DiseaseID = form.cleaned_data['rule'].disease.id
                EvidenceName =  form.cleaned_data['evidence'].name
                DiseaseName = form.cleaned_data['rule'].disease.name

                # Ensures that the linked disease has a base evidence
                if LinkedID != 0:
                    BaseEvidence = ""
                    BaseEvidence = RulesEvidence.objects.filter(
                        rule__disease__id=LinkedID,
                        rule__archived=False).exclude(evidence__id=EvidenceID)
                    
                    if not BaseEvidence:
                        string_error = "The linked disease {} has no \
                            evidence. Please put an evidence on the \
                            disease.".format(EvidenceName)
                        raise forms.ValidationError(string_error)

                # If the evidence that the user's archives is the last base evidence, stop the user
                
                disease_is_linked = ""

                disease_is_linked = RulesEvidence.objects.filter(
                    rule__disease=DiseaseID,rule__archived=False)

                evidence_is_archived = RulesEvidence.objects.filter(
                    evidence__id=EvidenceID,rule__archived=True)


                if not evidence_is_archived:
                    if disease_is_linked != "":
                        if len(disease_is_linked) == 1:
                            if form.cleaned_data['rule'].archived == True:
                                string_error =mark_safe(
                                    "You cannot archive the last base evidence \
                                    of a linked disease that exists in a rule. \
                                    <br/> If you want to archive this rule, \
                                    archive the '{}' and '{}' combination first."\
                                    .format(disease_is_linked[0].rule.disease.name,\
                                        disease_is_linked[0].evidence.name))
                                raise forms.ValidationError(mark_safe(string_error))

                # Ensures that a linked disease is not an evidence to the same disease

                if DiseaseID == LinkedID:
                    string_error = "The evidence '{}'' is linked to '{}'." \
                        .format(EvidenceName,DiseaseName)
                    raise forms.ValidationError(label=mark_safe(string_error))


                # Ensures that Evidence ID is not repeated
                if EvidenceID in repetition:
                    raise forms.ValidationError("Repeating the same evidence \
                        twice in a rule is not allowed.")
                

                repetition.append(EvidenceID)

                exists = RulesEvidence.objects.filter(
                    evidence__id=EvidenceID,rule__disease__id=DiseaseID,
                    rule__archived=False).exclude(id=FormId)
                
                # Ensures that the combination disease and rule is unique
                if exists:
                    string_error = "The rule combination of {} and {} \
                        already exists!".format(DiseaseName,EvidenceName)
                    raise forms.ValidationError(string_error)

            except Exception as e:
                print "Error" + str(e)
                raise forms.ValidationError(string_error)

        if len(repetition) > 1:
            # Evaluates Condition Order     
            Numbers = ['1','2','3','4','5','6','7','8','9','0']
            Condition_Order = self.data['Condition_Order']
            index = 0
            Stacked_ID = []
            ID_To_Insert = ""

            for character in Condition_Order:
                if character in Numbers:
                    ID_To_Insert += character
                else:
                    if ID_To_Insert != "":
                        Stacked_ID.append(ID_To_Insert)
                    ID_To_Insert = ""

                index += 1
                # Evaluates the last element of the string
                if index == len(Condition_Order):
                    if ID_To_Insert != "":
                        Stacked_ID.append(ID_To_Insert)
                        ID_To_Insert = ""
                        

            # Checks if evidence number is in the condition order 
            for ID in Stacked_ID:
                if int(ID) not in repetition:
                    raise forms.ValidationError(
                        "The evidence number '" + ID + "' \
                        in the condition order is not detected!")

            for ID in repetition:
                if str(ID) not in Stacked_ID:
                    raise forms.ValidationError("Please include \
                        evidence number '" + str(ID) + "' in the \
                        condition order.")

            try:
                # Double Check Evaluation.
                if(Condition_Order == ""):
                    eval(Condition_Order)
            except Exception as e:
                raise forms.ValidationError("Please recheck the \
                    Condition Order")


class EvidenceAdmin(admin.TabularInline):
    model = RulesEvidence
    formset = BaseEvidenceAdminInlineSet
    min_num = 1
    extra = 0

class RuleAdmin(admin.ModelAdmin):
    # This class is for displaying the Admin GUI in Django Admin
    form = RuleValidatedForm
    list_display = ['disease','evidences','certainty_factor']
    list_filter = ('archived',)
    search_fields = ('disease__name','rules__evidence__name','certainty_factor')
    inlines = [EvidenceAdmin]

    # Gets all the related evidence and joins it into one string to display
    def evidences(self, obj):
        final_string = ""
        for k in obj.rules.all():
            to_join = str(k.evidence).split('-')
            final_string += to_join[1] + ' ,'

        final_string = final_string[:-2]
        return final_string

 

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
        return super(RuleAdmin,self).changelist_view(
                request, extra_context=extra_context)
 

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Rule,RuleAdmin)