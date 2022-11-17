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
  ...,
  "houses.apps.HousesConfig",
]
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
