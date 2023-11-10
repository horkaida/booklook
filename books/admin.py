from django.contrib import admin

import books.models

admin.site.register(books.models.Book)
admin.site.register(books.models.BookInUse)
admin.site.register(books.models.Genre)
admin.site.register(books.models.Status)
admin.site.register(books.models.ReadingSession)
admin.site.register(books.models.Rate)
admin.site.register(books.models.Feedback)





