import os
import sys

def user_interface():
    print(" -----------------------------------------------")
    print(" Select what to do with Aidsecure database.")
    print(" Choices: \n       1. Backup \n       2. Restore \n       3. Delete all data\n       4. Do nothing. Close the program\n")

    
    choice = str(input(" Please input choice number: "))
    
    if choice == "1":
        # backup
        print(" Backing up data...\n")
        os.system('sudo  "python manage.py dbbackup  -s hivIncidence"') # may add --clean --compress --encrypt
        print("\n Done backing up data. Data is stored in /data-backup/backups/ in this directory.")
        user_interface()
        
    elif choice == "2":
        # restore
        print(" Restoring data...\n")
        os.system('sudo "python manage.py dbrestore -s hivIncidence"') # may add --decrypt if dbbackup uses --encrypt
        print("\n Done restoring data...")
        user_interface()
    elif choice == "3" :
        # delete
        print(" Deleting all data saved in database...\n")
        os.system('cmd /c "python manage.py flush"')
        print("\n Done deleting all data saved in database...")
        user_interface()
    elif choice == "4":
        # exit
        print(" Program closed.")
        sys.exit()
    else:
        print("\n\n Your choice is invalid. Please choose again.")
        user_interface()
 

   
# def sample():
#     print("TEST")
# sample()

# call the function
user_interface()

