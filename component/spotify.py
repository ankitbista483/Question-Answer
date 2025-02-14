
import requests

class SpotifyAPI:
    def __init__(self, access_token):
        self.base_url = 'https://api.spotify.com/v1'
        self.headers = {
            'Authorization': f'Bearer {access_token}'  
        }

    def get_albums(self, artist_id, desired_album_ids):
        url = f'{self.base_url}/artists/{artist_id}/albums?limit=50'
        albums = []

        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                albums.extend(data['items'])
                url = data.get('next')  
            else:
                print(f"Failed to retrieve albums: {response.status_code}")
                break

        return [album for album in albums if album['id'] in desired_album_ids]

    def get_tracks(self, album_id):
        url = f'{self.base_url}/albums/{album_id}/tracks'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()['items']
        else:
            print(f"Failed to retrieve tracks: {response.status_code}")
            return []


class AlbumProcessor:
    def __init__(self, access_token, artist_id, desired_album_ids, output_file):
        self.spotify_api = SpotifyAPI(access_token)
        self.artist_id = artist_id
        self.desired_album_ids = desired_album_ids
        self.output_file = output_file

    def process_albums(self):
        albums = self.spotify_api.get_albums(self.artist_id, self.desired_album_ids)
        
        with open(self.output_file, 'w') as file:
            for album in albums:
                file.write(f"Album: {album['name']}\n")
                tracks = self.spotify_api.get_tracks(album['id'])
                for track in tracks:
                    file.write(f" - {track['name']}\n")


# Example Usage
if __name__ == "__main__":
    access_token = 'BQDFMxXQIMRxPhcKT8zsZ8JtTIsXtJDP-8lfSusoM770Xq2-QONpgzqnVcw34gtMp9tiHLoaDW8L4TFV2_iDRZYFGa-lmMSqQOEa6_LcCxmfgjBBP21fP24xEeeEt_VKYVcV1PMmD7E'  # Your access token
    artist_id = '246dkjvS1zLTtiykXe5h60'  # Post Malone's artist ID
    desired_album_ids = [
        '4f2G7uAWqzpOPwEfCDV87A',  # F-1 Trillion (Long Bed)
        '4g1ZRSobMefqF6nelkgibi',  # Hollywood’s Bleeding
        '1F9LY06gadScF4g3g3BrDC',  # Austin (Bonus)
        '50MzJhO0pMjTsfpeOmZ1so',  # Twelve Carat Toothache (Deluxe)
        '6trNtQUgC8cgbWcqoMYkOR',  # beerbongs & bentleys
        '5s0rmjP8XOPhP6HhqOhuyC'   # Stoney (Deluxe)
    ]
    output_file = 'post_malone_selected_albums.txt'

    album_processor = AlbumProcessor(access_token, artist_id, desired_album_ids, output_file)
    album_processor.process_albums()
