#api key  = AIzaSyCNRcp3i9K8VzwqkGtq6vnnn3N1nEKugek
import os
import googleapiclient.discovery

def search_for_video(search_query):
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

	api_service_name = "youtube"
	api_version = "v3"
	DEVELOPER_KEY = "AIzaSyCNRcp3i9K8VzwqkGtq6vnnn3N1nEKugek"

	youtube = googleapiclient.discovery.build(
		api_service_name, api_version, developerKey = DEVELOPER_KEY)

	search = youtube.search().list(
		part="snippet",
		maxResults=1,
		q=search_query
	)

	query = search.execute()
	highlight_id = query["items"][0]["id"]["videoId"]

	url  = "https://www.youtube.com/watch?v=" + str(highlight_id)
	return url