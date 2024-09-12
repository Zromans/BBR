from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Make, Model, Year, Category
from .forms import PartsSearchForm, PartsFilterForm

def parts_list(request):
    parts = Product.objects.all()
    search_form = PartsSearchForm(request.GET)
    filter_form = PartsFilterForm(request.GET)

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        parts = parts.filter(name__icontains=query)

    if filter_form.is_valid():
        make = filter_form.cleaned_data['make']
        model = filter_form.cleaned_data['model']
        year = filter_form.cleaned_data['year']
        category = filter_form.cleaned_data['category']

        if make:
            parts = parts.filter(make=make)
        if model:
            parts = parts.filter(model=model)
        if year:
            parts = parts.filter(year=year)
        if category:
            parts = parts.filter(category=category)

    context = {
        'parts': parts,
        'search_form': search_form,
        'filter_form': filter_form,
    }
    return render(request, 'parts/parts_list.html', context)

def parts_detail(request, pk):
    part = get_object_or_404(Product, pk=pk)
    context = {'part': part}
    return render(request, 'parts/parts_detail.html', context)

def parts_by_make(request, make_name):
    make = get_object_or_404(Make, name__iexact=make_name)
    parts = Product.objects.filter(make=make)
    context = {'make': make, 'parts': parts}
    return render(request, 'parts/parts_by_make.html', context)

def parts_by_model(request, model_name):
    model = get_object_or_404(Model, name__iexact=model_name)
    parts = Product.objects.filter(model=model)
    context = {'model': model, 'parts': parts}
    return render(request, 'parts/parts_by_model.html', context)

def parts_by_year(request, year):
    year_obj = get_object_or_404(Year, year=year)
    parts = Product.objects.filter(year=year_obj)
    context = {'year': year, 'parts': parts}
    return render(request, 'parts/parts_by_year.html', context)

def parts_by_category(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    parts = Product.objects.filter(category=category)
    context = {'category': category, 'parts': parts}
    return render(request, 'parts/parts_by_category.html', context)