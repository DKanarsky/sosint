from django.shortcuts import render, redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required

from ctf.models import Flag
from ctf.services import (
    is_captured, available_flags, 
    save_submit
)
from ctf.forms import SubmitForm

@login_required
def flag_list(request):
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
    return render(
        request, 
        "ctf/flag_cards.html", 
        {
            'flag': flag, 
            'data': data, 
            'form': form, 
            'msg' : msg
        }
    )