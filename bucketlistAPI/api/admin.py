from django.contrib import admin
from api.models import BucketList, BucketListItem

# Register your models here.


class BucketListAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_modified', 'date_created']
    list_display_links = ['name']
    list_filter = ['date_created']
    search_fields = ['name']

    class Meta:
        model = BucketList


class BucketListItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'bucketlist', 'date_modified', 'date_created']
    list_display_links = ['item_name']
    list_filter = ['date_created', 'bucketlist']
    search_fields = ['item_name']

    class Meta:
        model = BucketListItem


admin.site.register(BucketList, BucketListAdmin)
admin.site.register(BucketListItem, BucketListItemAdmin)
