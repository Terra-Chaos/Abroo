from core.models import UserProfile
from asgiref.sync import sync_to_async

@sync_to_async
def get_or_create_user_profile(user):
    user_id = str(user.id)
    user_profile, created = UserProfile.objects.update_or_create(
        telegram_id=user_id,
        defaults={
            'telegram_username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language_code': user.language_code,
        }
    )
    return user_profile, created