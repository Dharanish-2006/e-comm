from django.shortcuts import render
from .models import Dashboard, Widget

def dashboard_view(request):
    dashboard, _ = Dashboard.objects.get_or_create(user=request.user)
    Widgets = Widget.objects.all()
    return render(request, 'dashboard.html', {'dashboard': dashboard, 'widgets': Widgets})