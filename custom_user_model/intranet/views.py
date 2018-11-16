from django.views import generic
from .models import Borrowers, Biblio, Items, Genre

#List view of Borrowers
class BorrowerListView(generic.ListView):
    template_name = 'intranet/borrowerslist.html'

    def get_queryset(self):
        return Borrowers.objects.all()

#Detail view of Borrowers
class BorrowerDetailView(generic.DetailView):
    model = Borrowers
    template_name = 'intranet/borrowerdetail.html'



#List view of Books
class BooksListView(generic.ListView):
    template_name =  'intranet/bookslist.html'

    def get_queryset(self):
        return Biblio.objects.all()


#Detail view of Books
class BookDetailsView(generic.DetailView):
    model = Biblio
    template_name = 'intranet/bookdetails.html'


#List view of Items
class ItemsListView(generic.ListView):
    template_name = 'intranet/itemslist.html'

    def get_queryset(self):
        return Items.objects.all()

#Detail view of Items
class ItemDetailsView(generic.DetailView):
    model = Items
    template_name = 'intranet/itemdetails.html'


#List view of Genres
class GenreListView(generic.ListView):
    template_name =  'intranet/genrelist.html'

    def get_queryset(self):
        return Genre.objects.all()