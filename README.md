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
# users/models
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

    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
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
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
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

