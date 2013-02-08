#-*- coding: utf-8 -*-
import os
from django.template.defaultfilters import slugify
from django.utils.text import get_valid_filename

def get_valid_ascii_filename(s):
    '''
    like the regular get_valid_filename, but also slugifies away
    umlauts and stuff.
    '''
    s = get_valid_filename(s)
    filename, ext = os.path.splitext(s)
    filename = slugify(filename)
    ext = slugify(ext)
    if ext:
        return u"%s.%s" % (filename, ext)
    else:
        return u"%s" % (filename,)