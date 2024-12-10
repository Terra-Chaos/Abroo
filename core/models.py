from django.db import models

class UserProfile(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    telegram_username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    language_code = models.CharField(max_length=8, null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.telegram_username}"