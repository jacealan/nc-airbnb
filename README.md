# airbnb clone by nomadcoders lecture
https://www.djangoproject.com/
https://www.django-rest-framework.org/

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

```python
# config/settings.py
LANGUAGE_CODE = 'ko-KR'
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

### 6. MODELS AND ADMIN

#### 6.0 User Model

```shell
pipenv install Pillow
```

```python
# users/models.py
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMAIL = ("femail", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "use", "Dollar"

    # ...

    avatar = models.ImageField(blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
```

```python
# users.admin.py
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                ),
                # "classes": ("wide",),
            },
        ),
        # ...
    )
```

#### 6.1 Room Model

#### 6.2 Many to Many

```shell
python manage.py startapp rooms
```

```python
# config/settings.py
CUSTUM_APPS = [
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
]
```

```python
# common/models.py
class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

```python
# rooms/models.py
from django.db import models
from common.models import CommonModel

class Room(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    country = models.CharField(max_length=50, default="??????")
    city = models.CharField(max_length=80, default="??????")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices,)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    amenities = models.ManyToManyField("rooms.Amenity")

class Amenity(CommonModel):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True)
```

```python
# rooms/admin.py
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass
```

#### 6.4 Rooms Admin

```python
# rooms/models.py
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
```

```python
# rooms/admin.py
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
```

#### 6.5 Experiences

```shell
python manage.py startapp experiences
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "experiences.apps.ExperiencesConfig",
]
```

```python
# experiences/models.py
from django.db import models
from common.models import CommonModel

class Experience(CommonModel):
    country = models.CharField(
        max_length=50,
        default="??????",
    )
    city = models.CharField(
        max_length=80,
        default="??????",
    )
    name = models.CharField(max_length=250)
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )


    def __str__(self) -> str:
        return self.name
```

```python
# experiences/admin.py
from django.contrib import admin
from .models import Experience, Perk

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "start",
        "end",
        "created_at",
    )

@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "details",
        "explanation",
    )
```

#### 6.6 Cetegories

```shell
python manage.py startapp categories
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "categories.apps.CategoriesConfig",
]
```

```python
# categories/models.py
from django.db import models
from common.models import CommonModel

class Category(CommonModel):
    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
```

```python
# experices/models.py
class Experience(CommonModel):
    # ...
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

# rooms/models.py
class Room(CommonModel):
    # ...
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
```

```python
# categories/admin.py
from django.contrib import admin
from .models import Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kind",
    )
    list_filter = ("kind",)
```

```python
# experices/admin.py
class ExperienceAdmin(admin.ModelAdmin):
    # ...
    list_filter = (
        "category",
    )
```

#### 6.7 Reviews

```shell
python manage.py startapp reviews
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "wishlists.apps.WishlistsConfig",
]
```

```python
# reviews/models.py
from django.db import models
from common.models import CommonModel

# Create your models here.
class Review(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f"{self.user} / {self.rating}"
```

```python
# reviews/admin.py
from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = ("rating",)
```

#### 6.8 Wishlists

```shell
python manage.py startapp wishlists
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "reviews.apps.ReviewsConfig",
]
```

```python
# wishlists/models.py
from django.db import models
from common.models import CommonModel

class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name
```

```python
# wishlists/admin.py
from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
```

#### 6.9 Bookings

```shell
python manage.py startapp bookings
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "bookings.apps.BookingsConfig",
]
```

```python
# bookings/models.py
from django.db import models
from common.models import CommonModel

class Booking(CommonModel):
    class BookingKindChoices(models.TextChoices):

        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f"{self.kind.title()} booking for: {self.user}"
```

```python
# bookings/admin.py
from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
    list_filter = ("kind",)
```

#### 6.10 medias

```shell
python manage.py startapp medias
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "medias.apps.MediasConfig",
]
```

```python
# medias/models.py
from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    file = models.ImageField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    def __str__(self) -> str:
        return "Photo File"
    
class Video(CommonModel):

    file = models.FileField()
    experience = models.OneToOneField(  
        "experiences.Experience",
        on_delete=models.CASCADE,
    )
    
    def __str__(self) -> str:
        return "Video File"
```

