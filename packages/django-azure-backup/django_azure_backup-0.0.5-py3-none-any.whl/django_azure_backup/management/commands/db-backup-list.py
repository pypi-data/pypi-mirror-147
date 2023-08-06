from ...db.base import BackupSystem
import datetime
from django.core.management.base import BaseCommand
import argparse
import configparser


class Command(BaseCommand):

    def handle(self, **options):
        print('checking configuration')
        backup_service = BackupSystem()
        print('Backup file list: --\n')
        for backup_file in backup_service.get_list_of_blobs():
            print(backup_file.name)
