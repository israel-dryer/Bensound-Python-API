"""
    An API for www.bensound.com
    Author: Israel Dryer
    Modified: 2020-08-11
"""
from io import BytesIO
from PIL import Image
import requests
import pathlib
import sqlite3
import datetime
from bs4 import BeautifulSoup

TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

class BensoundAPI:
    """An API for accessing the music, metadata, and associated images from the 
    www.bensound.com site.

    This API contains several methods which are useful for listening to, downloading, or
    purchasing music on the www.bensound.com website. Download links are provided, and if
    the license is not FREE, a download link is provided as a song attribute.

    Attributes
    ----------
    channels : dict
        Contains all available channels and corresponding urls.

    channel_playlist : dict
        Contains all available channels and a list of songs tagged to those channels.

    music_listss : tuple of lists
        A tuple containing two lists; the first is a list of songs, and the second is the song
        objects in the same order.

    Methods
    -------
    get_song_list():
        A convenience method to print a list of available song titles. 
    
    get_channel_list():
        A convience method to print a list of available channels.

    get_songs_by_channel(channel_name=None)
        Retrieve a list of songs from the specificed channel_name, or all channels with their
        cooresponding songs if none is provided.

    get_song_by_index(song_index)
        Retrieve a song object by index; the index corresponds to the title index in the
        `music_lists`, which you can also see by calling `get_song_list()`

    get_song_by_title(song_title)
        Retrieve a song object by finding the first song with the title matching `song_title`.
        This match is case-sensitive. Call the `get_song_list` method if you want to see what
        your options are.

    extract_channels()
        Extracts all available channels with a corresponding channel url.

    extract_channel_music(channel_name=None)
        Extract song data for all songs in a specified channel, or returns all songs
        if no channel is provided.

    extract_all_data()
        Extracts all available music data from www.bensound.com and updates the class attributes
        `channels`, `channel_playlist`, and `music_list`. Does NOT download the MP3 files.    
    """
    def __init__(self):
        self.channels = None
        self.channel_playlist = None
        self.music_lists = None

    def extract_all_data(self):
        """Extracts all available music data from www.bensound.com and updates the class attributes
        `channels`, `channel_playlist`, and `music_list`. Does NOT download the MP3 files.
        """
        unique_titles = []
        media_list = [] 
        if not self.channels:
            self.extract_channels()
        channels = list(self.channels.keys())
        channel_playlist = {channel: [] for channel in channels}

        for channel_name in channels:
            channel_media = self.extract_channel_music(channel_name)
            for song in channel_media:
                channel_playlist[channel_name].append(song.title)
                if song.title not in unique_titles:
                    unique_titles.append(song.title)
                    media_list.append(song)
        self.music_lists = ([song.title for song in media_list], media_list)
        self.channel_playlist = channel_playlist

        # report results
        print('Channels:', len(self.channels))
        print('Songs:', len(self.music_lists[0]))

    def extract_channels(self):
        """Get channels available on www.bensound.com. A channel is essentially 
        a style tag assigned to a song for the purpose of categorization. A song
        can be assigned to more than one channel.
        
        Returns
        -------
        dict
            channel name and channel url
        """
        soup = self.__get_page_soup('https://www.bensound.com/')
        menu_tags = soup.find('div', id='menu').find_all('a')
        channels = {tag.text: tag['href'] for tag in menu_tags if tag.text != 'All'}
        self.channels = channels
        return channels        

    def extract_channel_music(self, channel_name):
        """Extract and return a list of dictionaries containing all available songs 
        from the selected channel.
        
        Parameters
        ----------
        channel_name : str  
            A name referring to a the category tag associated with a music style. 
            Current, this can be seen on the top of the www.bensound.com website as 
            a list of music styles that you can page through. You can see a list of 
            the available channels by looking at the options listed on the website, 
            or by calling the `extract_channels` method.

        Returns
        -------
        list of dict
            A list of dictionaries containing song attributes scraped from the 
            www.bensound.com website.

        """
        if not self.channels:
            self.extract_channels
        channel_url = self.channels[channel_name]
        urls_to_fetch = [channel_url]
        urls_fetched = []
        songlist = []

        while urls_to_fetch:
            url = urls_to_fetch.pop(0) # get first url in list
            urls_fetched.append(url)
            soup = self.__get_page_soup(url) # extract html for parsing
            # find additional pages that may existing via pagination
            pages = self.__get_pagination(soup, urls_to_fetch, urls_fetched)
            if pages:
                urls_to_fetch.extend(pages)
            # extract the names of all songs from the page
            songlist.extend(self.__scrape_page_data(soup))

        return songlist

    def get_channel_list(self):
        """A convience method to print a list of channels"""
        if self.channels:
            print(list(self.channels.keys()))
        else:
            print('No channels available')

    def get_song_list(self):
        """A convience method to print a list of song titles from `music list`"""
        song_list = self.music_lists[0]
        if song_list:
            print(song_list)
        else:
            print('No songs available')

    def get_songs_by_channel(self, channel_name=None):
        """Retrieve a list of all song names associated with a channel.

        Parameters
        ----------
        channel_name : str
            A name referring to a the category associated with a music style. 
            Currently, this can be seen on the top navbar of the www.bensound.com website as 
            a list of music styles that you can page through. You can see a list of the 
            available channels by looking at the options listed on the website, 
            or by calling the `list_of_channels` method.

        Returns
        -------
        list
            A list of song names associated with the `channel_name` argument
        """
        if channel_name:
            try:
                print('Channel:', channel_name)
                print('Songs:')
                print(self.channel_playlist[channel_name])
            except KeyError:
                print('No songs available for this channel name')
        else:
            if self.channel_playlist:
                for channel, playlist in self.channel_playlist.items():
                    print('Channel:', channel)
                    print('Songs:')
                    print(playlist)
                    print('-'*55)
            else:
                print('No channel playlist available')

    def get_song_by_index(self, song_index):
        """Retrieve a song object by index"""
        try:
            return self.music_lists[song_index]
        except IndexError:
            print('Bad song index')
            return

    def get_song_by_title(self, song_title):
        """Retrieve a song object by finding the first song with the title corresponding to `song_title`"""
        song_names = self.music_lists[0]
        song_objects = self.music_lists[1]
        if song_names:
            song_index = song_names.index(song_title)
            if song_index:
                try:
                    return song_objects[song_index]
                except IndexError:
                    print('Bad song index')
            else:
                print('Song does not exists by that name')
        else:
            print('No songs currently available in `music_lists`')


    def __scrape_page_data(self, soup):
        """Extract media attributes for all media block containers on a page"""
        media_list = []
        block_container = soup.find('div', 'bloc_cat')
        blocks = block_container.find_all('div', ['bloc_produit', 'bloc_produit1'])
        for block in blocks:
            attributes = self.__scrape_block_attributes(block)
            song = Song(**attributes)
            media_list.append(song)
        return media_list      

    @staticmethod
    def __get_page_soup(url):
        """Request site content and return as BeautifulSoup object"""
        response = requests.get(url)
        if response.ok:
            return BeautifulSoup(response.text, 'lxml')

    @staticmethod
    def __get_pagination(soup, to_fetch, fetched):
        """Extract all pagination urls and return new items as a list"""
        nav_tags = soup.find('div', 'pagenavi').find_all('a', 'page')
        new_pages = []
        if nav_tags:
            for tag in nav_tags:
                url = tag['href']
                if url not in to_fetch and url not in fetched:
                    new_pages.append(url)
        return new_pages


    @staticmethod
    def __scrape_block_attributes(block):
        """Extract attributes for a single block_div media container and return as a dictionary"""
        attr = {}
        site_url = 'https://www.bensound.com/'
        attr['title'] = block.find('div', 'titre').p.text.strip()
        attr['length'] = block.find('p', 'totime').text.strip()
        attr['description'] = block.find('div', 'description').text.strip()
        attr['url_main'] = block.find('div', 'img_mini').a['href']
        attr['url_image'] = site_url + block.find('div', 'img_mini').img['src']
        attr['url_mp3'] = site_url + block.find('audio')['src']
        
        # available for download
        try:
            block.find('div', 'bouton_download').text.strip()
            attr['for_download'] = True
        except AttributeError:
            attr['for_download'] = False    
            
        # available for purchase
        try:
            block.find('div', 'bouton_purchase').text.strip()
            attr['for_purchase'] = True
            attr['url_purchase'] = block.find('div', 'pop_license').a['href']
        except AttributeError:
            attr['for_purchase'] = False
            attr['url_purchase'] = ''
            
        # media license
        try:
            l1 = block.find('div', 'pop_license').h1.text.strip() + '.'
        except AttributeError:
            l1 = ""
        try:
            l2 = block.find('div', 'pop_license').p.text.strip() + '.'
        except AttributeError:
            l2 = ""
        l3 = ", ".join([span.text.strip() for span in block.find_all('span', 'nothis')])
        attr['license'] = " ".join([l1, l2, l3]).strip().replace('\xa0', ' ') + '.'
        
        return attr


