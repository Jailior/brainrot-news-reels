from backend.services.storage_service import StorageService

s3 = StorageService()
url = s3.upload_file("tmp/video.mp4", "debug/video.mp4", content_type="video/mp4")
print(url)

url = s3.download_file("debug/video.mp4", "tmp/s3FILE.mp4")
print("url 2:", url)