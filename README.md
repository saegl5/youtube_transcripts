# youtube_transcripts
Use YouTube API to download transcription of videos for securities trading opportunities

## Instructions (Linux/macOS)

1. Create virtual environment: `python3 -m venv myenv`
2. Activate it: `source myenv/bin/activate`
3. Set it up: `pip install -r requirements.txt`
4. Open interactive shell: `python3`
5. In the shell:
```
>>> from src.transcribe import transcript_from_url
>>> transcript_from_url("https://www.youtube.com/watch?v=VIDEO_ID") # input VIDEO_ID
```
Alternatively, you can just input the VIDEO_ID: `transcript_from_url("VIDEO_ID")`