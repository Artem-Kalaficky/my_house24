from users.models import UserProfile


def new_users(request):
    return {'new_users': UserProfile.objects.filter(status='new')}
