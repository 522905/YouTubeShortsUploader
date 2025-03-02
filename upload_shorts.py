import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = 'token.json'

def authenticate_youtube():
    import os
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    client_secrets_file = r"C:\Users\om\DemoProject\client_secrets.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES
    )
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def upload_short(youtube, media_file, title, description, tags):
    """
    Uploads a single video to YouTube with Shorts-friendly metadata.
    Assumes video is <60s and in a vertical 9:16 format.
    """
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    print(f"Uploading: {media_file}")
    if not os.path.exists(media_file):
        print("❌ File not found:", media_file)
        return None

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    video_id = response["id"]
    print(f"✅ Short uploaded with ID: {video_id}\n")
    return video_id

def upload_all_shorts(youtube, folder_path):
    """
    Loops through all .mp4 files in 'folder_path' and uploads each as a Short.
    """
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp4')]
    if not files:
        print("❌ No video files found in folder:", folder_path)
        return
    files.sort()  # e.g., "Part 1.mp4", "Part 2.mp4", etc.
    for index, file_name in enumerate(files, start=1):
        media_file = os.path.join(folder_path, file_name)
        title = f"Short Part {index} #Shorts #comedy"
        description = f"This is only for entertainment {index} #Shorts"
        tags = ["shorts", "youtube shorts", "python", "api","enjoy"]
        upload_short(youtube, media_file, title, description, tags)



























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

#     # Remove old token file for re-authentication (optional)
#     if os.path.exists(TOKEN_FILE):
#         os.remove(TOKEN_FILE)

#     # Update with the full path to your client secrets JSON file if necessary
#     client_secrets_file = r"C:\Users\om\DemoProject\client_secrets.json"

#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secrets_file, SCOPES
#     )
    
#     # Force using fixed port 8080 so the redirect URI is always consistent
#     credentials = flow.run_local_server(port=8080)
#     youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
#     return youtube

# def upload_short(youtube, media_file, title, description, tags):
#     """
#     Uploads a single video to YouTube with Shorts-friendly metadata.
#     Assumes video is <60s and vertical (9:16).
#     """
#     request_body = {
#         "snippet": {
#             "categoryId": "22",  # 'People & Blogs' (commonly used for Shorts)
#             "title": title,
#             "description": description,
#             "tags": tags
#         },
#         "status": {
#             "privacyStatus": "public"  # or 'private'/'unlisted' if you prefer
#         }
#     }

#     print(f"Uploading: {media_file}")
#     if not os.path.exists(media_file):
#         print("❌ File not found:", media_file)
#         return None

#     # Create an insert request for the video
#     request = youtube.videos().insert(
#         part="snippet,status",
#         body=request_body,
#         media_body=googleapiclient.http.MediaFileUpload(
#             media_file,
#             chunksize=-1,
#             resumable=True
#         )
#     )

#     response = None
#     while response is None:
#         status, response = request.next_chunk()
#         if status:
#             print(f"Upload progress: {int(status.progress() * 100)}%")

#     video_id = response["id"]
#     print(f"✅ Short uploaded with ID: {video_id}\n")
#     return video_id

# def upload_all_shorts(youtube, folder_path):
#     """
#     Loops through all .mp4 files in 'folder_path' and uploads each as a Short.
#     """
#     # Get all .mp4 files in the folder and sort them alphabetically
#     files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp4')]
#     if not files:
#         print("❌ No video files found in folder:", folder_path)
#         return

#     files.sort()  # e.g., "Part 1.mp4", "Part 2.mp4", etc.

#     # Loop through the files and upload each one sequentially
#     for index, file_name in enumerate(files, start=1):
#         media_file = os.path.join(folder_path, file_name)
#         # Add "#Shorts" to the title and description so YouTube can recognize these as Shorts
#         title = f" {index} #Shorts #comedy"
#         description = f"Automatically uploaded YouTube Shorts part {index} #Shorts"
#         tags = ["shorts", "youtube shorts", "python", "api"]
        
#         # Upload each file
#         upload_short(youtube, media_file, title, description, tags)

# if __name__ == "__main__":
#     youtube = authenticate_youtube()
    
#     # Set your folder path where your shorts videos are located
#     folder_path = r"C:\Users\om\DemoProject\shorts"
    
#     # Upload all videos from the folder as Shorts
#     upload_all_shorts(youtube, folder_path)






