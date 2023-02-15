import os
folder_name = "dodge"
directory_path = "C:/Users/Joakim/Documents/3an\Kandidatarbete/Egen programmering"
os.mkdir(os.path.join(directory_path, folder_name))
print(f"Created folder {folder_name} in directory {directory_path}")
