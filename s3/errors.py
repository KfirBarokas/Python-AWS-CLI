class S3Error(Exception):
    # Base class for EC2 related errors
    pass


class BucketAlreadyExists(S3Error):
    def __init__(self, bucket_name):
        super().__init__(f"Bucket already exists with the name: {bucket_name}")


class BucketDoesntHaveTags(S3Error):
    def __init__(self):
        super().__init__(f"Bucket doesnt have matching tags")


class BucketDoesntExist(S3Error):
    def __init__(self, bucket_name):
        super().__init__(f"There is no bucket with the name: {bucket_name}")


class InvalidBucketName(S3Error):
    def __init__(self, bucket_name):
        super().__init__(f"Bucket name is invalid: {bucket_name}")


class FileDoesntExist(S3Error):
    def __init__(self, file_name):
        super().__init__(f"There is no such file: {file_name}")


class ErrorUploadingFileToBucket(S3Error):
    def __init__(self):
        super().__init__(f"Error uploading file to bucket")
