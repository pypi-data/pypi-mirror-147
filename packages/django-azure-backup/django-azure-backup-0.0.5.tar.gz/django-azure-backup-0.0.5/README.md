# Django Database Backup

This package can take postgres dump and able to upload data in azure cloud storage.

## Build Process
open the link.
[click here for steps.](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)

## Required 
1. Django Default Database Config.
2. AZURE_ACCOUNT_NAME (Azure Storage Account Name).
3. AZURE_CREDENTIAL (Azure Key).
4. AZURE_CONTAINER (Azure Container Name).
5. AZURE_BACKUP_FOLDER_NAME.

## Commands
1. python3 manage.py db-backup-list
2. python3 manage.py db-backup
3. python3 manage.py db-restore
