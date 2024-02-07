class YoutubeVideo:
    #constructor metod kuralım oncelıkle

    def __init__(self, video_id, video_title, video_url, channel_name, duration, publish_date):

        self.video_id = video_id
        self.video_title = video_title
        self.vide_url = video_url
        self.channel_name = channel_name
        self.duration = duration
        self.publish_date = publish_date
        

"""Bu Python kodu, bir YouTube videosunun ID'si, başlığı, URL'si, kanal adı, süresi ve yayınlanma tarihi gibi özelliklerini saklamak için bir YoutubeVideo sınıfı ve onun yapıcı (__init__) metodunu tanımlar.
"""