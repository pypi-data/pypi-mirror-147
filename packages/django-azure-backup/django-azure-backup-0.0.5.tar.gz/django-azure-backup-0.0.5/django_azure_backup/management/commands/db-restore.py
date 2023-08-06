import os
from ...db.base import BackupSystem
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-n', "--name", type=ascii, help='blob file name dont add backup folder name')

    def handle(self, **options):
        filename = options['name'][1:-1]
        print(filename)
        print('checking configuration')
        backup_service = BackupSystem()
        print('downloading backup file')
        obj_file = backup_service.download_blob_file(name=filename)
        with open('/tmp/' + filename, 'wb') as file_writer:
            file_writer.write(obj_file)
        print('restoring')
        backup_service.restore_postgres_db(filepath='/tmp/'+filename)
        print('restoring completed')
        try:
            print('removing temp file')
            os.remove('/tmp/' + filename)
        except:
            print('unable to delete file')
        print('request completed')
