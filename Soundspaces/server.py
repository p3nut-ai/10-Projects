# Sound Space
from requests import post, get
from flask import Flask, request, redirect, render_template
import json
from bs4 import BeautifulSoup
import requests

# from dotenv import load_dotenv
import os

app = Flask(__name__)

# load_dotenv()


s_PORT=5000
s_CLIENT_ID = "b2a10394dd294174a4031a74a4b8bb6b"
s_CLIENT_SECRET = "ecba4ca3bd0048d7b5d5370ccf6812c5"
s_REDIRECT_URI = "http://127.0.0.1:5000/callback"
s_FLASK_SECRET_KEY = "fdee78c64c4d4b1f0afdc146fd8ff8f822595e8baec46b86"


# Spotify API credentials
client_id = s_CLIENT_ID
client_secret = s_CLIENT_SECRET
redirect_uri = s_REDIRECT_URI
PORT = s_PORT

class SpotifyApi:
    def __init__(self):
        self.token = None

    def get_auth_url(self):
        scope = "user-read-recently-played user-follow-read"  # Added user-follow-read scope
        auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
        return auth_url

    def get_token(self, auth_code):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }
        result = post(url, headers=headers, data=data)

        if result.status_code != 200:
            print(f"Error getting token: {result.content}")
            return None

        json_result = json.loads(result.content)
        self.token = json_result["access_token"]
        return self.token

    def get_auth_header(self):
        return {"Authorization": "Bearer " + self.token}

    def search_for_artist(self, artist_name):
        if artist_name:
            try:
                url = "https://api.spotify.com/v1/search"
                headers = self.get_auth_header()
                query = f"?q={artist_name}&type=artist&limit=1"

                print(query)

                query_url = url + query
                result = get(query_url, headers=headers)

                if result.status_code != 200:
                    print(f"Error searching for artist: {result.content}")
                    return None

                json_result = json.loads(result.content)

                if "artists" not in json_result or not json_result["artists"]["items"]:
                    print("Artist name does not exist...")
                    return None

                artist_info = json_result["artists"]["items"][0]  # Get the first artist found
                followers = artist_info["followers"]["total"] if artist_info.get("followers") else None


                print(f"ARTIST ID : {artist_info['id']}")

                return {
                    "id": artist_info["id"],
                    "name": artist_info["name"],
                    "images": artist_info["images"],
                    "followers": format(followers, ",")
                }
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
        return None  # Return None if artist_name is missing

    def get_artist_followers(self, artist_info):
        return artist_info["followers"] if artist_info and "followers" in artist_info else None

    def get_artist_image(self, artist_info):
        return artist_info["images"][0]["url"] if artist_info and "images" in artist_info and artist_info["images"] else None

    def get_songs_by_artist(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=PH"
        headers = self.get_auth_header()

        result = get(url, headers=headers)

        if result.status_code != 200:
            print(f"Error getting songs: {result.content}")
            return None

        json_result = json.loads(result.content)
        return json_result["tracks"]


    def get_recently_played_tracks(self):
        url = "https://api.spotify.com/v1/me/player/recently-played"
        headers = self.get_auth_header()

        result = get(url, headers=headers)

        if result.status_code != 200:
            print(f"Error getting recently played tracks: {result.content}")
            return None

        json_result = json.loads(result.content)
        return json_result["items"]

    def get_followed_artists(self):
        url = "https://api.spotify.com/v1/me/following?type=artist&limit=5"  # Limit to 5 artists
        headers = self.get_auth_header()

        result = get(url, headers=headers)

        if result.status_code != 200:
            print(f"Error getting followed artists: {result.content}")
            return None

        json_result = json.loads(result.content)
        return [{
            "id": artist["id"],
            "name": artist["name"],
            "genres": artist["genres"],
            "popularity": artist["popularity"],
            "external_url": artist["external_urls"]["spotify"],
            "image": artist["images"][0]["url"] if artist["images"] else None
        } for artist in json_result["artists"]["items"]]

    def get_artist_banner(self, artist_id):
        url = f"https://open.spotify.com/artist/{artist_id}"
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser') # return respons na HTML format

        monthly_listeners_span = soup.find('span', class_='Ydwa1P5GkCggtLlSvphs')

        # Extract the text content
        if monthly_listeners_span:
            monthly_listeners_text = monthly_listeners_span.text
            # Split the text to get the number part
            monthly_listeners = monthly_listeners_text.split()[0]  # Get the first part which is the number
            print(monthly_listeners)
        else:
            print("Element not found")

    def check_if_user_follows_artist(self, artist_id):
        url = "https://api.spotify.com/v1/me/following/contains"
        headers = self.get_auth_header()
        data = {
            "type": "artist",
            "ids": artist_id  # Single artist ID
        }

        result = get(url, headers=headers, json=data)

        if result.status_code != 200:
            print(f"Error checking follow status: {result.content}")
            return None

        return result.json()  # Returns a list of booleans indicating follow status

    def get_artist_about(self, artist_id):
        url = f'https://open.spotify.com/artist/{artist_id}'  # Replace with the actual URL

        # Fetch the HTML content
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the span by its class
        span = soup.find('span', class_='G_f5DJd2sgHWeto5cwbi')

        # Check if the span was found and print its text
        if span:
            about = span.text
            return about
        else:
            return

    def get_artist_monthly_listeners(self, artist_id):
        url = f'https://open.spotify.com/artist/{artist_id}'  # Replace with the actual URL

        # Fetch the HTML content
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the span by its class
        span = soup.find('div', class_='fjP8GyQyM5IWQvTxWk6W')

        # Check if the span was found and print its text
        if span:
            monthly_listeners = span.text
            return monthly_listeners
        else:
            return

    def get_artist_tracks(self, artist_id):
        url = f"https://open.spotify.com/artist/{artist_id}"
        response = requests.get(url)
        songs = []
        songs = self.get_songs_by_artist(artist_id)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print('SOUP', soup)
            spans = soup.find_all('span', class_='ListRowTitle__LineClamp-sc-1xe2if1-0 jjpOuK')
            paragraphs = soup.find_all('p', class_='e-9541-text encore-text-body-small encore-internal-color-text-subdued ListRowDetails__ListRowDetailText-sc-sozu4l-0 hxCObm')

            results = []

            for span, paragraph, song in zip(spans, paragraphs, songs):
                title =  span.text.strip()
                plays = paragraph.text.strip()

                # Calculate duration in seconds
                duration_ms = song["duration_ms"]
                total_seconds = duration_ms / 1000

                # Calculate minutes and seconds
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)

                # Format the duration as MM:SS
                formatted_duration = f"{minutes}:{seconds:02d}"

                results.append({
                    "title": title,
                    "plays": plays,
                    "duration": formatted_duration
                })

            return results

        return None

