from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, queryset):
    print(model_admin)
    print(dir(request))
    print(queryset)


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)
    
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

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )

    search_fields: (str) = (
        "name",
        # "^name",
        "^price",
        "owner__username",
    )

    # def total_amenities(self, room):
    #     return room.amenities.count()


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