class Song:
    """A container class for the royalty free music tracks located on www.bensound.com.
    
    Attributes
    ----------
    title : str
        The song title.

    length : str
        The length of the song in mins:seconds.
    
    description : str
        A brief description of the song.
    
    for_download : bool
        Indicates whether the song is free to download.
    
    for_purchase : bool
        Indicated whether to song is available for purchase.
    
    license : str
        A summary of the license if available or not.
    
    url_main : str
        The homepage of the song on www.bensound.com.
    
    url_image : str
        The url of the artwork used for the song on www.bensound.com.
    
    url_purchase : str
        The url link for purchasing the song from www.bensound.com.
    
    modified: str
        A string formatted date that indicates when the records was extracted from
        www.bensound.com.

    Methods
    -------
    properies()
        Returns a dictionary containing all properties for the song. Is useful when
        uploading song properties to a database or to a json file.
    
    get_song_stream()
        Creates a streaming BytesIO object that can be used by an application
        to for media playback.

    get_song_art()
        Creates an in-memory image object from the image file stored at the 
        `url_image` location.

    download_mp3(destination=None)
        Download the mp3 file based on the url stored in `url_mp3`. This is also
        the location that is used for mp3 playback. The file must be downloadable
        for this method to work. You can technically download a file that requires
        purchase, but it will include the voiceover markers. You must purchase
        any music containing voicevers from www.bensound.com to access the clean
        version of the song.
    """
    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.length = kwargs['length']
        self.description = kwargs['description']
        self.for_download = kwargs['for_download']
        self.for_purchase = kwargs['for_purchase']
        self.license = kwargs['license']
        self.url_main = kwargs['url_main']
        self.url_image = kwargs['url_image']
        self.url_mp3 = kwargs['url_mp3']
        self.url_purchase = kwargs['url_purchase']
        self.modified = datetime.datetime.today().strftime('%Y-%m-%d')

    def get_properties(self):
        """Get and return object properties as a dictionary. Useful for uploading
        into a database or for other application interfaces.
        
        Returns
        -------
        dict
            A dictionary containing all object properties
        """
        return self.__dict__

    def get_song_stream(self):
        """Get and return streaming bytes object
        
        Returns
        -------
        BytesIO
            A streaming BytesIO object for media playback.
        """
        response = requests.get(self.url_mp3, stream=True)
        if response.ok:
            stream = BytesIO(response.content)
            return stream

    def get_song_art(self):
        """Creates an in memory image object from the image file stored at 
        the `url_image` location.
        
        Returns
        -------
        Image
            An image object.
        """
        response = requests.get(self.url_image)
        if response.ok:
            img_bytes = BytesIO(response.content)
            image = Image.open(img_bytes)
            return image

    def download_mp3(self, destination=None):
        """Download the mp3 file based on the url stored in `url_mp3`. This is also
        the location that is used for mp3 playback. The file must be downloadable
        for this method to work. You can technically download a file that requires
        purchase, but it will include the voiceover markers. You must purchase
        any music containing voicevers from www.bensound.com to access the clean
        version of the song.

        Parameters
        ----------
        destination : string, optional
            The local file location used to save the download mp3 file.

        Returns
        -------
        None
"""
        # where will this file be saved?
        path = pathlib.Path(destination) if destination else pathlib.Path().cwd()
        filename = self.url_mp3.split('/')[-1]
        
        # download and save the file
        response = requests.get(self.url_mp3)
        if response.ok:
            with open(filename, 'wb') as f:
                f.write(response.content)
