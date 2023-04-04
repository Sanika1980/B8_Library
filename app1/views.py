from django.shortcuts import render,redirect,HttpResponse
from .models import Book


# Create your views here.
def home(request):
    if request.method == "POST":
        bid = request.POST.get("book_id")
        name = request.POST.get("book_name")
        qty = request.POST.get("book_qty")
        price = request.POST.get("book_price")
        author = request.POST.get("book_author")
        is_published = request.POST.get("book_is_pub")
        if is_published == "Yes": 
            is_pub = True
        else:
            is_pub = False
        if not bid:
            Book.objects.create(name=name,qty=qty,price=price,author=author,is_published=is_pub)    
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()
        return redirect("home_page")
    elif request.method == 'GET':
        return render(request,"home.html")    

def show_active_books(request):
    return render(request,"show_books.html",{"books":Book.objects.filter(is_active=True),"active":True})               


def show_inactive_books(request):
    return render(request,"show_books.html",{"books":Book.objects.filter(is_active=False),"inactive":True})


def delete_book(request,id):
    Book.objects.get(id=id).delete()
    return redirect("all_active_books")

def soft_delete_book(request,id):
    book_obj = Book.objects.get(id=id)
    book_obj.is_active = False
    book_obj.save()    
    return redirect("all_active_books")

def restore_book(request,id):
   book_obj = Book.objects.get(id=id)
   book_obj.is_active = True
   book_obj.save()
   return redirect("all_active_books")

def update_book(request,id):
    book_obj = Book.objects.get(id=id) 
    return render(request,"home.html",{"single_book":book_obj})  


import csv
def create_csv_using_ORM(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-disposition'] = 'attachment;filename="test_csv"' 
    writer = csv.writer(response)
    writer.writerow(['name','qty','price','author','is_published','is_active'])
       
    books = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
    for book in books:
        writer.writerow(book) 
    return response   


def upload_csv(request):
    file = request.FILES["csv_file"]
    decoded_file = file.read().decode('utf-8').splitlines()
    expected_header_lst = ['name', 'qty', 'price', 'author', 'is_published','is_active']
    expected_header_lst.sort()
    actual_header_lst = decoded_file[0].split(",")
    actual_header_lst.sort()
    print(expected_header_lst,actual_header_lst)
    if expected_header_lst != actual_header_lst:
        return HttpResponse("Error....Headers are not equal....")

    reader = csv.DictReader(decoded_file) 
    
    lst = []
    for element in reader:
        book_name_lst = []
        all_books = Book.objects.all()
        for book in all_books:
            book_name_lst.append(book.name)
        name = element.get("name")    # name of book frm csv file
        if name in book_name_lst:
            return HttpResponse("This name has already given please choose some another book name")  
        else:
            is_pub = element.get("is_published")
            if is_pub == "TRUE":
               is_pub = True
            else:
               is_pub = False    
            lst.append(Book(name=element.get("name"),qty=element.get("qty"),price=element.get("price"),author=element.get("author"),is_published=is_pub))  
    
        
    Book.objects.bulk_create(lst)
    print(lst)
    return HttpResponse("success")            


  
    


import xlwt

def create_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="books.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws1 = wb.add_sheet('All Books')
    ws2 = wb.add_sheet('Active Books')
    ws3 = wb.add_sheet('Inactive Books')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name','qty','price','author','is_published','is_active' ]

    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], font_style)
        ws2.write(row_num, col_num, columns[col_num], font_style)
        ws3.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
    for row in rows:
        row_num += 1 
        for col_num in range(len(row)):
            ws1.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    rows = Book.objects.filter(is_active=True).values_list('name','qty','price','author','is_published','is_active')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws2.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    rows = Book.objects.filter(is_active=False).values_list('name','qty','price','author','is_published','is_active')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws3.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


import csv
from django.http import HttpResponse,FileResponse

def create_csv_using_raw(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    writer.writerow(['name','qty','price','author','is_published','is_active'])

    rows = Book.objects.raw('SELECT id,name, qty, price, author, is_published, is_active FROM my_project.book')
    for row in rows:
        writer.writerow([row.name, row.qty, row.price, row.author, row.is_published, row.is_active])

    return response


def show_text_file_contents(request):
        try:
            file =  open('D:\\Code_Files\\B8_django\\Library2\\Library2\\media\\textfile.txt', 'r') 
            contents = file.read()
            return render(request, 'text_file_contents.html', {'contents': contents})
        except FileNotFoundError as msg:
            return HttpResponse("File not Found")


def download_sample_csv(request):
        file_path = 'D:\Code_Files\B8_django\Library2\Library2\media\sample_csv_file.csv'
        try:
           f = open(file_path, 'rb') 
           response = FileResponse(f, content_type="application/vnd.ms-excel")
           response['Content-Disposition'] = 'attachment; filename="sample_csv_file.csv"'
           return response
        except FileNotFoundError as msg:
            return HttpResponse("File not found")

GET_ALL_STUDENTS_URL = "http://127.0.0.1:8000/api/get-all-students/"

import requests
def get_all_studs(request):
    response = requests.request("GET",GET_ALL_STUDENTS_URL)
    python_dict = response.json()
    return render(request,"student_data.html",{"data":python_dict})