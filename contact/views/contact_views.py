from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    user = request.user

    if user.is_authenticated:
        contacts = Contact.objects.filter(show=True, owner=user).order_by('-id')# noqa
        paginator = Paginator(contacts, 10)
        page_numeber = request.GET.get("page")
        page_obj = paginator.get_page(page_numeber)

        context = {
            'user': user,
            'page_obj': page_obj,
            'site_title': 'Contatos - ',
            'is_authenticated': user.is_authenticated,
        }
        return render(
            request,
            'contact/index.html',
            context,
        )

    else:
        context = {
            'site_title': 'Contatos - ',
        }
        return render(
            request,
            'contact/index.html',
            context
        )


def search(request):
    search_value = request.GET.get('q', '').strip()
    user = request.user

    if search_value == "":
        return redirect('contact:index')

    contacts = Contact.objects\
        .filter(show=True, owner=user)\
        .filter(
           Q(first_name__icontains=search_value) |
           Q(last_name__icontains=search_value) |
           Q(phone__icontains=search_value) |
           Q(email__icontains=search_value)
        )\
        .order_by('-id')

    paginator = Paginator(contacts, 10)
    page_numeber = request.GET.get("page")
    page_obj = paginator.get_page(page_numeber)

    context = {
        'page_obj': page_obj,
        'site_title': 'Search - ',
        'search_value': search_value,
    }
    return render(
        request,
        'contact/index.html',
        context,
    )


# quando queremos pegar um único contato, usamos desta forma
def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    user = request.user
    single_contact = get_object_or_404(Contact.objects, pk=contact_id, show=True, owner=user) # noqa

    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': site_title,
    }
    return render(
        request,
        'contact/contact.html',
        context,
    )
