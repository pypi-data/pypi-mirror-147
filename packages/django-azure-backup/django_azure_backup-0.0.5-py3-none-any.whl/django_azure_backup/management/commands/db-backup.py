from ...db.base import BackupSystem
import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, **options):
        print('checking configuration')
        backup_service = BackupSystem()
        print('creating psql dump')
        datafile = backup_service.backup_postgres_db(True)
        file_name = str(datetime.datetime.now().strftime('%Y-%m-%d-%M-%S')) + \
                    "-" + backup_service.postgres_db + ".psql"
        print('uploading psql dump to azure container')
        backup_service.upload_blob_file(name=file_name, data=datafile)
        print('successfully uploaded file name: {}'.format(file_name))
