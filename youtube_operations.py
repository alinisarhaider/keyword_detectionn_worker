import pytube
from pytube import Caption
from pytube import CaptionQuery
from pytube import extract
from pytube import mixins
from pytube import request
from pytube import Stream
from pytube import StreamQuery
from pytube.compat import install_proxy
from pytube.compat import parse_qsl
from pytube.exceptions import VideoUnavailable
from pytube.helpers import apply_mixin
import io
from pydub import AudioSegment


class MyYouTube(pytube.YouTube):
    # https://github.com/nficano/pytube/blob/master/pytube/__main__.py#L150
    def prefetch(self):
        """Eagerly download all necessary data.

        Eagerly executes all necessary network requests so all other
        operations don't does need to make calls outside of the interpreter
        which blocks for long periods of time.

        :rtype: None

        """
        self.watch_html = request.get(url=self.watch_url)
        self.embed_html = request.get(url=self.embed_url)
        self.age_restricted = extract.is_age_restricted(self.watch_html)
        self.vid_info_url = extract.video_info_url(
            video_id=self.video_id,
            watch_url=self.watch_url,
            watch_html=self.watch_html,
            embed_html=self.embed_html,
            age_restricted=self.age_restricted,
        )
        self.vid_info = request.get(self.vid_info_url)
        if not self.age_restricted:
            self.js_url = extract.js_url(self.watch_html, self.age_restricted)
            self.js = request.get(self.js_url)


def get_audio_stream(video_url: str):
    try:
        youtube = MyYouTube(video_url)
    except:
        return 'No YouTube video found for the given URL. Please try some other video.'
    #
    # video_length = int(youtube.player_config_args['player_response']['videoDetails']['lengthSeconds'])
    # if video_length > 90:
    #     return 'Videos longer than 90 seconds cannot be processed because of server limitations. ' \
    #            'Please choose a short video.'

    data = youtube.streams.get_by_itag(140)
    # data.download(output_path='static/', filename='abc')
    # audio_segment_buffer = AudioSegment.from_file('static/abc.mp4', 'mp4')
    data_io = data.stream_to_buffer()
    audio_segment_buffer = AudioSegment.from_file(io.BytesIO(data_io.getvalue()))
    return audio_segment_buffer
