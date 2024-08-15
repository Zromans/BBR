from django.shortcuts import render

def parts_list(request):
    return render(request, 'parts/parts_list.html')