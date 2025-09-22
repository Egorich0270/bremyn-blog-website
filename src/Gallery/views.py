import markdown
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import Card, AboutAuthor, ContactMessage, Tag
from django.utils.translation import get_language
from .forms import ContactForm


def page_not_found(request, exeption):
    return HttpResponseNotFound('Page_not_found')


def gallery_view(request):
    tag = request.GET.get('tag')
    cards = Card.objects.all()

    if tag:
        get_object_or_404(Tag, name=tag)
        cards = cards.filter(tags__name=tag)

    cards = cards.order_by('-created_at')
    paginator = Paginator(cards, 5)  # 5 карточек на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Gallery/gallery.html', {
        'cards': page_obj,
        'selected_tag': tag
    })



def about_view(request):
    latest = AboutAuthor.objects.order_by('-created_at').first()
    lang = get_language()

    if lang == 'ru':
        content = latest.content_ru
    else:
        content = latest.content_en

    html_content = markdown.markdown(content)
    return render(request, "Gallery/about.html", {
        "title": "Обо мне" if lang == 'ru' else "About me",
        "content": html_content,
        "date": latest.created_at
    })


def card_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, card.template_name + '/' + get_language() + '.html', {'card': card})

def cooperation_view(request):
    return render(request, "Gallery/cooperation.html")
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            message = form.cleaned_data["message"]
            feedback_contact = form.cleaned_data["feedback_contact"]

            if ContactMessage.objects.filter(feedback_contact=feedback_contact, message=message).exists():
                return render(request, "Gallery/success.html", {"name": name})

            ContactMessage.objects.create(name=name, message=message, feedback_contact=feedback_contact)

            return render(request, "Gallery/success.html", {"name": name})
    else:
        form = ContactForm()
    return render(request, "Gallery/contact.html", {"form": form})
