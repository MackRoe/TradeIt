from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect


from .models import Offer, Profile, Contact
from .forms import UserForm, ProfileForm, NewOfferForm, ContactForm

def index(request):
    return HttpResponse("This4That index page")


def profile_page(request):
    model = Profile
    user = User.objects.get(pk=1)
    profile = Profile.objects.get(user=user)
    profile_context = {
        "profile": profile
    }

    return render(request, 'tradeit/profile.html', profile_context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/this4that/profile_page')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'tradeit/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class OfferList(ListView):
    model = Offer

    def get(self, request):
        offer_context = {
            "offers": Offer.objects.all()
        }
        return render(request, 'this4that/offerlist.html', offer_context)
        pass


class OfferDetail(DetailView):
    model = Offer

    def get(self, request, slug):
        """ Returns a specific of wiki page by slug. """
        page = Offer.objects.get(slug=slug)
        context = {
            "page": page
        }
        return render(request, "tradeit/offerdetail.html", context)

    def post(self, request, slug):
        pass


class OfferListView(ListView):
    '''Create an includible sample of offers for display on
    main page'''
    model = Offer

    def get(self, request):
        offers = Offer.objects.all()
        offer_context = {
            "offers": offers
        }
        return render(request, "tradeit/offerlist.html", offer_context)


class OfferCreate(CreateView):
    template_name = 'newoffer.html'

    def get(self, request):
        form = NewOfferForm()
        print('get_method for new_offer')
        return render(request, 'tradeit/newoffer.html', {'form': form})

    def post(self, request):
        form = PageForm(request.POST)
        if form.is_valid():
            print('new offer post action made. Form is valid')
            newcard = form.save()
            return HttpResponseRedirect(reverse_lazy('tradeit/offer_detail/<slug>', args=[newcard.slug]))
        print('form not valid')
        return render(request, 'tradeit/newoffer.html', {'form': form})


class OfferUpdate(UpdateView):
    model = Offer
    fields = ['offer_title', 'offer_description', 'offer_maker', 'tokens_requested']
    success_url = reverse_lazy("offerlist")


class OfferDelete(DeleteView):
    model = Offer
    success_url = reverse_lazy("offerlist")


class ContactUser(CreateView):
    model = Contact
    # return render(request, 'contact.html', {
    #     'form': form_class,
    # })

    def get(self, request):
        form = ContactForm()

        return render(request, 'tradeit/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        pk = User.pk
        if form.is_valid():
            newcontact = form.save()
            messages.success(request, 'Your message was successfully saved!')
            return HttpResponseRedirect(reverse_lazy('contact', args=[newcontact.pk]))
        return render(request, 'tradeit/contact.html', {'form': form})


class MessageListView(ListView):
    model = Contact

    def get(self, request):
        message = Contact.objects.all()
        msg_context = {
            "message": message
            }
        return render(request, "tradeit/messagelist.html", msg_context)


class MessageDetailView(DetailView):
    model = Contact
    # pk = Contact.objects.get('_id')

    def get(self, request, pk):
        """ Returns a specific message """
        message = Contact.objects.get(pk)
        context = {
            "page": page
        }
        return render(request, "tradeit/messagedetail.html", message)
