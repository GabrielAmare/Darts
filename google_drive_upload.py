from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def upload_file(zip_filename):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    gfile = drive.CreateFile({'parents': [{'id': '1imvHnVfcIYXUQhzWs9_6YvoRUgl0CVPG'}]})

    gfile.SetContentFile(zip_filename)
    gfile.Upload()

    print(f"\nSuccessfully uploaded {zip_filename} to google drive\n")

    for files in drive.ListFile():
        for file in files:
            if file["title"] == zip_filename:
                return file["webContentLink"]
    else:
        raise Exception("Process error")
