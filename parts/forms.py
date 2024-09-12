from django import forms

class PartsSearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)

class PartsFilterForm(forms.Form):
    make = forms.ModelChoiceField(queryset=Make.objects.all(), required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.all(), required=False)
    year = forms.ModelChoiceField(queryset=Year.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
