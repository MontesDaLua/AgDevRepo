#-*- coding: utf-8 -*-
import urlparse
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from pymogile import Client
from ogv_documents.storage.utils import get_valid_ascii_filename
from django.conf import settings

class MogilefsStorage(Storage):
    """
    simple mogilefs storage. It doesn NOT take care of serving the file.
    """
    def __init__(self, base_url=None, container=None, domain=None, trackers=None, client=None):
        """
        :param base_url: public facing url prefix. e.g "/my/private/docs/"
        :param container: prefix to use for the mogilefs storage. e.g "documents"
        :param domain: mogilefs domain to store stuff into. e.g "privatemedia"
        :param trackers: list of mogilefs trackers
        :return:

        with the above examples the file "my/file.pdf" will be handled like this:
        mogilefs:
            domain: privatemedia
            key: documents/my/file.pdf
        public url: /my/private/docs/my/file.pdf
        """
        self.base_url = base_url or settings.MEDIA_URL
        self.container = container or getattr(settings, 'MOGILEFS_MEDIA_CONTAINER', '')
        self.domain = domain or getattr(settings, 'MOGILEFS_DOMAIN', '')
        self.trackers = trackers or getattr(settings, 'MOGILEFS_TRACKERS', [])
        self.client = client or Client(domain=self.domain, trackers=self.trackers)

    def get_mogilefs_key(self, name):
        """
        converts a regular "file name" to a mogilefs key, using self.container as prefix.
        """
        name = name.replace('\\', '/')
        if self.container:
            return u"%s/%s" % (self.container, name)
        else:
            return u"%s" % (name)

    def get_mogilefs_locations(self, name):
        """
        returns a list of urls where the file can be accessed
        """
        return self.client.get_paths(self.get_mogilefs_key(name))

    def get_valid_name(self, name):
        """
        Returns a filename, based on the provided filename, that's suitable for
        use in the mogilefs storage system. Uses the django-filer get_valid_filename, which filters out
        umlauts.
        """
        return get_valid_ascii_filename(name)

    def exists(self, name):
        key = self.get_mogilefs_key(name)
        return len(self.client.get_paths(key)) > 0


    def url(self, name):
        """
        Returns an absolute URL where the file's contents can be accessed
        directly by a Web browser.
        """
        return urlparse.urljoin(self.base_url, name).replace('\\', '/')

    def size(self, name):
        """
        Returns the size of the file in bytes. This is very inefficient, since it has to load the whole file.
        Unfortunatly pymogile does not support returning the filesize on its own yet.
        """
        return self._open(name).size

    def _open(self, name, mode='rb'):
        """
        load the file contents from mogilefs and return it.
        """
        key = self.get_mogilefs_key(name)
        content = self.client.get_file_data(key)
        return ContentFile(content=content)

    def _save(self, name, content):
        key = self.get_mogilefs_key(name)
        content.seek(0)
        file_obj = self.client.new_file(key)
        file_obj.write(content.read())
        file_obj.close()
        return name

    def delete(self, name):
        return self.client.delete(self.get_mogilefs_key(name))