```python
# medias/admin.py
from django.contrib import admin
from .models import Photo, Video

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass
```


#### 6.11 Direct Messages

```shell
python manage.py startapp direct_messages
```

```python
# config/settings.py
CUSTUM_APPS = [
    # ...
    "direct_messages.apps.DirectMessagesConfig",
]
```

```python
# direct_messages/models.py
from django.db import models
from common.models import CommonModel

class ChattingRoom(CommonModel):
    """Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self) -> str:
        return "Chatting Room."


class Message(CommonModel):
    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
```

```python
# direct_messages/admin.py
from django.contrib import admin
from .models import ChattingRoom, Message
e.
@admin.register(ChattingRoom)
class ChattingRoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "room",
        "created_at",
    )
    list_filter = ("created_at",)

```

```python
# direct_messages/apps.py
from django.apps import AppConfig

class DirectMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "direct_messages"
    verbose_name = "Direct Messages"
```

### 7. ORM

#### 7.0 Introduction

```shell
$ python managy.py shell
Python 3.11.0 (main, Oct 24 2022, 19:56:13) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from rooms.models import Room
>>> Room.objects.all()
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.get(name="Beautiful House in ??????")
<Room: Beautiful House in ??????>
>>> room = Room.objects.get(name="Beautiful House in ??????")
>>> room.pk
1
>>> room.id
1
>>> room.name
'Beautiful House in ??????'
>>> room.owner
<User: jace>
>>> room.owner.email
'jace@g.com'
>>> room.price
1
>>> room.price = 20
>>> room.save()
>>> room.amenities.all()
<QuerySet [<Amenity: Shower>, <Amenity: Cooking basics>, <Amenity: Dishes and silverware>, <Amenity: Private entrance>]>
>>>
```

#### 7.1 filter, get, create, delete

```shell
>>> for room in Room.objects.all():
...     print(room.name)
...
Beautiful House in ??????
Apt. in ??????
>>> Room.objects.get(pk=1)
<Room: Beautiful House in ??????>
>>> Room.objects.get(pet_friendly=True)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/jace/.local/share/virtualenvs/nc-airbnb-pTv2yA_W/lib/python3.11/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jace/.local/share/virtualenvs/nc-airbnb-pTv2yA_W/lib/python3.11/site-packages/django/db/models/query.py", line 653, in get
    raise self.model.MultipleObjectsReturned(
rooms.models.Room.MultipleObjectsReturned: get() returned more than one Room -- it returned 2!
>>> Room.objects.filter(pet_friendly=True)
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.filter(pet_friendly=False)
<QuerySet []>
>>> Room.objects.get(pk=3)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/jace/.local/share/virtualenvs/nc-airbnb-pTv2yA_W/lib/python3.11/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jace/.local/share/virtualenvs/nc-airbnb-pTv2yA_W/lib/python3.11/site-packages/django/db/models/query.py", line 650, in get
    raise self.model.DoesNotExist(
rooms.models.Room.DoesNotExist: Room matching query does not exist.
>>> Room.objects.filter(price__gt=15)
<QuerySet [<Room: Beautiful House in ??????>]>
>>> Room.objects.filter(name__contains="??????")
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.filter(name__startswith="Apt")
<QuerySet [<Room: Apt. in ??????>]>
```

```shell
>>> from rooms.models import Amenity
>>> Amenity.objects.all()
<QuerySet [<Amenity: Shower>, <Amenity: Cooking basics>, <Amenity: Dishes and silverware>, <Amenity: Private entrance>]>
>>> Amenity.objects.create()
<Amenity: >
>>> Amenity.objects.create(name="Amenity from the console", description="How cool!")
<Amenity: Amenity from the console>
>>> to_delete = Amenity.objects.get(pk=6)
>>> to_delete
<Amenity: Amenity from the console>
>>> to_delete.delete()
(1, {'rooms.Amenity': 1})
```

#### 7.2 QuerySets

