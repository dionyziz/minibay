import random

from django.shortcuts import redirect
from django.http import HttpResponse

from bay.models import File
from bay.views.homepage import homepage


def search(request, q):
    try:
        file = File.search(q)
    except:
        suggestions = (
            ('529190', 'With A Little Help From My Friends', 'some Beatles'),
            ('87819', 'Rolling Stones - She\'s Like A Rainbow', 'some Rolling Stones'),
            ('1698659', 'Porcupine Tree - Arriving Somewhere', 'some Porcupine Tree'),
            ('61575', 'Massive Attack Paradise Circus', 'some Massive Attack'),
            ('1050486', 'Beatles - Hey Jude', 'some Beatles'),
            ('530043', 'Skyfall', 'the latest James Bond soundtrack'),
            ('621264', 'Life in Mono', 'Life in Mono'),
            ('1050854', 'Pink Floyd The Wall', 'The Wall'),
            ('523717', 'The Killers Human', 'some Killers'),
            ('2197334', 'The Doors People Are Strange', 'some Doors')
        )
        error = 'Could not find any song named "%s"' % q
        song = random.choice(suggestions)
        suggestion = {
            'id': song[0],
            'q': song[1],
            'text': song[2]
        }
        return homepage(request, q, error, suggestion)

    return redirect('/bay/listen/%i/%s' % (file.id, q))
