from django.shortcuts import render
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.generic import ListView

from apps.callback.forms import CallbackForm
from apps.callback.models import Callback


def add_callback(request):

    form = CallbackForm(request.POST or None)

    status_code = 200

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Callback added, wait for the call')
            return JsonResponse({
                'message': 'Callback added, wait for the call'
            })
        else:
            status_code = 403

    return render(request, 'callback/add_callback.html', {
        'form': form,
        'status_code': status_code,
    }, status=status_code)

class CallbackListView(ListView):

    model = Callback
