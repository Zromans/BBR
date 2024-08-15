from django import forms
from .models import Year, Make, Model

class ProductSearchForm(forms.Form):
    year = forms.ModelChoiceField(
        queryset=Year.objects.all().order_by('-year'),
        empty_label="Select Year",
        required=False
    )
    make = forms.ModelChoiceField(
        queryset=Make.objects.all().order_by('name'),
        empty_label="Select Make",
        required=False
    )
    model = forms.ModelChoiceField(
        queryset=Model.objects.none(),
        empty_label="Select Model",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = Model.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                pass