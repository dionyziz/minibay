from django.shortcuts import redirect

from bay.models import File


def search(request, q):
    file = File.search(q)

    return redirect('/bay/listen/%i/%s' % (file.id, q))
