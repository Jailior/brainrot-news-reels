import backend.services.audio_generator as AudioGenerator
from backend.config import settings
import backend.services.script_generator as ScriptGenerator
from backend.services.news_fetcher import NewsFetcher
from backend.models.article import Article

audio_generator = AudioGenerator.AudioGenerator()
script_generator = ScriptGenerator.ScriptGenerator()
news_fetcher = NewsFetcher()

print("Fetching articles from NewsAPI...")
article_data = news_fetcher.fetch_articles(page_size=2)[0]
normalized_id = article_data["unique_id"].replace(" ", "_").replace(".", "_").replace("\'", "").lower()

article = Article(id=normalized_id, title=article_data["title"], content=article_data["content"])

print("Generating script using OpenRouter API...")
script = script_generator.generate_script(article)
print(script[:500])

script_path = script_generator.save_script(normalized_id, script)
print(f"Script saved to file with ID: {normalized_id}")

print("Generating audio using ElevenLabs API...")
response = audio_generator.generate_audio(script, "qeS8uAmQhHubeX9yv1e9")

print(f"Saving audio to temporary directory with ID: {normalized_id}...")
audio_generator.save_audio_to_temp(response, normalized_id)

word_timestamps = audio_generator.get_word_timestamps(response.alignment, settings.MAX_CHAR_TO_DISPLAY)
print(word_timestamps)
