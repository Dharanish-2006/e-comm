from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Dashboard, Widget

@login_required
def dashboard_view(request):
    dashboard, _ = Dashboard.objects.get_or_create(user=request.user)
    widgets = Widget.objects.all()
    return render(request, 'dashboard.html', {
        'dashboard': dashboard,
        'widgets': widgets
    })
