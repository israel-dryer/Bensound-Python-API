# Bensound-Python-API
A Python API for accessing the music, metadata, and associated images from www.bensound.com.

See the [Getting Started](https://github.com/israel-dryer/Bensound-Python-API/blob/master/bensound-getting-started.ipynb) notebook for some basic usage examples.

## BensoundAPI : *class*
The main constructor for accessing the data from www.bensound.com. This API contains several methods which are useful for listening to, downloading, or purchasing music on the website. Download links are provided, and if the license is not FREE, a download link is provided as a song attribute.

### Attributes

>**channels : *dict***  
>Contains all available channels and corresponding urls.  

>**channel_playlist : *dict***  
>Contains all available channels and a list of songs tagged to each channel.  

>**music_lists : *tuple***  
>A tuple containing two lists; the first is a list of songs, and the second contains the song objects in the same order.     

### Methods

>**get_channel_list()**  
>A convience method to print a list of available channels.

>**get_song_list()**  
>A convenience method to print a list of available song titles.    

>**get_songs_by_channel(channel_name=None)**   
>Print a list of songs for a specified channel. If no channel is provided, then all channels will be printed with their corresponding playlist.  

>**get_song_by_index(song_index)**  
>Retrieve a song object by index; the index corresponds to the title index in the `music_list`, which you can also see by calling `get_song_list()`.  

>**get_song_by_title(song_title)**
Retrieve a song object by finding the first song with the title matching `song_title`. This match is case-sensitive. Call the `get_song_list()` method if you want to see what your options are.  

>**extract_channels()**  
>Extracts all available channels with a corresponding url.  

>**extract_all_data()**  
>Extracts all available music data from www.bensound.com and updates the class attributes `channels`, `channel_playlist`, and `music_lists`. Does NOT download the MP3 files.  

>**extract_channel_music(channel_name=None)**  
>Extract song data for all songs in a specified channel, or returns all songs if no channel is provided.  


## Song : *class*
A container for the royalty free music extracted from www.bensound.com.  

### Attributes
>**title : *str***  
>A song title.  
  
>**length : *str***  
>The length of the song in mins:seconds.  
  
>**description : *str***  
>A brief description of the song.  
  
>**for_download : *bool***  
>Indicates whether the song is free to download.  
  
>**for_purchase : *bool***  
>Indicates whether the song is available for purchase.  
  
>**license : *str***  
>A summary of the license information, if available.  
  
>**url_main : *str***   
>The homepage of the song on www.bensound.com.  
  
>**url_image : *str***   
>The url of the artwork used for the wong on www.bensound.com.  
  
>**url_purchase : *str***   
>A url link for purchasing the song from www.bensound.com.  
  
>**date_requested : *str***
>A string formatted date that shows the date of the request for data.  
  
### Methods

>**get_properties()**  
>Returns a dictionary containing all properties for a song; useful when uploading song properties to a database or json file.   

>**get_song_stream()**  
>Creates a streaming `BytesIO` object that can be used by an application for media playback.  

>**get_song_art()**  
>Creates an in-memory image object from the image url stored in the `url_image`.  

>**download_mp3(destination=None)**  
>Download the MP3 file from the URL stored in the `url_mp3` property. If no destination is provide, the song will be download to the current working directory. The file must be downloadable for this method to work. While you can technically download any file that requires purchase, it will include voice-over markers. You must purchase any music containing voiceovers from www.bensound.com to access the clean version of the song.  
