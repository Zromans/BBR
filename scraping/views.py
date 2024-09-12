from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ScrapedData
from .utils import calculate_difference

def review_changes(request):
    unapproved_data = ScrapedData.objects.filter(approved=False).order_by('-timestamp')
    
    changes = []
    for data in unapproved_data:
        old_data = ScrapedData.objects.filter(url=data.url, approved=True).exclude(id=data.id).order_by('-timestamp').first()
        if old_data:
            differences = calculate_difference(old_data, data)
            if differences:
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
        rejected_ids = request.POST.getlist('reject')
        
        approved_data = ScrapedData.objects.filter(id__in=approved_ids)
        rejected_data = ScrapedData.objects.filter(id__in=rejected_ids)
        
        approved_data.update(approved=True)
        rejected_data.delete()
        
        if approved_data:
            messages.success(request, f"{approved_data.count()} changes approved.")
        if rejected_data:
            messages.warning(request, f"{rejected_data.count()} changes rejected.")
        
        return redirect('review_changes')
    
    context = {
        'changes': changes,
        'has_changes': bool(changes),
    }
    return render(request, 'scraping/review_changes.html', context)
