from django.shortcuts import render
import os
import subprocess
from django.http import HttpResponse


def backupAidsecure(request):
    print("backing up data...")
    process = subprocess.Popen(['python', 'manage.py', 'dbbackup', '--encrypt'])
    print("\n Successfully backed up the data.")

    return  render(request, 'backup_and_restore/backup.html')


def restoreAidsecure(request):
    print("restoring data...")
    process = subprocess.Popen(['python', 'manage.py', 'dbrestore', '--decrypt'])
    print("\n Successfully restored the data.")

    return  render(request, 'backup_and_restore/restore.html')


