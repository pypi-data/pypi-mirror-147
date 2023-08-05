import os
import shutil
from glob import glob

Download_Folder: str = "C:/Users/verys/Downloads/*"
Destination_Folder: str = "C:/Users/verys/Downloads/TestDestination/"

Tax_Return_Check_String: str = "signal"
Client_Contact_Check_String: str = "Minecraft"

Ignore_Next_Tax_Return_Check: bool = False
Ignore_Next_Client_Contact_Check: bool = False

Files = glob(Download_Folder).sort(key=os.path.getctime)
print(f"Your download files: \n{Files}")
Files.reverse()
for file in Files:
  if Tax_Return_Check_String in file and not Ignore_Next_Tax_Return_Check:
    input(
        f"Moving this file: \n  {file}\n to folder \n  {Destination_Folder}\nClose this window to exit")
    shutil.move(file, Destination_Folder)
    Ignore_Next_Tax_Return_Check = True
  if Client_Contact_Check_String in file and not Ignore_Next_Client_Contact_Check:
    input(
        f"Moving this file: \n  {file}\n to folder \n  {Destination_Folder}\nClose this window to exit")
    shutil.move(file, Destination_Folder)
    Ignore_Next_Client_Contact_Check = True
