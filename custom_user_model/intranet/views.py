from django.views import generic
from .models import Borrowers, Biblio

def borrowers(request):
    table = BorrowersTable(data=Borrowers.objects.all(), template_name='django_tables2/bootstrap-responsive.html')
    #table.paginate(page=request.GET.get('page',1),per_page=1)
    #the above is when not using RequestConfig
    RequestConfig(request, paginate={'per_page':1}).configure(table)
    return render(request, 'intranet/borrowers.html', {'table': table})