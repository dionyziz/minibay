import os
import sys

from django.shortcuts import render, redirect
from django.http import HttpResponse

from mobi.decorators import detect_mobile

from bay.models import File

@detect_mobile
def song_download(request, id):
    file = File.objects.get(pk=id)
    local_file_name = file.get_local_file_name()

    if request.mobile:
        response = HttpResponse(mimetype='audio/mpeg')
    else:
        response = HttpResponse(mimetype='application/force-download')
    response['X-SENDFILE'] = local_file_name
    whitelist_filename = os.path.basename(local_file_name)
    whitelist_characters = [' ', '.', '-', '\'']
    whitelist_filename = ''.join(c for c in whitelist_filename if c in whitelist_characters or c.isalnum())
    sys.stderr.write(whitelist_filename + '\n')
    if not request.mobile:
        response['Content-Disposition'] = 'attachment; filename=%s' % whitelist_filename
    response['Content-type'] = 'audio/mpeg'
    response['Content-length'] = os.stat(local_file_name).st_size

    return response
