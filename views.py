import json
import os
import tempfile
import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from deep_translator import GoogleTranslator

@csrf_exempt
def generate_music(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "").strip()
        target_lang = data.get("language", "en")

        if not prompt:
            return JsonResponse({"error": "Prompt is required"}, status=400)

        # 1. Translate ONLY the user's exact input words
        if target_lang != "en":
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(prompt)
        else:
            translated_text = prompt

        # 2. Setup temporary file path
        temp_dir = tempfile.gettempdir()
        mp3_path = os.path.join(temp_dir, "generated_audio.mp3")

        # 3. Generate TTS audio for the translated text only
        try:
            tts = gTTS(text=translated_text, lang=target_lang)
            tts.save(mp3_path)
        except ValueError:
            # Fallback for Odia if native voice isn't fully supported by gTTS
            tts = gTTS(text=translated_text, lang="hi")
            tts.save(mp3_path)

        # 4. Convert the saved audio file to a Base64 string
        with open(mp3_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

        # Clean up the temporary file
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

        # 5. Return BOTH the translated text and the audio in a JSON response
        return JsonResponse({
            "translated_text": translated_text,
            "audio_base64": audio_base64
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)