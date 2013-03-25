import random
from django.shortcuts import render

from bay.models import File


def homepage(request):
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
