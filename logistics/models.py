from typing import Iterable
from django.db import models
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from logistics.imports.choices import *
from django.utils.text import slugify
User = get_user_model()


class Shipment(models.Model):
    staff = models.ForeignKey(
        User, related_name='staff', on_delete=models.DO_NOTHING)
    updated_staff = models.ForeignKey(
        User, related_name='updated_staff', on_delete=models.DO_NOTHING)
    tracking_id = models.CharField(max_length=15, blank=True)
    slug = models.SlugField(max_length=260, blank=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    sender_name = models.CharField(verbose_name='Full name', max_length=30)
    sender_phone = models.CharField(max_length=14)
    city_of_origin = models.CharField(max_length=20)
    state_of_origin = models.CharField(
        max_length=15, choices=STATES)
    reciever_phone = models.CharField(max_length=14)
    reciever_address = models.CharField(verbose_name='Address', max_length=90)
    reciever_name = models.CharField(verbose_name='Full_name', max_length=30)
    status = models.CharField(
        max_length=15, choices=STATUS, default="packaging", blank=True)
    destination_city = models.CharField(max_length=20)
    destination_state = models.CharField(max_length=15, choices=STATES)
    transport_method = models.CharField(
        max_length=15, choices=TRANSPORT_METHOD)
    substance_type = models.CharField(
        max_length=15, choices=SUBSTANCE_TYPE)
    unit_of_measurement = models.CharField(
        max_length=15, choices=UNIT_OF_MEASUREMENT)
    units = models.DecimalField(max_digits=20, decimal_places=1)
    request_refund = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    desc = models.TextField()

    def save(self):
        self.slug = slugify(self.tracking_id)
        super().save()

    class Meta:
        ordering = ['-created_timestamp']

    def get_absolute_url(self):
        return reverse("logistics:update-shipment", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("logistics:update-shipment", kwargs={"slug": self.slug})

    def __str__(self):
        return self.sender_name
