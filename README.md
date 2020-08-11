# Bensound-Python-API
A Python API for accessing the music, metadata, and associated images from www.bensound.com.



## BensoundAPI
The main constructor for accessing the data from www.bensound.com. This API contains several methods which are useful for listening to, downloading, or purchasing music on the website. Download links are provided, and if the license is not FREE, a download link is provided as a song attribute.

### Attributes

**channels : *dict***  
contains all available channels and corresponding urls  

**channel_playlist : *dict***  
contains all available channels and a list of songs tagged to each channel  

**music_list : *dict***  
a list of dictionaries containing song objects extracted from www.bensound.com   

### Methods

**get_channel_playlist(channel_name=None)**  
Extracts the name of all channels with a list of associated songs; accepts a valid channel name located in `channels`, or `None` to get data for all channels.  

**get_channels()**  
Extracts all available channels with a corresponding url  

**get_all_music()**  
Extracts all available music data from www.bensound.com and updates the class attributes `channels`, `channel_playlist`, and `music_list`  

