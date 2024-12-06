import eyed3
import csv
from pathlib import Path
from os.path import getctime
from datetime import date


def table_content_is_modified(table_content, metavar):
    if metavar is not None:
        if metavar != table_content:
            return True
        else:
            return False
    elif table_content != "":
        return True
    else:
        return False

    
def scan(args):
    mp3 = Path(args.path)
    fp = open(Path.cwd()/"songs.csv", "w", newline="", encoding="utf-8")

    songs_writer = csv.writer(fp)
    songs_writer.writerow(["Title", "New Title", "Artist(s)", "Album","Genre", "Date added", "N°"])

    for song in mp3.rglob("*.mp3"):
        audiofile = eyed3.load(song)
        song_name = song.name[:-4]
        if audiofile is None:
            songs_writer.writerow([song_name])
        else:
            genre = audiofile.tag.genre.name if audiofile.tag.genre else None
            songs_writer.writerow([
                    song_name, 
                    None,  # New Title
                    audiofile.tag.artist, 
                    audiofile.tag.album, 
                    genre, 
                    date.fromtimestamp(getctime(song)),
                    audiofile.tag.track_num.count
                    ])
    fp.close()


def edit(args):
    mp3 = Path(args.path)
    csv_file = Path.cwd()/args.csv
    csv_is_modified = False
    with open(csv_file, encoding="utf-8") as fp:
        songs_reader = csv.reader(fp)
        rows = list(songs_reader)[1:]
        for index, row in enumerate(rows):
            filename = row[0] + ".mp3"
            try:
                audiofile = eyed3.load(mp3/filename)
            except OSError:
                print("failed to load the song", mp3/filename)
                continue
            if audiofile is not None:
                if table_content_is_modified(row[2], audiofile.tag.artist):
                    print(filename, f"artist: {audiofile.tag.artist} → '{row[2]}'")
                    audiofile.tag.artist = row[2]
                    audiofile.tag.save()
                if table_content_is_modified(row[3], audiofile.tag.album):
                    print(filename, f"album: {audiofile.tag.album} → '{row[3]}'")
                    audiofile.tag.album = row[3]
                    audiofile.tag.save()
                
                genre = audiofile.tag.genre.name if audiofile.tag.genre else None
                if table_content_is_modified(row[4], genre):
                    print(filename, f"genre: {genre} → '{row[4]}'")
                    audiofile.tag.genre = row[4]
                    audiofile.tag.save()

            if row[1] != "" and row[1] != row[0]:
                print(f"filename: {row[0]} → {row[1]}")
                (mp3/Path(filename)).rename(mp3/(row[1]+".mp3"))
                updated_row = row
                updated_row[0] = row[1]
                updated_row[1] =  None
                rows[index] = updated_row
                csv_is_modified = True
                
    if csv_is_modified:
        with open(csv_file, "w", newline="", encoding="utf-8") as fp:
            songs_writer = csv.writer(fp)
            songs_writer.writerow(["Title", "New Title", "Artist(s)", "Album","Genre", "Date added", "N°"])
            songs_writer.writerows(rows)
            
mp3_path = None