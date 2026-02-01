from django.db import models
from django.utils import timezone


class ClubInfo(models.Model):
    """Singleton model for club information"""
    title = models.CharField(max_length=200, default="HOUSKI Climbing Club")
    description = models.TextField(help_text="Main club description")
    history = models.TextField(blank=True, help_text="Club history and achievements")
    founded_year = models.IntegerField(default=2000)
    location = models.CharField(max_length=100, default="Pilsen, Czech Republic")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Club Information"
        verbose_name_plural = "Club Information"
    
    def save(self, *args, **kwargs):
        # Singleton pattern - only allow pk=1
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion of club info
        pass
    
    @classmethod
    def load(cls):
        """Load the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return self.title


class PictureOfWeek(models.Model):
    """Picture of the week displayed on homepage sidebar"""
    image = models.ImageField(upload_to='potw/', help_text="Upload picture of the week")
    caption = models.CharField(max_length=200)
    photographer = models.CharField(max_length=100, blank=True, help_text="Photographer name")
    date_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(
        default=True, 
        help_text="Only one picture can be active at a time"
    )
    
    class Meta:
        ordering = ['-date_added']
        verbose_name = "Picture of the Week"
        verbose_name_plural = "Pictures of the Week"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other pictures when this one is set as active
            PictureOfWeek.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.caption} - {self.date_added.date()}"
