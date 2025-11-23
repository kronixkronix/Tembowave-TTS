from flask import Flask, request, send_file, jsonify
from orpheus_tts import OrpheusTTS
import tempfile
import os

app = Flask(__name__)

# Default voice
DEFAULT_VOICE = "Tara"

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        text = data.get("text")
        voice = data.get("voice", DEFAULT_VOICE)  # Use default if not provided

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Initialize TTS with selected voice
        tts = OrpheusTTS(voice=voice)

        # Generate speech audio
        audio_bytes = tts.tts(text)

        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(audio_bytes)
        temp_file.close()

        # Return file
        return send_file(temp_file.name, mimetype="audio/wav", as_attachment=True, download_name="speech.wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
