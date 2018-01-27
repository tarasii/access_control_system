import os
from django.conf import settings
import requests
from zipfile import ZipFile

NEPATH = os.path.join(settings.BASE_DIR,"raw_data","ne")


class FileHelper():
    @classmethod
    def download(self, filename, url, force):
        filepath = os.path.join(NEPATH, filename)

        if not os.path.exists(NEPATH):
            os.makedirs(NEPATH)

        if not os.path.isfile(filepath) or force:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception('Sever response status was {}'.format(resp.status_code))

            with open(filepath, 'w') as temp_file:
                temp_file.writelines(resp.content)
                print filepath

    @classmethod
    def unzip(self, filename, dbffilename, force):
        filepath = os.path.join(NEPATH, filename)
        if not os.path.isfile(os.path.join(NEPATH, dbffilename)) or force:
            if os.path.isfile(filepath):
                with ZipFile(filepath, "r") as myzip:
                    if dbffilename in myzip.namelist():
                        myzip.extract(dbffilename, NEPATH)
                        print dbffilename


    @classmethod
    def procees(self, name, force):
        name_zip = "{}.zip".format(name)
        name_dbf = "{}.dbf".format(name)
        url = "http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/{}".format(name_zip)

        self.download(name_zip, url, force)
        self.unzip(name_zip, name_dbf, force)

        return name_dbf
