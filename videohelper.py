import scrapetube
from langchain_community.document_loaders.generic import GenericLoader #youtubedan gelen sesın transkirptora aktarır
from langchain_community.document_loaders import YoutubeAudioLoader #youtubedan ses cekemye yarar
from langchain_community.document_loaders.parsers import OpenAIWhisperParser #transkripsiyon 
import os
from dotenv import load_dotenv
from youtubevideo import YoutubeVideo

load_dotenv()
my_key_openai = os.getenv("OPENAI_API_KEY")


#1 Transkripsiyon

def get_video_transcript(url):

    target_dir = "./audios/"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url], save_dir=target_dir),
        OpenAIWhisperParser(api_key=my_key_openai)

    )

    loader.load()

    video_transcript_docs = loader.load()

    return video_transcript_docs

#2 Youtube Araması

def get_videos_for_search_term(search_term, video_count=1, sorting_criteria="relevance"):

    convert_sorting_options = { 
                                "En İlgili" : "relevance",
                                "Tarihe Göre" : "upload_date",
                                "İzlenme Sayısı" : "view_count",
                                "Beğeni Sayısı" : "rating"
                            }
    videos = scrapetube.get_search(query=search_term, limit=video_count, sort_by=convert_sorting_options[sorting_criteria]) #yotuuebedan vıdeolarımız aldık
    videolist = list(videos)

    youtube_videos = []

    for video in videolist:
        new_video = YoutubeVideo(
            video_id = video["videoId"],
            video_title=video["title"]["runs"][0]["text"],
            video_url = "https://www.youtube.com/watch?v=" + video["videoId"],
            channel_name= video["longBylineText"]["runs"][0]["text"],
            duration= video["lengthText"]["accessibility"]["accessibilityData"]["label"],
            publish_date= video["publishedTimeText"]["simpleText"]
        )

        youtube_videos.append(new_video)

    return youtube_videos


    

"""Bu kod, YouTube'dan belirli arama terimleri kullanarak videoları aramak ve seçilen videoların seslerini indirip transkribe etmek için kullanılır. YoutubeAudioLoader sınıfı, belirli bir URL'den YouTube videolarının ses dosyalarını indirir, OpenAIWhisperParser sınıfı bu ses dosyalarını transkribe eder ve scrapetube kütüphanesi, belirtilen arama terimlerine göre YouTube'da video araması yapar. Sonuç olarak elde edilen transkriptler ve YouTube video bilgileri, daha sonra analiz edilebilir veya kullanıcı sorgularına yanıt vermek için kullanılabilir."""