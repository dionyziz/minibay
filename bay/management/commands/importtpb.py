from django.core.management.base import BaseCommand, CommandError
from bay.models import Torrent, File

from unidecode import unidecode

import traceback
import csv
from pprint import pformat
import codecs
import os
import progressbar


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

class Command(BaseCommand):
    args = '<data-directory>'
    help = 'Imports the specified torrent from a data directory'

    def scale(self, size, unit):
        return {
            'B': 1,
            'K': 1024,
            'M': 1024 * 1024,
            'G': 1024 * 1024 * 1024
        }[unit] * size

    def create_file(self, torrent_id, file_details):
        _, extension = os.path.splitext(file_details['Filename'])
        if extension == '.mp3':
            size = self.scale(file_details['Size'], file_details['Unit'])
            file = File(
                torrent_id=torrent_id,
                name=file_details['Filename'],
                extension=extension,
                size=self.scale(file_details['Size'], file_details['Unit']),
            )
            file.save()
            return True
            # self.stdout.write('Created file "%s"' % file_details['Filename'])
        return False

    def create_torrent(self, torrent_id, details, description):
        torrent = Torrent(
            id=torrent_id,
            description=description,
            title=details['Title'],
            seeders=details['Seeders'],
            leechers=details['Leechers'],
            uploaded=details['Uploaded'],
            uploader=details['By'],
            infohash=details['Info Hash']
        )
        torrent.save()
        return torrent

    def process_torrent_directory(self, torrent_directory):
        torrent_id = int(os.path.split(torrent_directory)[1])

        description_file_path = torrent_directory + '/description.txt'
        with codecs.open(description_file_path, 'r', 'utf-8-sig') as description_file:
            description = description_file.read()

        details_file_path = torrent_directory + '/details.csv'
        try:
            with open(details_file_path, 'r') as details_file:
                details_file.read(3)
                details_reader = csv.reader(details_file.readlines())
                column_names = details_reader.next()
                column_values = details_reader.next()
                details = dict(zip(column_names, column_values))
        except:
            print('Error when importing torrent details for torrent %i' % torrent_id)
            raise

        filelist_file_path = torrent_directory + '/filelist.csv'
        with open(filelist_file_path, 'r') as filelist_file:
            filelist_file.read(3) # skip BOM
            filelist_reader = csv.reader(filelist_file.readlines())
            column_names = filelist_reader.next()
            filelist = []
            for file_info in filelist_reader:
                filelist.append(dict(zip(column_names, file_info)))

        try:
            for idx, file_details in enumerate(filelist):
                filelist[idx]['Size'] = float(filelist[idx]['Size'])
        except:
            # print('Failed to process the size value for torrent %i. Probably an encoding issue.' % torrent_id)
            raise

        details['Seeders'] = int(details['Seeders'])
        details['Leechers'] = int(details['Leechers'])
        details['Type'] = int(details['Type'])

        title = details['Title']

        if details['Type'] != 101:
            # self.stdout.write('Skipping non-music torrent %i ("%s")' % (torrent_id, title))
            # self.stdout.write('.', ending='')
            pass
        else:
            torrent = self.create_torrent(torrent_id, details, description)
            files_count = 0
            for file in filelist:
                success = self.create_file(torrent_id, file)
                if success:
                    files_count += 1

            if files_count == 1:
                plural = ''
            else:
                plural = 's'

            if files_count:
                pass
                # self.stdout.write('\rImported torrent %i "%s" containing %i .mp3 file%s' % (torrent_id, title, files_count, plural))
            else:
                # self.stdout.write('\rSkipping torrent %i "%s" containing no .mp3 files' % (torrent_id, title))
                torrent.delete()

    def handle(self, *args, **options):
        torrent_data_dir = args[0]

        file_count = 0
        for (dirpath, dirnames, filenames) in os.walk(torrent_data_dir):
            if filenames:
                file_count += 1

        progress_count = 0
        pbar = progressbar.ProgressBar(
            widgets=['Importing: ', progressbar.Percentage(),
                     ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),
                     ' ', progressbar.ETA()],
            maxval=file_count
        ).start()
        for (dirpath, dirnames, filenames) in os.walk(torrent_data_dir):
            if filenames:
                try:
                    self.process_torrent_directory(dirpath)
                except:
                    pass
                    # print("Failed to import torrent %s. Callstack:" % dirpath)
                    # traceback.print_exc()
                    # print("Skipping torrent.")
                progress_count += 1
                pbar.update(progress_count)
        pbar.finish()
