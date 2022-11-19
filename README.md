# airbnb clone by nomadcoders lecture

## setup

- [python3.11 on deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)
- [pipenv](https://pipenv.pypa.io/en/latest/)

### pipenv graph

Django==4.1.3

- asgiref [required: >=3.5.2,<4, installed: 3.5.2]
- sqlparse [required: >=0.2.2, installed: 0.4.3]

## Lecture

### 1. SETUP

```shell
django-admin startproject config .
```

### 3. DJANGO BASICS

```shell
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

### 4. DJANGO APPS

#### 4.0 Models

```shell
python manage.py startapp houses
```

```python
# houses/models.py
class House(models.Model):
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
```

```python
# config/settings.py
INSTALLED_APPS = [
    "houses.apps.HousesConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = SYSTEM_APPS + CUSTUM_APPS
```

#### 4.1 Migrations

```shell
python manage.py makemigrations
python manage.py migrate
```

#### 4.3 Admin

```python
# houses/models.py
class House(models.Model):
    def __str__(self):
        return self.name
```

```python
# houses/admin.py
class HouseAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_night", "address", "pets_allowed")
    list_filter = ("price_per_night", "pets_allowed")
    search_fields = ("address",)
```

### 5. USERS APP

#### 5.1 Custom Model

```shell
python manage.py startapp users
```

```python
# users/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  pass
```

```python
# config/settings.py

CUSTUM_APPS = [
    "houses.apps.HousesConfig",
    "users.apps.UsersConfig",
]

AUTH_USER_MODEL = "users.User"
```

```python
# users/admin.py
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
```

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 5.2 Custom Fields

```python
# users/models.py
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
```

#### 5.4 Customo Admin

```python
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": ("username", "password", "name", "email", "is_host"),
                # "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    # fields = ("email", "password", "name")
    
    list_display = ("username", "email", "name", "is_host")
```

#### 5.5 Foreign Keys

```python
# houses/models.py
class House(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
```