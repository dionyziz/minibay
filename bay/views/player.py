import datetime
import threading

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from mobi.decorators import detect_mobile

from mutagen.easyid3 import EasyID3
import discogs_client as discogs

from bay.models import File


@detect_mobile
def player(request, file_id, q):
    file = File.objects.get(pk=file_id)
    torrent = file.torrent

    file_available = file.available()

    if file_available:
        if request.mobile:
            return redirect('/bay/download/%i' % file.id)

        # TODO: split up meta-info lookup into model
        file_name = file.get_local_file_name()
        id3 = EasyID3(file_name)
        meta = {}
        meta['title'] = file.name
        meta['album'] = ''
        meta['artist'] = ''
        meta['thumb'] = ''
        try:
            meta['title'] = id3['title'][0]
        except:
            pass
        try:
            meta['artist'] = id3['artist'][0]
        except:
            pass
        try:
            meta['album'] = id3['album'][0]
        except:
            pass
        if len(meta['album']) and len(meta['artist']):
            discogs.user_agent = '%s/%s <%s>' % (settings.PROJECT['NAME'], settings.PROJECT['VERSION'], settings.ADMINS[0][1])
            s = discogs.Search(meta['artist'] + ' - ' + meta['album'])
            try:
                res = s.results()
                if len(res):
                    if isinstance(res[0], discogs.MasterRelease) or \
                       isinstance(res[0], discogs.Release):
                        images = res[0].data['images']
                        if len(images):
                            image = images[0]
                            meta['thumb'] = image['uri150']
            except:
                # not found
                pass

    else:
        meta = None

    try:
        eta = file.torrent.get_eta()
        if eta is None:
            eta = datetime.timedelta(minutes=5)
    except:
        eta = datetime.timedelta(minutes=5)

    context = {
        'song': file,
        'torrent': torrent,
        'file_id': file.id,
        'available': file_available,
        'eta': eta,
        'q': q,
        'meta': meta
    }

    def lazy_process():
        file.download()

    if not file.available():
        t = threading.Thread(target=lazy_process, args=[])
        t.setDaemon(False)
        t.start()

    return render(request, 'song/play.html', context)
