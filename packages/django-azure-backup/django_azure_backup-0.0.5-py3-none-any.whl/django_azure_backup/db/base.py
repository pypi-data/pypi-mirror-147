import os
import subprocess
from django.conf import settings
from azure.storage.blob import BlockBlobService


class BackupSystem:

    def __init__(self):
        self.blob_service_client: BlockBlobService
        default_config = settings.DATABASES.get('default')
        self.postgres_host = default_config.get('HOST')
        self.postgres_port = default_config.get('PORT')
        self.postgres_db = default_config.get('NAME')
        self.postgres_user = default_config.get('USER')
        self.postgres_password = default_config.get('PASSWORD')
        self.azure_credential = settings.AZURE_CREDENTIAL
        self.azure_container = settings.AZURE_CONTAINER
        self.azure_account_name = settings.AZURE_ACCOUNT_NAME
        self.azure_backup_folder_name = settings.AZURE_BACKUP_FOLDER_NAME
        self.blob_service_client = BlockBlobService(account_name=self.azure_account_name,
                                                    account_key=self.azure_credential)

    def get_list_of_blobs(self):
        return self.blob_service_client.list_blobs(container_name=self.azure_container,
                                                   prefix=self.azure_backup_folder_name + '/')

    def download_blob_file(self, name):
        return self.blob_service_client.get_blob_to_bytes(container_name=self.azure_container,
                                                          blob_name=self.azure_backup_folder_name + "/" + name).content

    def upload_blob_file(self, name, data):
        self.blob_service_client.create_blob_from_bytes(container_name=self.azure_container,
                                                        blob_name=self.azure_backup_folder_name + "/" + name,
                                                        blob=data)

    def backup_postgres_db(self, verbose):
        """
        Backup postgres db to a file.
        """
        if verbose:
            try:
                process = subprocess.Popen(
                    ['pg_dump',
                     '-Fc',
                     '-v'],
                    shell=True,
                    env={
                        'PGUSER': self.postgres_user,
                        'PGPASSWORD': self.postgres_password,
                        'PGDATABASE': self.postgres_db,
                        'PGPORT': str(self.postgres_port),
                        'PGHOST': self.postgres_host
                    },
                    stdout=subprocess.PIPE
                )
                output = process.communicate()[0]
                if int(process.returncode) != 0:
                    print('Command failed. Return code : {}'.format(process.returncode))
                    exit(1)
                return output
            except Exception as e:
                print(e)
                exit(1)
        else:
            print('{}:{}@{}:{}/{}'.format(self.postgres_user,
                                          self.postgres_password,
                                          self.postgres_host,
                                          self.postgres_port,
                                          self.postgres_db))
            try:
                process = subprocess.Popen(
                    ['pg_dump',
                     '-Fc 8'],
                    shell=True,
                    env={
                        'PGUSER': self.postgres_user,
                        'PGPASSWORD': self.postgres_password,
                        'PGDATABASE': self.postgres_db,
                        'PGPORT': str(self.postgres_port),
                        'PGHOST': self.postgres_host
                    },
                    stdout=subprocess.PIPE
                )
                output = process.communicate()[0]
                if process.returncode != 0:
                    print('Command failed. Return code : {}'.format(process.returncode))
                    exit(1)
                return output
            except Exception as e:
                print(e)
                exit(1)

    def restore_postgres_db(self, filepath):
        """Restore postgres db from a file."""
        try:
            d = dict(os.environ)
            d['PGPASSFILE'] = filepath
            d['PGPASSWORD'] = self.postgres_password
            host = self.postgres_host

            process = subprocess.Popen(['psql',
                                        "-f%s" % filepath,
                                        "-d%s" % self.postgres_db,
                                        "-h%s" % host,
                                        "-U%s" % self.postgres_user
                                        ], env=d,
                                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
                                       )
            process.wait()
            if process.returncode != 0:
                print('Command failed. Return code : {}'.format(process.returncode))
                exit(1)
            return process.returncode
        except Exception as e:
            print("Issue with the db restore : {}".format(e))
