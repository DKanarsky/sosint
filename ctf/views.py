from django.shortcuts import render, redirect, get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.template.loader  import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from ctf.models import Flag, FlagChain, Submit
from ctf.services import is_captured, available_flags, save_submit
from ctf.forms import SubmitForm

@login_required
def flag_list(request, messages=[]):
    form = SubmitForm(request.POST or None)
    user = request.user
    msg = []
    data = []
    flag = None

    if request.method == "POST":
        if "flag_id" in request.POST:
            flag = get_object_or_404(Flag, pk=request.POST['flag_id'])
            form.fields['flag_id'].initial = flag.id
            if "answer" in request.POST:
                # if answer was submitted
                if form.is_valid():
                    submit_value = form.cleaned_data.get("answer")
                    error, msg = save_submit(user, flag, submit_value)
                    if not error and len(msg) == 0:
                        # success save submit and redirect (cause of post)
                        return redirect("/")
                else:
                    msg.append('Введите корректный ответ')
    flags = available_flags(user)
    captured = []
    for f in flags:
        captured.append(is_captured(f, user))
    data = list(zip(flags, captured))
    # return render(request, 'ctf/flag_cards.html', {'data': data, 'messages' : messages})

    return render(request, "ctf/flag_cards.html", {'flag': flag, 'data': data, 'form': form, 'msg' : msg})



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