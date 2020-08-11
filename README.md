# Bensound-Python-API
A Python API for accessing the music, metadata, and associated images from www.bensound.com.



## BensoundAPI : *class*
The main constructor for accessing the data from www.bensound.com. This API contains several methods which are useful for listening to, downloading, or purchasing music on the website. Download links are provided, and if the license is not FREE, a download link is provided as a song attribute.

### Attributes

>**channels : *dict***  
>contains all available channels and corresponding urls  

>**channel_playlist : *dict***  
>contains all available channels and a list of songs tagged to each channel  

>**music_list : *dict***  
>a list of dictionaries containing song objects extracted from www.bensound.com   

### Methods

>**get_channel_playlist(channel_name=None)**  
>Extracts the name of all channels with a list of associated songs; accepts a valid channel name located in `channels`, or `None` to get data for all channels.  

>**get_channels()**  
>Extracts all available channels with a corresponding url  

>**get_all_music()**  
>Extracts all available music data from www.bensound.com and updates the class attributes `channels`, `channel_playlist`, and `music_list`  

## Song : *class*
A container for the royalty free music extracted from www.bensound.com  

### Attributes
>**title : *str***  
>a song title  
  
>**length : *str***  
>the length of the song in mins:seconds  
  
>**description : *str***  
>a brief description of the song  
  
>**for_download : *bool***  
>indicates whether the song is free to download  
  
>**for_purchase : *bool***  
>indicates whether the song is available for purchase  
  
>**license : *str***  
>a summary of the license information, if available  
  
>**url_main : *str***   
>the homepage of the song on www.bensound.com  
  
>**url_image : *str***   
>the url of the artwork used for the wong on www.bensound.com  
  
>**url_purchase : *str***   
>a url link for purchasing the song from www.bensound.com.  
  
>**date_requested : *str***
>A string formatted date that shows the date of the request for data.  
  
### Methods

>**properties()**  
>Returns a dictionary containing all properties for a song; useful when uploading song properties to a database or json file.   

>**get_song_stream()**  
>Creates a streaming `BytesIO` object that can be used by an application for media playback.  

>**get_song_art()**  
>Creates an in-memory image object from the image url stored in the `url_image`.  

>**download_mp3(destination=None)**  
>Download the MP3 file from the URL stored in the `url_mp3` property. This is also the location that is used for MP3 playback. The file must be downloadable for this method to work. You can technically download any file that requires purchase, but it will include voice-over markers. You must purchase any music containing voiceovers from www.bensound.com to access the clean version of the song.  
