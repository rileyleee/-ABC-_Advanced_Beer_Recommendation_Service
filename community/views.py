from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from community.models import Column, Event
from community.forms import ColumnForm, EventForm


@login_required
def columns(request):
    column_qu = Column.objects.all().order_by('-pk')
    return render(
        request,
        'community/column.html',
        {
            'column_list': column_qu,
        })


@login_required
def column_detail(request, pk):
    column = get_object_or_404(Column, pk=pk)
    return render(request, "community/column_detail.html", {
        "columns": column,
    })


@login_required
def column_new(request):
    if request.method == "GET":
        form = ColumnForm()
    else:
        form = ColumnForm(request.POST, request.FILES)
        if form.is_valid():  # 폼이 유효하다면
            column = form.save()
            return redirect(f"/community/column/{column.pk}/")

    return render(request, "community/column_new.html", {
        "form": form,
    })


def column_edit(request, pk):
    column = Column.objects.get(pk=pk)

    if request.method == "POST":
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            # form.cleaned_data
            column = form.save()
            messages.success(request, "successfully modified")

            return redirect(f"/community/column/{column.pk}/")
    else:
        form = ColumnForm(instance=column)

    return render(request, "community/column_edit.html", {
        "form": form,
    })



@login_required
def events(request):
    event_qu = Event.objects.all().order_by('-pk')
    return render(request, "community/event.html",
                  {
                      'event_list': event_qu,
                  })


@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, "community/event_detail.html",
                  {
                      "events": event,
                  })


@login_required
def event_new(request):
    if request.method == 'GET':
        form = EventForm()
    else:
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()  # ModelForm에서 지원
            return redirect(f"/community/event/{event.pk}/")
    return render(request, "community/event_new.html",
                  {
                      "form": form
                  })
