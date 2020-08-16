from django.shortcuts import render, redirect, get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.template.loader  import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from ctf.models import Flag, FlagChain, Submit
from ctf.services import is_captured, available_flags

@login_required
def flag_list(request, messages=[]):
    user = request.user
    flags = available_flags(user)
    captured = []
    for flag in flags:
        captured.append(is_captured(flag, user))
    data = list(zip(flags, captured))
    return render(request, 'ctf/flag_list.html', {'data': data, 'messages' : messages})


@login_required
def submit(request, flag_id):
    flag = get_object_or_404(Flag, pk=flag_id)
    user = request.user
    error = False
    messages = []
    try:
        submit_value = request.POST.get('value', None)
        if submit_value is None or submit_value == '':
            messages.append("Вы не ввели вариант ответа")
            error = True
        if is_captured(flag, user):
            messages.append("Данный флаг уже захвачен")
            error = True
    except Exception:
        messages.append("Непредвиденная ошибка")
        error = True
    finally:
        if not error:
            submit = Submit(flag=flag, user=user, value=submit_value)
            submit.save()
            if not submit.captured and not error:
                messages.append("Ответ невереный")
        return flag_list(request, messages=messages)