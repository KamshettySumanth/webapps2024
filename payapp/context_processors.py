from .models import Notification

def notifications_count(request):
    if request.user.is_authenticated:
        notifications_count=Notification.objects.filter(user=request.user,is_seen=False).count()
    else:
        notifications_count = 0
    return {"notif_count":notifications_count}