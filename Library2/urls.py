"""Library2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/',views.home,name="home_page"),
    path('books/',views.show_active_books,name="all_active_books"),
    path('inactive-books/',views.show_inactive_books,name="all_inactive_books"),
    path('update/<int:id>/',views.update_book,name="update_book"),
    path('delete/<int:id>/',views.delete_book,name="delete_book"),
    path('soft-delete/<int:id>/',views.soft_delete_book,name="soft_delete_book"),
    path('restore/<int:id>/',views.restore_book,name="restore_book"),
    path('create-csv-using-ORM/',views.create_csv_using_ORM,name="create_csv_using_ORM"),
    path('upload-csv/',views.upload_csv,name="upload_csv"),
    path('create-excel/',views.create_excel,name="create_excel"),
    path('create-csv-using-raw/',views.create_csv_using_raw,name="create_csv_using_raw"),
    path('text-file-contents/',views.show_text_file_contents),
    path('download-sample-csv-file/',views.download_sample_csv,name="download_csv"),
    path('get-all-studs/',views.get_all_studs),
]


