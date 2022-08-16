from django.shortcuts import get_object_or_404

from crm.models import Message, House
from users.models import UserProfile


def new_users(request):
    count_apartments = None
    messagess = None
    houses = None
    if request.user.is_authenticated and 'crm' not in request.path:
        houses = House.objects.prefetch_related('sections').all()
        count_apartments = get_object_or_404(UserProfile,
                                             pk=request.user.id).apartment.select_related('owner').all()
    if request.user.is_authenticated and 'crm' not in request.path and count_apartments:
        messagess = Message.objects.select_related('sender', 'message_for_owner', 'house').all()
    return {'new_users': UserProfile.objects.filter(status='new'),
            'count_apartments': count_apartments,
            'messagess': messagess,
            'houses': houses}
