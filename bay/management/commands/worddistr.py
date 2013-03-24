from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from bay.models import File, Word

import re
import progressbar


class Command(BaseCommand):
    args = ''
    help = 'Finds the distribution of words in files'

    def handle(self, *args, **options):
        cursor = connection.cursor()

        file_count = File.objects.all().count()
        pbar = progressbar.ProgressBar(
            widgets=['Finding words: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),
                     ' ', progressbar.ETA(), ' '],
            maxval=file_count
        ).start()
        BATCH_SIZE = 10000
        word_dict = {}
        for i in xrange(0, file_count, BATCH_SIZE):
            files = File.objects.all()[i:i + BATCH_SIZE]

            for file in files:
                for word in re.findall(r"[\w']+", file.name):
                    word = word.lower()
                    if not word in word_dict:
                        word_dict[word] = 0
                    word_dict[word] += 1

            if i % 1000 == 0:
                pbar.update(i)

        pbar.finish()

        pbar = progressbar.ProgressBar(
            widgets=['Inserting words: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),
                     ' ', progressbar.ETA(), ' '],
            maxval=len(word_dict)
        ).start()
        i = 0
        for word in word_dict:
            count = word_dict[word]
            cursor.execute('INSERT INTO bay_word (word, count) VALUES (%s, %s)', [word, count])
            pbar.update(i)
            i += 1

        pbar.finish()

        transaction.commit_unless_managed()
