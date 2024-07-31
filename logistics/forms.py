from django import forms
from logistics.models import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from logistics.imports.choices import EMAIL_SUBJECTS


class TrackFrom(forms.Form):
    track_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Tracking ID'}))

    class Meta:
        fields = ["track_id"]

    def clean(self):
        track_id = self.cleaned_data.get("track_id")
        try:
            shipment = Shipment.objects.get(tracking_id=track_id)
            if shipment:
                pass

        except Shipment.DoesNotExist:
            raise forms.ValidationError('Incorrect tracking ID.')
            # return redirect(reverse('logistics:shipment-detail', {'shipment': shipment}))
        return track_id


class AddShipmentForm(forms.ModelForm):
    reciever_address = forms.CharField(max_length=90, widget=forms.TextInput(
        attrs={'placeholder': 'Receiver Address'}))
    sender_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Full name'}))
    sender_phone = forms.CharField(min_length=11, max_length=14, widget=forms.TextInput(
        attrs={'placeholder': ' Phone'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address'}))
    city_of_origin = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'City of Departure'}))

    reciever_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Full name'}))
    reciever_phone = forms.CharField(min_length=11, max_length=14, widget=forms.TextInput(
        attrs={'placeholder': 'Phone'}))
    destination_city = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'City of Destination'}))
    units = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Units'}))

    desc = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Additional details about this shipment...',
        'rows': 4,
    }))

    class Meta:
        model = Shipment
        fields = "__all__"
        exclude = ('staff', 'updated_staff', 'request_refund',
                   'created_timestamp', 'update_timestamp', 'status', 'slug', 'tracking_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['substance_type'].empty_label = 'Liquid/Solid'
        self.fields['unit_of_measurement'].empty_label = 'Kg / Lbs'
        self.fields['transport_method'].empty_label = 'Transport method'
        self.fields['state_of_origin'].empty_label = 'Choose State'
        self.fields['destination_state'].empty_label = 'Choose State'


class UpdateShipmentForm(forms.ModelForm):
    sender_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Fullname'}))
    sender_phone = forms.CharField(max_length=12, widget=forms.TextInput(
        attrs={'placeholder': ' Phone'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address'}))
    city_of_origin = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'City of Departure'}))

    reciever_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Fullname'}))
    reciever_phone = forms.CharField(max_length=12, widget=forms.TextInput(
        attrs={'placeholder': 'Phone'}))
    destination_city = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'City of Destination'}))
    units = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Units'}))

    desc = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Additional details about this shipment...',
        'rows': 4,
    }))

    class Meta:
        model = Shipment
        fields = "__all__"
        exclude = ('staff', 'updated_staff',
                   'request_refund', 'created_timestamp', 'update_timestamp', 'slug', 'tracking_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['substance_type'].empty_label = 'Liquid/Solid'
        self.fields['unit_of_measurement'].empty_label = 'Kg / Lbs'
        self.fields['transport_method'].empty_label = 'Transport method'
        self.fields['state_of_origin'].empty_label = 'Choose State'
        self.fields['destination_state'].empty_label = 'Choose State'


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Firstname"
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Lastname"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Your Email Address"
    }))
    subject = forms.ChoiceField(choices=EMAIL_SUBJECTS)
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Type in your message"
    }))
