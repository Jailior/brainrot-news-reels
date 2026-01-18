from backend.services.video_compositor import VideoCompositor
import backend.services.audio_generator as AudioGenerator
from backend.config import settings
import backend.services.script_generator as ScriptGenerator
from backend.services.news_fetcher import NewsFetcher
from backend.models.article import Article

audio_generator = AudioGenerator.AudioGenerator()
script_generator = ScriptGenerator.ScriptGenerator()
news_fetcher = NewsFetcher()
video_compositor = VideoCompositor()

print("Fetching articles from NewsAPI...")
article_data = news_fetcher.fetch_articles(page_size=10)
article_data = article_data[1]
normalized_id = article_data["unique_id"].replace(" ", "_").replace(".", "_").replace("\'", "").lower()

article = Article(id=normalized_id, title=article_data["title"], content=article_data["content"])

print("Generating script using OpenRouter API...")
script = script_generator.generate_script(article)
print(script[:500])

print("Generating audio using ElevenLabs API...")
response = audio_generator.generate_audio(script, "qeS8uAmQhHubeX9yv1e9")

print(f"Saving audio to temporary directory with ID: {normalized_id}...")
audio_path = audio_generator.save_audio_to_temp(response, "audio")

word_timestamps = audio_generator.get_word_timestamps(response.alignment, settings.MAX_CHAR_TO_DISPLAY)

srt_output_path = f"tmp/srt_{normalized_id}.srt"
video_compositor.generate_srt_file(word_timestamps, "tmp/subtitles.srt")
print(f"SRT file saved to: tmp/subtitles.srt")

print("Compositing video...")
video_compositor.composite_video(f"tmp/YTParkour1.mp4", "tmp/audio.mp3", "tmp/subtitles.srt", "tmp/video.mp4")
print(f"Video saved to: tmp/video.mp4")
