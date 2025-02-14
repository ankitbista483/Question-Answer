import os
import csv
import lyricsgenius as lg

class GeniusLyricsFetcher:
    def __init__(self, access_token, file_path, output_csv):
        self.genius = lg.Genius(access_token)
        self.file_path = file_path
        self.output_csv = output_csv
    
    def fetch_lyrics(self):
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        
        with open(self.output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Song Title', 'Artist', 'Lyrics'])

            
            for song_name in lines[1:]:
                song_name = song_name.strip()  
                print(f"Fetching lyrics for song: {song_name}")

            
                song = self.genius.search_song(title=song_name, artist="Post Malone")

                try:
                    # Get the lyrics
                    lyrics = song.lyrics
                    writer.writerow([song_name, "Post Malone", lyrics])

                except Exception as e:
                    print(f"Error fetching lyrics for {song_name}: {str(e)}")
        
        print(f"Lyrics for all songs have been saved to {self.output_csv}.")


if __name__ == "__main__":
    access_token = os.environ['GENIUS_ACCESS_TOKEN']  
    file_path = '/Users/ankitbista/Desktop/practice/Question-Answer/post_malone_selected_albums.txt'  
    output_csv = 'song_lyrics.csv'  

    lyrics_fetcher = GeniusLyricsFetcher(access_token, file_path, output_csv)
    lyrics_fetcher.fetch_lyrics()


#export GENIUS_ACCESS_TOKEN="SkRrEqxio_HV06K7d_m28omKserqVoktIqL6z37P91kQQe_fDB4Y6gMWuFLj4a4K" 