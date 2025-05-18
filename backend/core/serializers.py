# base of serializers, our code will use it in views.py most likely
# we create models for code to use


from . import models
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

class ContactSerializer(serializers.ModelSerializer):
    name = CharField(source='title', required=True)
    message = CharField(source='description', required=True)
    email = EmailField(required=True)

    class Meta:
        model = models.Contact
        fields = (
            'name',
            'email',
            'message'
        )