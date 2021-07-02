import sys
import os
import shutil
from google_drive_upload import upload_file

from distutils.core import setup
import py2exe
from darts.__meta__ import APP_NAME, VERSION
from send_email import send_email

sys.argv.append('py2exe')

ASSETS_PATH = "assets\\"


def images():
    root = os.path.abspath(ASSETS_PATH + "images")
    return [os.path.join(root, fn) for fn in os.listdir(root)]


def all_vocals():
    root = ASSETS_PATH + "messages"
    for dn in os.listdir(root):
        base = os.path.join(root, dn)
        yield base, [os.path.join(base, fn) for fn in os.listdir(base)]


def exes():
    root = os.path.abspath(ASSETS_PATH + "exes")
    return [os.path.join(root, fn) for fn in os.listdir(root)]


data_files = [
    (ASSETS_PATH + 'images', images()),
    *all_vocals(),
    (ASSETS_PATH + 'exes', exes())
]

# SET THE ENVIRONMENT TO PRODUCTION
with open("darts\\__meta__.py", mode="w", encoding="utf-8") as file:
    file.write(f"""APP_NAME = "{APP_NAME}"
VERSION = ({VERSION[0]}, {VERSION[1]}, {VERSION[2]})
ENV = "PROD"
""")

output_dirname = f"{APP_NAME}_v{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"

setup(
    windows=[APP_NAME + ".py"],
    data_files=data_files,
    options={
        "py2exe": {
            "unbuffered": True,
            "optimize": 2,
            "dist_dir": output_dirname,
            "compressed": True,
        }
    }
)

shutil.make_archive(output_dirname, 'zip', root_dir=os.curdir, base_dir=output_dirname)
zip_filename = output_dirname + ".zip"

# AUTO UPGRADE THE VERSION EACH TIME THE APPLICATION IS COMPILED
with open("darts\\__meta__.py", mode="w", encoding="utf-8") as file:
    file.write(f"""APP_NAME = "{APP_NAME}"
VERSION = ({VERSION[0]}, {VERSION[1]}, {VERSION[2] + 1})
ENV = "DEV"
""")

########################################################################################################################
# SAVE FILE ON DRIVE
########################################################################################################################
zip_url = upload_file(zip_filename)

########################################################################################################################
# SEND EMAIL
########################################################################################################################
send_email(zip_url, *VERSION)
