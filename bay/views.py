import os
import sys
import random
import threading
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader

from bay.models import File


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

def listen(request, file_id, q):
    file = File.objects.get(pk=file_id)
    torrent = file.torrent

    template = loader.get_template('song/play.html')

    file_available = file.available()

    try:
        eta = file.torrent.get_eta()
        if eta is None:
            eta = datetime.timedelta(minutes=5)
    except:
        eta = datetime.timedelta(minutes=5)

    context = Context({
        'song': file,
        'torrent': torrent,
        'file_id': file.id,
        'available': file_available,
        'eta': eta,
        'q': q
    })

    def lazy_process():
        file.download()

    if not file.available():
        t = threading.Thread(target=lazy_process, args=[])
        t.setDaemon(False)
        t.start()

    return HttpResponse(template.render(context))

def search(request, q):
    file = File.search(q)

    return redirect('/bay/listen/%i/%s' % (file.id, q))

def index(request):
    backgrounds = [{
        'file': 'string_of_pearls.jpg',
        'author': u'Gilles Chiroleu'
    }, {
        'file': 'soprano_saxophone.jpg',
        'author': u'soupboy'
    }, {
        'file': 'piano.jpg',
        'author': u'Mourner'
    }, {
        'file': 'cello.jpg',
        'author': u'cellonaut'
    }, {
        'file': 'electric_guitar.jpg',
        'author': u'Feliciano Guimaraes'
    }, {
        'file': 'portuguese_guitar.jpg',
        'author': u'Feliciano Guimaraes'
    }, {
        'file': 'bass_guitar.jpg',
        'author': u'Feliciano Guimaraes'
    }, {
        'file': 'electric_guitar2.jpg',
        'author': u'a_roadbiker'
    }, {
        'file': 'broken_key.jpg',
        'author': u'janoma.cl'
    }, {
        'file': 'viola.jpg',
        'author': u'Mourner'
    }, {
        'file': 'piano2.jpg',
        'author': u'Robert Couse-Baker'
    }, {
        'file': 'score.jpg',
        'author': u'photosteve101'
    }, {
        'file': 'score2.jpg',
        'author': u'pfly'
    }, {
        'file': 'score3.jpg',
        'author': u'Brandon Giesbrecht'
    }, {
        'file': 'music.jpg',
        'author': u'Ferrari + caballos + fuerza = cerebro Humano'
    } ]

    background = random.choice(backgrounds)

    ctx = {
        'image': background
    }

    return render(request, 'song/search.html', ctx)
