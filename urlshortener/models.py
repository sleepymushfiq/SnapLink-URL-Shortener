from django.db import models

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"