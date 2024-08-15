from django.shortcuts import render, redirect
from .models import ScrapedData
from .utils import calculate_difference

def review_changes(request):
    unapproved_data = ScrapedData.objects.filter(approved=False).order_by('-timestamp')
    
    changes = []
    for data in unapproved_data:
        old_data = ScrapedData.objects.filter(url=data.url, approved=True).exclude(id=data.id).order_by('-timestamp').first()
        if old_data:
            differences = calculate_difference(old_data, data)
            changes.append({
                'new_data': data,
                'old_data': old_data,
                'differences': differences
            })
        else:
            changes.append({
                'new_data': data,
                'old_data': None,
                'differences': None
            })

    if request.method == 'POST':
        approved_ids = request.POST.getlist('approve')
        ScrapedData.objects.filter(id__in=approved_ids).update(approved=True)
        return redirect('review_changes')

    return render(request, 'scraping/review_changes.html', {'changes': changes})