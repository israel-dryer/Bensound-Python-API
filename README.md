# Bensound-Python-API
A Python API for accessing the music, metadata, and associated images from www.bensound.com.


| class name       |    description   |
|:---------------- |:---------------- |
|[BensoundAPI]()  | The main constructor for accessing data from the wwww.bensound.com.|
|[Song]()         | A container for song data, methods, and attributes |


## BensoundAPI
The main constructor for accessing the data from www.bensound.com. This API contains several methods which are useful for listening to, downloading, or purchasing music on the website. Download links are provided, and if the license is not FREE, a download link is provided as a song attribute.

### Attributes

**BensoundAPI.channels : *dict***  
contains all available channels and corresponding urls  

**BensoundAPI.channel_playlist : *dict***  
contains all available channels and a list of songs tagged to each channel  

**BensoundAPI.music_list : *dict***  
a list of dictionaries containing song objects extracted from www.bensound.com   

### Methods

`get_channel_playlist
