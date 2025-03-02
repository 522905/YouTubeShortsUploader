# import os
# import google_auth_httplib2
# import google_auth_oauthlib
# import googleapiclient.discovery
# import googleapiclient.errors
# import googleapiclient.http

# SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
# TOKEN_FILE = 'token.json'

# def authenticate_youtube():
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     # Remove old token file if exists (for re-authentication)
#     if os.path.exists(TOKEN_FILE):
#         os.remove(TOKEN_FILE)

#     # Load client secrets file, update with your file path if needed
#     client_secrets_file = r"C:\Users\om\DemoProject\client_secrets.json"

#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secrets_file, SCOPES)
    
#     # Force using fixed port 8080 to get a consistent redirect URI
#     credentials = flow.run_local_server(port=8080)

#     youtube = googleapiclient.discovery.build(
#         "youtube", "v3", credentials=credentials)

#     return youtube

# def upload_video(youtube):
#     request_body = {
#         "snippet": {
#             "categoryId": "22",
#             "title": "Uploaded from Python",
#             "description": "This is the most awesome description ever",
#             "tags": ["test", "python", "api"]
#         },
#         "status": {
#             "privacyStatus": "private"
#         }
#     }

#     # Updated path to the video file you want to upload
#     media_file = r"C:\Users\om\DemoProject\processed_videos\video.mp4"
#     print('Media File Exists : ', os.path.exists(media_file))

#     request = youtube.videos().insert(
#         part="snippet,status",
#         body=request_body,
#         media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
#     )

#     response = None

#     while response is None:
#         status, response = request.next_chunk()
#         if status:
#             print(f"Upload {int(status.progress() * 100)}%")

#     print(f"Video uploaded with ID: {response['id']}")

# if __name__ == "__main__":
#     youtube = authenticate_youtube()
#     upload_video(youtube)
