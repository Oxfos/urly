import requests
import string, random
from .models import Shortcode



alphanum = string.ascii_lowercase + string.digits + '_'


def make_shortcode(l):
    """Function to create random shortcode of length l."""
    return ''.join(random.sample(alphanum,l))


def make_unique_shortcode(l, set):
    """Function to create unique get_shortcode."""
    shortcode = make_shortcode(l)
    while shortcode in set:
        shortcode = make_shortcode(l)
    return shortcode


def url_exists(url):
    """Function to test whether url exists."""
    try:
        response = requests.get(url)
    except:
        return False
    else:
        return False if response.status_code != 200 else True


def is_valid(shortcode):
    """Function to test whether provided shortcode is valid."""
    return (shortcode == '' or (len(shortcode) == 6 and 0 not in [c in alphanum for c in shortcode]))