spotify_api = SpotifyApi()

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    token = spotify_api.get_token(auth_code)

    if token:
        print("Token retrieved successfully.")
        return redirect('/home')  # Redirect to the home page
    else:
        print("Failed to retrieve token.")
        return redirect('/')

@app.route('/')
def index():
    auth_url = spotify_api.get_auth_url()
    return render_template('index.html', auth_url=auth_url)

@app.route('/search_artist', methods=['GET','POST'])
def search_artist():
    artist_name = request.form.get('artist_name')
    if artist_name:
        return redirect(f'/artist?artist_name={artist_name}')
    return redirect('/')

@app.route('/home')
def home():
    if spotify_api.token:
        followed_artists = spotify_api.get_followed_artists()
        return render_template('home.html', followed_artists=followed_artists)
    return redirect('/')

@app.route('/artist', methods=['GET', 'POST'])
def artist_track():
    if spotify_api.token:
        artist_name = request.args.get('artist_name')
        artist = spotify_api.search_for_artist(artist_name)

        songs = []
        top_tracks = []
        artist_image = None
        artist_followers = 0
        artist_banner = None
        following = False
        about = None
        monthly_listeners = None
        tracks = {}

        if artist is not None:
            artist_id = artist["id"]
            songs = spotify_api.get_songs_by_artist(artist_id)
            artist_image = spotify_api.get_artist_image(artist)
            artist_followers = spotify_api.get_artist_followers(artist)
            artist_banner = spotify_api.get_artist_banner(artist_id)
            about = spotify_api.get_artist_about(artist_id)
            monthly_listeners = spotify_api.get_artist_monthly_listeners(artist_id)
            tracks = spotify_api.get_artist_tracks(artist_id)

            # Check if the artist is followed
            following_status = spotify_api.check_if_user_follows_artist(artist_id)
            following = following_status[0] if following_status is not None else False  # Get the follow status

        for song in songs:
            song["duration_minutes"] = round(song["duration_ms"] / 60000, 2)
            song["popularity"] = song.get("popularity", "N/A")

        artist_play_count = {}

        # Get recently played tracks
        recently_played_tracks = spotify_api.get_recently_played_tracks()
        if recently_played_tracks:
            for item in recently_played_tracks:
                track_artists = item['track']['artists']  # Get the artists of the track

                # Increment the play count for each artist in the track
                for track in track_artists:
                    top_artist = track['name']
                    if top_artist in artist_play_count:
                        artist_play_count[top_artist] += 1
                    else:
                        artist_play_count[top_artist] = 1

        # Sort the artists by play count and get the top 10
        top_played_artists = sorted(artist_play_count.items(), key=lambda x: x[1], reverse=True)[:5]
        for artist_name, count in top_played_artists:
            top_tracks.append({"artist": artist_name, "count": f"{count:,}"})  # Reduced redundant API calls


        # Get the top 5 recently followed artists
        followed_artists = spotify_api.get_followed_artists()

        return render_template('artist.html', top_tracks=top_tracks,
                               artist_name=artist_name,
                               artist_banner=artist_banner, artist_image=artist_image,
                               following=following, about=about, monthly_listeners=monthly_listeners, tracks=tracks,
                               followed_artists=followed_artists)
    return redirect('/')



@app.route('/wrapped', methods=['GET', 'POST'])  # Correctly placed outside of any other function
def wrapped():
    if spotify_api.token:
        artist_play_count = {}

        # Get recently played tracks
        recently_played_tracks = spotify_api.get_recently_played_tracks()
        if recently_played_tracks:
            for item in recently_played_tracks:
                track_artists = item['track']['artists']  # Get the artists of the track

                # Increment the play count for each artist in the track
                for track in track_artists:
                    top_artist = track['name']
                    if top_artist in artist_play_count:
                        artist_play_count[top_artist] += 1
                    else:
                        artist_play_count[top_artist] = 1

        # Sort the artists by play count and get the top 10
        top_played_artists = sorted(artist_play_count.items(), key=lambda x: x[1], reverse=True)[:5]

        wrapped_data = []
        for top_artist, count in top_played_artists:
            artist_info = spotify_api.search_for_artist(top_artist)  # Call the function to get artist info
            artist_pfp = spotify_api.get_artist_image(artist_info)  # Get the artist's profile image

            wrapped_data.append({
                "artist": top_artist,
                "image": artist_pfp,
                "count": f"{count:,}"
            })

        return render_template('wrapped.html', wrapped_data=wrapped_data)

    return redirect('/')



if __name__ == '__main__':
    app.run(port=int(PORT), debug=True)
