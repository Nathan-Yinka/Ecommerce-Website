from django.contrib import admin

from .models import Cart


# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        # Disable the ability to add new Cart instances
        return False

    def has_change_permission(self, request, obj=None):
        # Allow viewing but not editing existing Cart instances
        return True

    def has_delete_permission(self, request, obj=None):
        # Disable the ability to delete Cart instances
        return False
    list_display = ["user",'data',"type"]
