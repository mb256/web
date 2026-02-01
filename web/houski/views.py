from django.shortcuts import render
from .models import ClubInfo, PictureOfWeek


def home(request):
    """Homepage with club information and Picture of the Week"""
    club_info = ClubInfo.load()
    picture_of_week = PictureOfWeek.objects.filter(is_active=True).first()
    
    context = {
        'club_info': club_info,
        'picture_of_week': picture_of_week,
    }
    return render(request, 'houski/home.html', context)
