#-*- coding: utf-8 -*-
from pymogile import Client
c = Client(domain="privatemedia", trackers=['127.0.0.1:7001'])
cpub = Client(domain="publicmedia", trackers=['127.0.0.1:7001'])

# list keys
c.list_keys()

# create a file in mogilefs
f = c.new_file('foobar.txt')
f.write('hi, my name bar, foo bar.')
f.close()

# show paths
c.get_paths('foobar.txt')
c.get_paths('404.txt')

# get file data
c.get_file_data('404.txt')
c.get_file_data('foobar.txt')

# remove
c.delete('foobar.txt')



# django storage backend

from ogv_documents.storage.mogilefs import MogilefsStorage
from django.core.files.base import ContentFile

s = MogilefsStorage(domain='privatemedia', container='documents', base_url='/documents/', trackers=['127.0.0.1:7001'])
s.exists('six/2011/justone.pdf')
s.save(u'epic.txt', ContentFile('my epic content. now with a content file'))
s.save(u'ëpîc.txt', u'my epic content with ümlauts.')

s.save(s.get_available_name(s.get_valid_name(u'ëpîc.txt')), 'my epic content with umlauts.')