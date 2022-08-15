from django.shortcuts import get_object_or_404

from users.models import UserProfile


def new_users(request):
    count_apartments = None
    if request.user.is_authenticated:
        count_apartments = len(get_object_or_404(UserProfile,
                                                 pk=request.user.id).apartment.select_related('owner').all())
    return {'new_users': UserProfile.objects.filter(status='new'),
            'count_apartments': count_apartments}