```shell
>>> Room.objects.all()
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.filter(pet_friendly=True)
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.filter(pet_friendly=True).exclude(price__lt=15).filter(name__contains="??????")
<QuerySet [<Room: Beautiful House in ??????>]>
>>> Room.objects.filter(pet_friendly=True, name__contains="??????", price__gt=15)
<QuerySet [<Room: Beautiful House in ??????>]>
>>> for room in Room.objects.all():
...     print(room.name)
...
Beautiful House in ??????
Apt. in ??????
>>> Room.objects.filter(pet_friendly=True).count()
2
```

#### 7.3 Admin Methods

```shell
>>> Room.objects.filter(created_at__year=2022)
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.filter(created_at__year=2021)
<QuerySet []>
>>> Room.objects.filter(price__lt=15).exists()
True
```

```python
# rooms/models.py
class Amenity(CommonModel):
    # ...
    class Meta:
        verbose_name_plural = "Amenities"
```

```python
# rooms/admin.py
class RoomAdmin(admin.ModelAdmin):
    # ...
    def total_amenities(self, room):
        return room.amenities.count()
```

#### 7.4 ForeignKey Filter

```shell
>>> room = Room.objects.get(pk=1)
>>> room
<Room: Beautiful House in ??????>
>>> room.price
20
>>> room.owner
<User: jace>
>>> room.owner.username
'jace'
>>> Room.objects.filter(owner__username="jace")
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
>>> Room.objects.filter(owner__username__startswith="ja")
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
```

#### 7.5 Reverse Accessors

```shell
>>> from users.models import User
>>> me = User.objects.get(pk=1)
>>> me
<User: jace>
>>> dir(me)
['CurrencyChoices', 'DoesNotExist', 'EMAIL_FIELD', 'GenderChoices', 'LanguageChoices', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 'avatar', 'booking_set', 'chattingroom_set', 'check', 'check_password', 'clean', 'clean_fields', 'currency', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'experience_set', 'first_name', 'from_db', 'full_clean', 'gender', 'get_all_permissions', 'get_constraints', 'get_currency_display', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_gender_display', 'get_group_permissions', 'get_language_display', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_host', 'is_staff', 'is_superuser', 'language', 'last_login', 'last_name', 'logentry_set', 'message_set', 'name', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'refresh_from_db', 'review_set', 'room_set', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_constraints', 'validate_unique', 'wishlist_set']
>>> me.room_set
<django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x7fbdb44d79d0>
>>> me.room_set.all()
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
```

#### 7.6 related_name

```python
# rooms/models.py
class Room(CommonModel):
    # ...
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )
```

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py shell
```

```shell
Python 3.11.0 (main, Oct 24 2022, 19:56:13) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from users.models import User
>>> me = User.objects.get(pk=1)
>>> me
<User: jace>
>>> me.rooms.all()
<QuerySet [<Room: Beautiful House in ??????>, <Room: Apt. in ??????>]>
```

### 8. POWER ADMIN

#### 8.1 Search Fields

```python
# rooms/models.py
class Room(CommonModel):
    # ...
    def rating(room):
        count = room.reviews.count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)
```

```python
# rooms/admin.py
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
        "updated_at",
    )
    
    search_fields: (str) = (
        "owner__username",
        "name",
        "^name",
        "=price",
    )
```

#### 8.2 Admin Actions

```python
# rooms/admin.py
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, queryset):
    print(model_admin)
    print(dir(request))
    print(queryset)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)
```

```python
# reviews/admin.py
class ReviewAdmin(admin.ModelAdmin):
    list_filter = (
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly"
    )
```

#### 8.3 Custum Filters
```python
# revies/admin.py
class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    
    parameter_name = "potato"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews

class ReviewAdmin(admin.ModelAdmin):
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
```

### 9. URLS AND VIEWS

#### 9.0 Views

```python
# config/urls.py
from django.contrib import admin
from django.urls import path
from rooms import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms", views.say_hello),
]
```

```python
# rooms/views.py
from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    return HttpResponse("hello")
```

#### 9.1 Include

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", include("rooms.urls")),
]
```

```python
# rooms/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.say_hello),
]
```

#### 9.2 URL Arguments

```python
# rooms/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_rooms),
    path("<int:room_id>", views.see_one_rooms),
]
```

