#-*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage

class PrivateFileSystemStorage(FileSystemStorage):
    """
    File system storage that saves its files in the private directory.
    This directory should NOT be served directly by the web server.
    """
    is_secure = True

