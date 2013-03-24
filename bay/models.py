import os

from django.db import models
from django.conf import settings
import transmissionrpc


class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)
    count = models.IntegerField(default=0)

# TODO: Maintain a 'last_wanted' field per-torrent and per-file containing date of last use of a torrent/file
#       for cleanup purposes

class Torrent(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=1024)
    seeders = models.IntegerField(default=0)
    leechers = models.IntegerField(default=0)
    uploaded = models.DateTimeField('date uploaded')
    uploader = models.CharField(max_length=1024)
    infohash = models.CharField(max_length=2048)

    def get_transmission_connection(self):
        return transmissionrpc.Client(
            settings.TRANSMISSION['HOST'],
            port=settings.TRANSMISSION['PORT'],
            user=settings.TRANSMISSION['USER'],
            password=settings.TRANSMISSION['PASSWORD']
        )

    def get_transmission_torrent(self):
        tc = self.get_transmission_connection()
        torrents = tc.get_torrents()
        transmission_torrent_id = -1
        for torrent in torrents:
            if torrent.hashString.lower() == self.infohash.lower():
                return torrent
        raise TypeError

    def get_eta(self):
        tt = self.get_transmission_torrent()
        return tt.eta
        
    # TODO: split transmission-specific code to separate module
    # TODO: create a daemon that runs in python and cleans up / maintains files from torrents
    # TODO: Use cleaner exceptions
    def update_for_file_needs(self):
        tc = self.get_transmission_connection()
        # TODO: Reuse above code here
        torrents = tc.get_torrents()
        transmission_torrent_id = -1
        for torrent in torrents:
            if torrent.hashString.lower() == self.infohash.lower():
                transmission_torrent = torrent
                transmission_torrent_id = torrent.id
                transmission_metadata_percent = torrent.metadataPercentComplete
        # TODO: use exceptions instead of return values
        if transmission_torrent_id == -1:
            return False
        # TODO: Make this EPSILON
        if transmission_metadata_percent < 0.9999:
            return False
        db_files = File.objects.filter(torrent_id__exact=self.id)
        wanted = []
        unwanted = []
        transmission_files = transmission_torrent.files()
        if not transmission_files:
            return False
        for transmission_file_idx in transmission_files:
            found = False
            for db_file in db_files:
                transmission_file = transmission_files[transmission_file_idx]
                # print('Transmission side: ')
                # print(transmission_file['name'])
                # print('Db side: ')
                # print(db_file.name)
                file_name = db_file.name
                if file_name[0] != '/':
                    file_name = '/' + file_name
                if transmission_file['name'] == transmission_torrent.name + file_name:
                    if db_file.wanted:
                        wanted.append(transmission_file_idx)
                    else:
                        unwanted.append(transmission_file_idx)
                    found = True
                    break
            if not found:
                unwanted.append(transmission_file_idx)
        # print('Wanted: ')
        # print(wanted)
        # print('Unwanted: ')
        # print(unwanted)
        tc.change_torrent(transmission_torrent_id, files_wanted=wanted, files_unwanted=unwanted)
        return True

    def download(self):
        tc = self.get_transmission_connection()
        torrents = tc.get_torrents()
        torrent_exists = False
        for torrent in torrents:
            if torrent.hashString.lower() == self.infohash.lower():
                torrent_exists = True
        if not torrent_exists:
            tc.add_torrent(self.get_magnet(), download_dir=('%s/%i' % (settings.DOWNLOAD_DIR, self.id)))

        updated = False
        while not updated:
            updated = self.update_for_file_needs()
            
        return torrent_exists

    def get_download_dir(self):
        tc = self.get_transmission_connection()
        torrents = tc.get_torrents()
        for torrent in torrents:
            if torrent.hashString.lower() == self.infohash.lower():
                name = torrent.name
                if not name:
                    # torrent meta data not yet retrieved from DHT
                    raise TypeError
                return '%s/%i/%s' % (settings.DOWNLOAD_DIR, self.id, name)
        raise TypeError

    def get_magnet(self):
        return 'magnet:?xt=urn:btih:' + self.infohash

    magnet = property(get_magnet)
    
    def __unicode__(self):
        return self.title

class File(models.Model):
    torrent = models.ForeignKey(Torrent)
    name = models.CharField(max_length=1024)
    extension = models.CharField(max_length=8)
    size = models.IntegerField(default=0)
    wanted = models.BooleanField(default=False)

    @classmethod
    def search(cls, text):
        return File.objects.raw('SELECT '
                                '    f.id, f.name, '
                                '    t.title, t.seeders, t.infohash, '
                                '    MATCH (f.name) AGAINST (%s) '
                                '        AS score '
                                'FROM'
                                '    bay_file f '
                                '    CROSS JOIN '
                                '    bay_torrent t '
                                '        ON f.torrent_id = t.id '
                                'WHERE '
                                '    MATCH (f.name) AGAINST (%s) '
                                'ORDER BY '
                                '    score * pow(seeders, 0.2) DESC '
                                'LIMIT 1 ',
                                [text, text])[0]

    def get_local_file_name(self):
        file_name = self.name
        if file_name[0] != '/':
            file_name = '/' + file_name
        return self.torrent.get_download_dir() + file_name

    def available(self):
        try:
            # print(self.get_local_file_name())
            return os.path.exists(self.get_local_file_name())
        except:
            return False

    def download(self):
        self.wanted = True
        self.save()
        self.torrent.download()

    def __unicode__(self):
        return self.name
