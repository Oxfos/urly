import requests
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import ShortcodeForm
from .utils import make_unique_shortcode, url_exists, is_valid
from .models import Shortcode
from .serializers import ShortcodeSerializer, ShortcodeStatsSerializer


def homepage(request):
    """View for '/', i.e. homepage.""" 
    form = ShortcodeForm()
    return render(request, 'urly/index.html', {'form':form})


def make_shortcode(request):
    """View to shorten url."""
    form = ShortcodeForm(data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        shortcode = cd['shortcode']
        entry = form.save(commit=False)
        if url_exists(cd['url']) != True:
            response = HttpResponse('Url not present.<br><a href="/">Try again</a>.')
            response.status_code = 400
            response.reason_phrase = 'Url not present'
            return response
        elif not is_valid(shortcode):
            response = HttpResponse('The provided shortcode is invalid.<br>\
                    <a href="/">Try again</a>.')
            response.status_code = 412
            response.reason_phrase = 'The provided shortcode is invalid'
            return response
        shortcodes = [getattr(c, 'shortcode') for c in Shortcode.objects.all()]
        if shortcode in shortcodes:
            response = HttpResponse('Shortcode already in use.<br>\
                <a href="/">Try again</a>.')
            response.status_code = 409
            response.reason_phrase = 'Shortcode already in use'
            return response
        elif shortcode == '':
            entry.shortcode = make_unique_shortcode(6, shortcodes)
        entry.redirectCount = 0
        entry.save()
        serializer = ShortcodeSerializer(entry, many=False)
        return JsonResponse(serializer.data, status=201)
    return render(request, 'urly/index.html', {'form':form})


def check_shortcode(request, shortcode):
    """View to check whether shortcode is already in db."""
    try:
        shortcode = Shortcode.objects.get(shortcode=shortcode)
    except:
        response = HttpResponse('Shortcode not found.<br><a href="/">Try again</a>.')
        response.status_code = 404
        response.reason_phrase = 'Shortcode not found'
        return response
    else:
        response = HttpResponseRedirect(shortcode.url)
        response.status_code = 302
        response['Location'] = shortcode.url
        shortcode.lastRedirect = timezone.now()
        shortcode.redirectCount = shortcode.redirectCount + 1
        shortcode.save()
        return response
        

def get_stats(request, shortcode):
    """View to get shortcode statistics."""
    try:
        shortcode = Shortcode.objects.get(shortcode=shortcode)
    except:
        response = HttpResponse('Shortcode not found.<br><a href="/">Try again</a>.')
        response.status_code = 404
        response.reason_phrase = 'Shortcode not found'
        return response
    else:
        serializer = ShortcodeStatsSerializer(shortcode, many=False)
        return JsonResponse(serializer.data, status=200)

