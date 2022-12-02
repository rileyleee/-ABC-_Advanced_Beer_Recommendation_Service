from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from community.models import Column, Event, Board
from community.forms import ColumnForm, EventForm, BoardForm


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


@login_required
def column_edit(request, pk):
    column = Column.objects.get(pk=pk)

    if request.method == "POST":
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            # form.cleaned_data
            column = form.save()
            messages.success(request, "성공적으로 글이 수정되었습니다.")

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


@login_required
def event_edit(request, pk):
    event = Event.objects.get(pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            # form.cleaned_data
            event = form.save()
            messages.success(request, "성공적으로 글이 수정되었습니다.")

            return redirect(f"/community/event/{event.pk}/")
    else:
        form = EventForm(instance=event)

    return render(request, "community/event_edit.html", {
        "form": form,
    })


def board(request):
    board_qu = Board.objects.all().order_by('-pk')
    paginator = Paginator(board_qu, '20')
    page = request.GET.get('page', 1)
    pagenated_board_qu = paginator.get_page(page)
    context_eve = {'board_list': board_qu, 'pagenated_board_qu': pagenated_board_qu}

    return render(request, template_name="community/board.html", context=context_eve)


@login_required
def board_detail(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, "community/board_detail.html",
                  {
                      "boards": board,
                  })


@login_required
def board_new(request):
    if request.method == 'GET':
        form = BoardForm()
    else:
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = form.save()
            return redirect((f"/community/board/{board.pk}"))
    return render(request, "community/board_new.html", {
        "form": form
    })


def board_edit(request, pk):
    board = Board.objects.get(pk=pk)

    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            # form.cleaned_data
            board = form.save()
            messages.success(request, "successfully modified")

            return redirect(f"/community/board/{board.pk}/")
    else:
        form = BoardForm(instance=board)

    return render(request, "community/board_edit.html", {
        "form": form,
    })
