import random
from django.shortcuts import render

from bay.models import File


def homepage(request, q = '', error = '', suggestion = None):
    backgrounds = (
        ('string_of_pearls.jpg', 'Gilles Chirole'),
        ('soprano_saxophone.jpg', 'soupboy'),
        ('piano.jpg', 'Mourner'),
        ('cello.jpg', 'cellonaut'),
        ('electric_guitar.jpg', 'Feliciano Guimaraes'),
        ('portuguese_guitar.jpg', 'Feliciano Guimaraes'),
        ('bass_guitar.jpg', 'Feliciano Guimaraes'),
        ('electric_guitar2.jpg', 'a_roadbiker'),
        ('broken_key.jpg', 'janoma.cl'),
        ('viola.jpg', 'Mourner'),
        ('piano2.jpg', 'Robert Couse-Baker'),
        ('score.jpg', 'photosteve101'),
        ('score2.jpg', 'pfly'),
        ('score3.jpg', 'Brandon Giesbrecht'),
        ('music.jpg', 'Ferrari + caballos + fuerza = cerebro Humano')
    )

    background = random.choice(backgrounds)

    if not q:
        q = ''

    ctx = {
        'image': {
            'file': background[0],
            'author': background[1]
        },
        'q': q,
        'error': error,
        'suggestion': suggestion
    }

    return render(request, 'song/search.html', ctx)
