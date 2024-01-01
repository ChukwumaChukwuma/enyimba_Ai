# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserQuery

admin.site.register(UserQuery)
