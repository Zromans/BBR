from django import forms
from BBR.products.models import Year, Make, Model, Product

class ProductSearchForm(forms.Form):
    keyword = forms.CharField(
        label='Search Keyword',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter keyword'})
    )
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
    min_price = forms.DecimalField(
        label='Minimum Price',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter minimum price'})
    )
    max_price = forms.DecimalField(
        label='Maximum Price',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter maximum price'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make', 0))
                self.fields['model'].queryset = Model.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError("Minimum price cannot be greater than maximum price.")

        return cleaned_data

    def search_products(self):
        keyword = self.cleaned_data.get('keyword')
        year = self.cleaned_data.get('year')
        make = self.cleaned_data.get('make')
        model = self.cleaned_data.get('model')
        min_price = self.cleaned_data.get('min_price')
        max_price = self.cleaned_data.get('max_price')

        products = Product.objects.all()

        if keyword:
            products = products.filter(name__icontains=keyword)
        if year:
            products = products.filter(years=year)
        if make:
            products = products.filter(makes=make)
        if model:
            products = products.filter(models=model)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        return products

class ProductImportForm(forms.Form):
    file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file containing product data.'
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV.')
        return file
