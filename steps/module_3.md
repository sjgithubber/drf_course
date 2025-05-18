# Django Rest Framework (DRF) Course - Module 3
This is my DRF course. I hope you like it.

> These notes follow on from steps/module_2.md
***
***

## Current root directory
Your root directory should look like the following.
```
drf_course\  <--This is the root directory
    backend\
        core\
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >tests.py
            >views.py
        docker\
            ...
        drf_course\
            >__init__.py
            >asgi.py
            >settings.py
            >urls.py
            >wsgi.py
        static\
        >manage.py
        >requirements.txt
    steps\
        ...
    venv\
        include\
        Lib\
        Scripts\
    >.env
    >.gitignore
    >docker-compose.yml
    >env.template
    >README.md
    >server.py
```
If in doubt, run the following git commands:
```
git checkout module_3
git pull origin module_3
```

## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

In the last module, we constructed wired up two new applications and added the necessary code to fire up DRF's user interface. Let's expand on this and create our first API endpoint.

Nice and simple... We want a contact us endpoint so a user can send their name, email and message to our backend.

We need:
a) a model to capture store the incoming data
b) a router/url called '/contact/'
c) a serializer to process the data coming from the user and send a response back again.
d) a view to encapsulates the common REST HTTP method calls

easy, right?

1) Model - Go ahead and open /core/models.py and paste in the following code.
```

from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)

class Contact(
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
	Model
	):

	class Meta:
		verbose_name_plural = "Contacts"

	email = models.EmailField(verbose_name="Email")

	def __str__(self):
		return f'{self.title}'
```

2) Abstract models - You will notice that we are importing and using a few abstract models. Some are straight out of the box from django-extensions. However, I have my own that I like to use that uses a UUID instead of the default ID field. 
a) Go ahead and make a new directory in /backend called utils
b) Create a new file called model_abstracts.py and another called __init__.py
c) Paste the following code into /backend/utils/model_abstracts.py

```
import uuid
from django.db import models


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True
```

3) Serializer - Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.
Go ahead and:
a) Create a new file called serializers.py in /backend/core
b) Paste the following code into /backend/core/serializers.py

```
from . import models
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField



class ContactSerializer(serializers.ModelSerializer):

	name = CharField(source="title", required=True)
	message = CharField(source="description", required=True)
	email = EmailField(required=True)
	
	class Meta:
		model = models.Contact
		fields = (
			'name',
			'email',
			'message'
		)
```


4) ViewSets - A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as .get() or .post(), and instead provides actions such as .list() and .create().

Go ahead and paste the following code into /backend/core/views.py

```
from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ContactSerializer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from rest_framework.response import Response



class ContactViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for creating contact entires.
    """
    serializer_class = ContactSerializer

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

```

5) Routers & URLs - Some Web frameworks such as Rails provide functionality for automatically determining how the URLs for an application should be mapped to the logic that deals with handling incoming requests.

REST framework adds support for automatic URL routing to Django, and provides you with a simple, quick and consistent way of wiring your view logic to a set of URLs.

go ahead and replace the code in /drf_course/urls.py with the following code.

```
from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'contact', core_views.ContactViewSet, basename='contact') #new endpoint for '/contact/'

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]
```

6) Register - Go ahead and open /core/admin.py and paste in the follwing code to register the new models to the built in admin page. 

```
from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'email')
```

7) Migrations - Please use the following command to migrate the new model configuration.

```
python manage.py makemigrations
python manage.py migrate
```

You will now be able to see the fruits of your labour at [http://localhost:8000](http://localhost:8000).
>Note: We will fully test the endpoint in the next video


***
***

## Root directory
>Note: If all went well, your root directory should now look like this
```
drf_course\  <--This is the root directory
    backend\
        core\
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >serializers.py <--New file
            >tests.py
            >views.py
        docker\
            ...
        drf_course\
            >__init__.py
            >asgi.py
            >settings.py
            >urls.py
            >wsgi.py
        static\
        utils\ <--New directory
            >__init__.py
            >model_abstracts.py 
        >manage.py
        >requirements.txt
    steps\
        ...
    venv\
        include\
        Lib\
        Scripts\
    >.env
    >.gitignore
    >docker-compose.yml
    >env.template
    >README.md
    >server.py
```

***
***