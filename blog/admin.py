from django.contrib import admin
from .models import Post, Comment, User, Address

admin.site.register( Post )
admin.site.register( Comment )
admin.site.register( User )
admin.site.register( Address )