```python
# rooms/views.py
from django.shortcuts import render
from django.http import HttpResponse

def see_all_rooms(request):
    return HttpResponse("see all rooms")

def see_one_rooms(request, room_id):
    return HttpResponse(f"see one with id: {room_id}")
```

#### 9.3 render

```python
# rooms/views.py
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this title from django",
        },
    )
```

```python
# rooms/templates/all_rooms.html
<h1>{{title}}</h1>
```

#### 9.4 Django Templates

```python
# rooms/templates/all_rooms.html
<h3>{{title}}</h3>

<ul>
    {% for room in rooms %}
        <li><a href="/rooms/{{room.pk}}">
            {{room.name}}<br />
            {% for amenity in room.amenities.all %}
                <span>-{{amenity.name}}</span>
            {% endfor %}
        </a></li>
    {% endfor %}
</ul>
```

#### 9.5 DoesNotExist

```python
# rooms/views.py
def see_one_rooms(request, room_pk):
    try:

        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
```

```python
# rooms/templates/room_detail.html
{% if not not_found %}
    <h1>{{room.name}}</h1>

    <h3>{{room.country}}/{{room.city}}</h3>
    <h4>{{room.price}}</h4>
    <p>{{room.description}}</p>
    <h5>{{room.category.name}}</h5>
{% else %}
    <h1>404 not found</h1>
{% endif %}
```

### 10. DJANGO REST FRAMEWORK

#### 10.0 Introduction

```shell
pipenv install djangorestframework
```

```python
# config/settings.py
THIRD_PARTY_APPS = [
    "rest_framework",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTUM_APPS
```

#### 10.1 JsonResponse

```python
# config/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", include("rooms.urls")),
    path("categories/", include("categories.urls")),
]
```

```python
# categories/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.categories)
]
```

```python
# categories/views.py
from django.http import JsonResponse
from .models import Category

def categories(request):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
        },
    )
```

#### 10.2 api_view

```python
# categories/views.py
from django.http import JsonResponse
from django.core import serializers
from .models import Category

def categories(request):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            "categories": serializers.serialize("json", all_categories),
        },
    )
```

```python
# categories/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category

# Create your views here.
@api_view()
def categories(request):
    return Response(
        {
            "ok": True,
        },
    )

```

#### 10.3 Serializer

```python
# categories/serializers.py
from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField()
```

```python
# categories/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

@api_view()
def categories(request):
    all_categories = Category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response(
        {
            "ok": True,
            "categories": serializer.data,
        },
    )
```

#### 10.4 POST Requests

```python
# categories/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.categories),
    path("<int:pk>", views.category),
]
```

```python
# categories/views.py
@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
```

```python
# categories/views.py
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        Category.objects.create(
            name=request.data["name"],
            kind=request.data["kind"],
        )
        return Response({"created": True})
```

#### 10.5 is_valid()

```python
# categories/serializers.py
from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.CharField(
        max_length=15,
    )
    created_at = serializers.DateTimeField(read_only=True)
```

```python
# categories/views.py
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)
```

#### 10.6 save()

```python
# categories/serializers.py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
```

```python
# categories/views.py
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            # name=validated_data["name"],
            # kind=validated_data["kind"],
            return Response(serializer.errors)  
```

#### 10.7 update()

```python
# categories/serializers.py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
    # ...
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
```

```python
# categories/views.py
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

# ...

@api_view(["GET", "PUT"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        try:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise NotFound
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
```

#### 10.8 DELETE

```python
# categories/views.py
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer

# ...

@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    # ...
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
```

```python
# config/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
]
```

#### 10.9 Recap
#### 10.10 APIView

```python
# categories/views.py
from rest_framework.views import APIView

class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)

class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
```

```python
# categories/urls.py
urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]
```

#### 10.11 ModelSerializer

```python
# categories/serializers.py
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
```

#### 10.12 ModelViewSet

```python
# categories/views.py
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
```

```python
# categories/urls.pyurlpatterns = [
    # path("", views.categories),
    # path("<int:pk>", views.category),
    # path("", views.Categorie.as_view()),
    # path("<int:pk>", views.CategoryDetail.as_view()),
    path(
        "",
        views.CategorieViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
```

#### 10.13 Conclusions