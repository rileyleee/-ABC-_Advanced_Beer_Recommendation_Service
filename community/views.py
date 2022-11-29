from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from community.models import Column, Event
from community.forms import ColumnForm, EventForm


@login_required
def columns(request):
    column_qu = Column.objects.all().order_by('-pk')
    paginator = Paginator(column_qu, '3')
    page = request.GET.get('page', 1)
    pagenated_column_qu = paginator.get_page(page)
    context_col = {'column_list': column_qu, 'pagenated_column_qu': pagenated_column_qu}
    return render(request, template_name='community/column.html', context=context_col)


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
            column = form.save(commit=False)
            column.author = request.user
            column.save()
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
    paginator = Paginator(event_qu, '3')
    page = request.GET.get('page', 1)
    pagenated_event_qu = paginator.get_page(page)
    context_eve = {'event_list': event_qu, 'pagenated_event_qu': pagenated_event_qu}

    return render(request, template_name="community/event.html", context=context_eve)


@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, "community/event_detail.html",
                  {
                      "events": event,
                  })


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
