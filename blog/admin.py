from django.contrib import admin

import blog.models

admin.site.register(blog.models.BlogPost)
admin.site.register(blog.models.Tag)
