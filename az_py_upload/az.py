import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from pathlib import Path


class Az:
    """"scans folder and uploads all files to unstaged in container"""

    def __init__(self, account_url="https://your_storage_account.blob.core.windows.net", container_name="your_storage_container"):
        # self.account_url = account_url
        # self.container_name = container_name
        default_credential = DefaultAzureCredential()
        service_client = BlobServiceClient(
            account_url, credential=default_credential)
        self.client = service_client.get_container_client(
            container_name)

    def list_files(self, local_path):
        return os.listdir(local_path)

    def upload(self, source, dest):
        '''
        Upload a file or directory to a path inside the container
        '''
        if (os.path.isdir(source)):
            self.upload_dir(source, dest)
        else:
            self.upload_file(source, dest)

    def upload_file(self, source, dest):
        '''
        Upload a single file to a path inside the container
        '''
        print(f'Uploading {source} to {dest}')
        with open(source, 'rb') as data:
            try:
                self.client.upload_blob(
                    name=dest, data=data)  # , overwrite=True
            except Exception as e:
                print(e)

    def upload_dir(self, source, dest):
        '''
        Upload the files of a directory to a path inside the storage container
        '''
        prefix = '' if dest == '' else dest + '/'
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = '' if dir_part == '.' else dir_part + '/'
                file_path = os.path.join(root, name)
                blob_path = prefix + name
                self.upload_file(file_path, blob_path)

    def ls_dirs(self, path, recursive=False):
        '''
        List directories under a path, optionally recursively
        '''
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        dirs = []
        for blob in blob_iter:
            relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
        if relative_dir and (recursive or not '/' in relative_dir) and not relative_dir in dirs:
            dirs.append(relative_dir)
        return dirs

    def ls_files(self, path, recursive=False):
        '''
        List files under a path, optionally recursively
        '''
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
        if recursive or not '/' in relative_path:
            files.append(relative_path)
        return files

    def ls_files_sorted(self, path):
        if not path == '' and not path.endswith('/'):
            path += '/'
        blob_iter = self.client.list_blobs(name_starts_with=path)
        sortedByCreation = sorted(
            blob_iter, key=lambda x: x.creation_time, reverse=True)
        files = []
        for blob in sortedByCreation:
            files.append(blob.name)
        return files

    def download_first_match(self, paths, search, dest):
        match = next(f for f in paths if search in f)
        # [START download_a_blob]
        DESTDIR = dest
        Path(DESTDIR).mkdir(parents=True, exist_ok=True)
        with open(DESTDIR + "/" + os.path.basename(match), "wb") as my_blob:
            download_stream = self.client.download_blob(match)
            my_blob.write(download_stream.readall())
        # [END download_a_blob]


def main():
    az = Az(account_url="https://your_storage_account.blob.core.windows.net",
            container_name="your_storage_container")
    az.upload_dir("./example_dir", "staging")


if __name__ == "__main__":
    main()
