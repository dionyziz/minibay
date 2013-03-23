from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
import threading
import datetime
from bay.models import File
import os
import sys

def download(request, id):
    file = File.objects.get(pk=id)
    local_file_name = file.get_local_file_name()

    response = HttpResponse(mimetype='application/force-download')
    response['X-SENDFILE'] = local_file_name
    whitelist_filename = os.path.basename(local_file_name)
    whitelist_characters = [' ', '.', '-', '\'']
    whitelist_filename = ''.join(c for c in whitelist_filename if c in whitelist_characters or c.isalnum())
    sys.stderr.write(whitelist_filename + '\n')
    response['Content-Disposition'] = 'attachment; filename=%s' % whitelist_filename
    response['Content-type'] = 'audio/mpeg'
    response['Content-length'] = os.stat(local_file_name).st_size

    return response

def listen(request, file_id):
    file = File.objects.get(pk=file_id)
    torrent = file.torrent

    template = loader.get_template('song/play.html')

    file_available = file.available()

    try:
        eta = file.torrent.get_eta()
    except:
        eta = datetime.timedelta(minutes=5)

    context = Context({
        'song': file,
        'torrent': torrent,
        'file_id': file.id,
        'available': file_available,
        'eta': eta
    })

    def lazy_process():
        file.download()

    if not file.available():
        t = threading.Thread(target=lazy_process, args=[])
        t.setDaemon(False)
        t.start()

    return HttpResponse(template.render(context))

def search(request, text):
    file = File.search(text)

    return redirect('/bay/listen/%i' % file.id)

def index(request):
    return render(request, 'song/search.html')
