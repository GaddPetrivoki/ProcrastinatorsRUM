from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader

from ZeitNehmer.direct.models import Message

# Create your views here.



@login_required
def inbox(request, directs=None):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = None
    direct = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        direct = Message.objects.filter(user=user, recipient=message['user'])
        direct.update(is_read=True)

        for message in messages:
            if message['user'].usernamer == active_direct:
                message['unread']=0

        context = {
            'directs': directs,
            'messages': messages,
            'active_direct': active_direct,
        }

    template = loader.get_template('Main_Page/templates/inbox.html')
    return HttpResponse(template.render(context, request))