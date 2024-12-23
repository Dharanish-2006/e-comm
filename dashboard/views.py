from django.shortcuts import render
from django.http import JsonResponse
from .models import Dashboard, Widget

def dashboard_view(request):
    dashboard, _ = Dashboard.objects.get_or_create(user=request.user)
    widgets = Widget.objects.all()
    return render(request, 'dashboard.html', {'dashboard': dashboard, 'widgets': widgets})

def update_layout(request):
    if request.method == 'POST':
        layout = request.POST.get('layout')
        dashboard = Dashboard.objects.get(user=request.user)
        dashboard.layout = layout
        dashboard.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
