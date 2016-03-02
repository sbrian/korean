#!/usr/bin/python

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

dictionary_file = drive.CreateFile({'id': '1-sz13m0O0YIeyhcqnqQxRuTpeL2G5fK1AOsLNgHRq1c'})
print 'title: %s, mimeType: %s' % (dictionary_file['title'], dictionary_file['mimeType'])
print dictionary_file.GetContentFile('dict.txt',mimetype='text/plain')


