from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import *
from .models import *
from .mixins import *
from .utils import create_ref_code
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView


def trackShipment(request):
    if request.method == "GET":
        form = TrackFrom(request.GET)
        track_id = request.GET.get('track_id')
        shipment = None
        if track_id:
            try:
                shipment = Shipment.objects.get(tracking_id=track_id)
            except Shipment.DoesNotExist:
                pass
                # messages.error(request, "Incorrect tracking ID")

    context = {'shipment': shipment, 'form': form}
    return render(request, 'logistics/shipment-detail.html', context)


class IndexView(FormView):
    form_class = TrackFrom
    template_name = 'logistics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Louisgistics Xpress | Homepage'
        context['home_active'] = True
        return context


class AddShipment(LoginRequiredMixin, StaffUserMixin, CreateView):
    model = Shipment
    form_class = AddShipmentForm
    success_url = reverse_lazy('logistics:add-shipment')
    template_name = 'logistics/addshipment.html'

    def form_valid(self, form):
        sender_name = f"{form.cleaned_data.get('sender_name').title()}"
        reciever_name = f"{form.cleaned_data.get('reciever_name').title()}"

        form.instance.staff = self.request.user
        form.instance.updated_staff = self.request.user
        form.instance.tracking_id = create_ref_code()
        messages.success(
            self.request, f"{sender_name} shipment has been registered successfully")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Submit'
        context['add_shipment_active'] = True
        context['title'] = 'Add Shipment'
        return context


class UpdateShipment(LoginRequiredMixin, StaffUserMixin, UpdateView):
    model = Shipment
    form_class = UpdateShipmentForm
    template_name = 'logistics/addshipment.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', super().get_success_url())

    def form_valid(self, form):
        sender_name = f"{form.cleaned_data.get('sender_name').title()}"
        reciever_name = f"{form.cleaned_data.get('reciever_name').title()}"

        form.instance.updated_staff = self.request.user
        messages.success(
            self.request, f"{sender_name} shipment has been updated successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        shipment = self.get_object()
        context = super().get_context_data(**kwargs)
        context['shipment'] = shipment
        context['submit_btn'] = 'Update'
        context['add_shipment_active'] = True
        context['title'] = 'Update Shipment'
        return context


class AllShipments(LoginRequiredMixin, StaffUserMixin, ListView):
    paginate_by = 35
    context_object_name = 'shipments'
    template_name = 'logistics/shipments.html'
    queryset = Shipment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "All Shipments"
        context['empty_txt'] = "You've not registered any shipment."
        context['shipments_active'] = True
        context['all_shipment_active'] = True
        context['txt_writeup'] = "All shipments registered by all staffs"
        return context


class UserShipments(LoginRequiredMixin, StaffUserMixin, ListView):
    paginate_by = 35
    context_object_name = 'shipments'
    template_name = 'logistics/shipments.html'

    def get_queryset(self):
        return Shipment.objects.filter(staff=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.request.user.first_name} | Shipments"
        context['empty_txt'] = "No shipment registered."
        context['user_shipment_active'] = True
        context['txt_writeup'] = "Here are some shipments you've registered"
        return context


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'logistics/contact.html'
    success_url = reverse_lazy('logistics:contact-us')

    def form_valid(self, form):
        messages.info(
            self.request, "Thanks for getting in touch with us, we receieved your message.")
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        full_name = f'{first_name} {last_name}'

        full_message = f"""
         Recieved message below from {full_name}, {email}
         ____________________________________
         {message}
        """
        send_mail(
            subject='Recieved contact us information',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Louisgistics | Contact Us'
        context["contact_active"] = True
        return context


@login_required
def deleteShipment(request, slug):
    shipment = get_object_or_404(Shipment, slug=slug)
    if request.user == shipment.staff:
        shipment.delete()
        messages.info(request, f'Shipment deleted')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('logistics:home')
