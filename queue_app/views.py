from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Ticket
from .forms import TakeTicketForm

def index(request):
    # Display a simple page with a button to take a ticket and a link to status
    latest_called = Ticket.objects.filter(status=Ticket.STATUS_CALLED).order_by('-called_at').first()
    pending_count = Ticket.objects.filter(day=timezone.localdate(), status=Ticket.STATUS_PENDING).count()
    return render(request, 'index.html', {
        'latest_called': latest_called,
        'pending_count': pending_count,
        'form': TakeTicketForm(),
    })

@require_POST
def take_ticket(request):
    form = TakeTicketForm(request.POST)
    if not form.is_valid():
        return redirect('index')
    number = Ticket.next_number_for_today()
    t = Ticket.objects.create(number=number)
    request.session['my_ticket_id'] = t.id
    return redirect('my_ticket')

def my_ticket(request):
    ticket_id = request.session.get('my_ticket_id')
    ticket = None
    if ticket_id:
        ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, 'my_ticket.html', {'ticket': ticket})

def status_view(request):
    today = timezone.localdate()
    pending = Ticket.objects.filter(day=today, status=Ticket.STATUS_PENDING).order_by('number')
    latest_called = Ticket.objects.filter(day=today, status=Ticket.STATUS_CALLED).order_by('-called_at').first()
    return render(request, 'status.html', {
        'pending': pending,
        'latest_called': latest_called,
    })

def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def admin_dashboard(request):
    today = timezone.localdate()
    pending = Ticket.objects.filter(day=today, status=Ticket.STATUS_PENDING).order_by('number')
    latest_called = Ticket.objects.filter(day=today, status=Ticket.STATUS_CALLED).order_by('-called_at').first()
    served_today = Ticket.objects.filter(day=today, status=Ticket.STATUS_SERVED).count()
    return render(request, 'admin/dashboard.html', {
        'pending': pending,
        'latest_called': latest_called,
        'served_today': served_today,
    })

@user_passes_test(is_staff)
@require_POST
def call_next(request):
    today = timezone.localdate()
    next_ticket = Ticket.objects.filter(day=today, status=Ticket.STATUS_PENDING).order_by('number').first()
    if next_ticket:
        next_ticket.status = Ticket.STATUS_CALLED
        next_ticket.called_at = timezone.now()
        next_ticket.save()
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
def mark_served(request, ticket_id):
    t = get_object_or_404(Ticket, id=ticket_id)
    t.status = Ticket.STATUS_SERVED
    t.served_at = timezone.now()
    t.save()
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
def skip_ticket(request, ticket_id):
    t = get_object_or_404(Ticket, id=ticket_id)
    t.status = Ticket.STATUS_SKIPPED
    t.save()
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
@require_POST
def reset_today(request):
    today = timezone.localdate()
    Ticket.objects.filter(day=today).delete()
    return redirect('admin_dashboard')
