import requests
import string, random
from .models import Shortcode


def get_shortcode(l):
    """Function to create random shortcode of length l."""
    alphanum = string.ascii_lowercase + string.digits + '_'
    code = ''
    for i in range(l):
        code = code + random.sample(alphanum, 1)[0]
    return code


def get_unique_shortcode(l):
    """Function to create unique get_shortcode."""
    shortcodes = Shortcode.objects.all()
    shortcode = get_shortcode(l)
    while shortcode in shortcodes:
        shortcode = get_shortcode(l)
    return shortcode


def is_not_unique(shortcode):
    """Test if shortcode is unique."""
    return Shortcode.objects.filter(shortcode=shortcode).exists()


def url_exists(url):
    """Function to test whether url exists."""
    try:
        response = requests.get(url)
    except:
        return False
    else:
        return False if response.status_code != 200 else True
