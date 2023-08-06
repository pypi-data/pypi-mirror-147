def upload(**args):

    import os

    import google_auth_oauthlib.flow
    import googleapiclient.discovery
    import googleapiclient.errors

    from googleapiclient.http import MediaFileUpload

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    api_service_name = "youtube"
    api_version = "v3"

    client_secrets_file = args['client_secrets']
    video_file = args['video_file']
    thumbnail = args['thumbnail']
    visibility = args['visibility']
    category = args['category']
    title = args['title']
    description = args['description']
    tags = args['tags']


    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        media_body=MediaFileUpload(video_file),
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            
            },
            
            "status": {
                "privacyStatus": visibility
          }

        }
        
    )
    response = request.execute()

    if 'uploaded' in response['status']['uploadStatus']:
        thumbnail_request = youtube.thumbnails().set(videoId=response['id'], media_body=thumbnail)
        thumbnail_response = thumbnail_request.execute()
        print('Title: "{}"'.format(response['snippet']['title']))
        print('ID: {}'.format(response['id']))
        print('URL: https://youtu.be/{}'.format(response['id']))
    

    print('Status: {}'.format(response['status']['uploadStatus']))