from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .models import Bookmark
from .forms import BookmarkForm

# hame page
def bookmarking_site(request):
    return render(request,'index.html')

#signup
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


#login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            return redirect('page_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# logout
@login_required(login_url='/login/')
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    context = {
        'user': request.user
    }

    return render(request, 'logout.html', context)

#create
@login_required(login_url='/login/')
def bookmark_create(request):  
    if Bookmark.objects.filter(user=request.user).count() >= 5:
        return render(request, 'error.html', {'message': 'You can only add up to 5 bookmarks.'})
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            return redirect('page_list')
    else:
        form = BookmarkForm()
    return render(request, 'create.html', {'form': form})

from django.core.paginator import Paginator

#listing or retrieve
@login_required(login_url='/login/')
def listing(request):
    product_list = Bookmark.objects.filter(user=request.user)   #set .all() for list all data in table
    paginator = Paginator(product_list, 2)  # Set the number of items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {'page_obj': page_obj})

#update/edit
@login_required
def bookmark_update(request, pk):
    
    edit = Bookmark.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookmarkForm(request.POST,instance=edit)
        if form.is_valid():
            
              form.save()
              return redirect('home')
            
    else:
        form =BookmarkForm(instance=edit)           
    return render(request, 'update.html', {'form': form})
 

#delete
@login_required
def bookmark_delete(request,pk):
    bookmark=Bookmark.objects.get(pk=pk)  
    if request.method == 'POST':
        bookmark.delete()
        return redirect('page_list')
    
    return render(request,'delete.html',{'list':bookmark})

from django.http import JsonResponse
from django.db.models import Q
#search ajax
@login_required
def search_bookmarks(request):
    query = request.GET.get('q', '')
    results = Bookmark.objects.filter(user=request.user)
    if (query):
        results = results.filter(
            Q(title__icontains=query) | Q(url__icontains=query)
        ) 
    bookmarks = [{'title': bookmark.title, 'url': bookmark.url, 'date': bookmark.date,'time':bookmark.time}for bookmark in results ]
    return JsonResponse(bookmarks, safe=False)                            


