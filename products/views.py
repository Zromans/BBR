from django.shortcuts import render

def home(request):
    return render(request, 'products/home.html')

def start_scrape(request):
    if request.method == 'POST':
        try:
            scraped_data = scrape_products()
            csv_file = save_to_csv(scraped_data)
            with open(csv_file, 'rb') as file:
                response = HttpResponse(file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(csv_file)}"'
            os.remove(csv_file)  # Remove the temporary file
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
def get_models(request):
    make_id = request.GET.get('make')
    models = Model.objects.filter(make_id=make_id).order_by('name')
    return render(request, 'model_dropdown_list_options.html', {'models': models})