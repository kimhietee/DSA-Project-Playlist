#Track class
class Track:
    def __init__(self, unique_identifier: int, title: str, main_artist: str,
                 album_name: str, duration_mmss: str, creation_order: int,
                 additional_artists=None):
        if additional_artists is None:
            additional_artists = []
        self.unique_identifier = unique_identifier
        self.title = title
        self.main_artist = main_artist
        self.album_name = album_name
        self.additional_artists = list(additional_artists)
        self.duration_seconds = self._convert_mmss_to_seconds(duration_mmss)
        self.creation_order = creation_order

    def _convert_mmss_to_seconds(self, mmss_string: str) -> int:
        parts = mmss_string.strip().split(":")
        if len(parts) != 2:
            raise ValueError("duration must be 'mm:ss'")
        minutes_integer = int(parts[0])
        seconds_integer = int(parts[1])
        return minutes_integer * 60 + seconds_integer

    def to_dictionary(self):
        return {
            "unique_identifier": int(self.unique_identifier),
            "title": self.title,
            "main_artist": self.main_artist,
            "album_name": self.album_name,
            "additional_artists": list(self.additional_artists),
            "duration_seconds": int(self.duration_seconds),
            "creation_order": int(self.creation_order)
        }

    @classmethod
    def from_dictionary(cls, data_dictionary):
        #duration seconds in stored JSON
        duration_seconds_integer = int(data_dictionary["duration_seconds"])
        #convert back to mm:ss string for constructor
        minutes_integer = duration_seconds_integer // 60
        seconds_integer = duration_seconds_integer % 60
        mmss_string = f"{minutes_integer:02d}:{seconds_integer:02d}"
        return cls(
            unique_identifier=int(data_dictionary["unique_identifier"]),
            title=data_dictionary["title"],
            main_artist=data_dictionary["main_artist"],
            album_name=data_dictionary["album_name"],
            duration_mmss=mmss_string,
            creation_order=int(data_dictionary.get("creation_order", 0)),
            additional_artists=data_dictionary.get("additional_artists", [])
        )


#Playlist class
class Playlist:
    def __init__(self, unique_identifier: int, playlist_name: str, creation_order: int):
        self.unique_identifier = unique_identifier
        self.playlist_name = playlist_name
        # track unique identifiers preserve insertion order (date added)
        self.track_unique_identifiers = []
        self.creation_order = creation_order

    def to_dictionary(self):
        return {
            "unique_identifier": int(self.unique_identifier),
            "playlist_name": self.playlist_name,
            "track_unique_identifiers": list(self.track_unique_identifiers),
            "creation_order": int(self.creation_order)
        }

    @classmethod
    def from_dictionary(cls, data_dictionary):
        p = cls(
            unique_identifier=int(data_dictionary["unique_identifier"]),
            playlist_name=data_dictionary["playlist_name"],
            creation_order=int(data_dictionary.get("creation_order", 0))
        )
        p.track_unique_identifiers = list(data_dictionary.get("track_unique_identifiers", []))
        return p
