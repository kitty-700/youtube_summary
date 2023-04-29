import sys
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        manual_transcripts = [t for t in transcript_list if not t.is_generated]
        if manual_transcripts:
            transcript = manual_transcripts[0].fetch()
        else:
            generated_transcripts = [t for t in transcript_list if t.is_generated]
            if generated_transcripts:
                transcript = generated_transcripts[0].fetch()
            else:
                sys.exit("자막을 찾을 수 없습니다.")
    except Exception as e:
        sys.exit("Error: " + str(e))

    full_text = " ".join([text['text'] for text in transcript])
    return full_text

if __name__ == "__main__":
    video_url = input("유튜브 영상 URL을 입력하세요: ")
    video_id = video_url.split("watch?v=")[-1]

    transcript_text = get_transcript(video_id)

    print("\n자막:")
    print(transcript_text)
