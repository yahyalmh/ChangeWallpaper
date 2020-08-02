import hashlib
import os


class HashManager:

    def check_hash(self, pageList):
        for page in pageList:
            if os.path.exists(page.image_local_address):
                file_hash = self.md5(page.image_local_address)
                print(file_hash)
                # os.remove()
        return 0

    def md5(self, address):
        hash_md5 = hashlib.md5()
        with open(address, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
