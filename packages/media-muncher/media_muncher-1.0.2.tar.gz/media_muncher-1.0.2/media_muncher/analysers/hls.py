from functools import lru_cache

import m3u8
from media_muncher.codecstrings import CodecStringParser
from media_muncher.handlers.hls import HLSHandler
from media_muncher.messages import WarningMessage
from pymediainfo import MediaInfo


class HlsAnalyser:
    def __init__(self, handler: HLSHandler) -> None:
        self.handler = handler

        self.messages = []

    def extract_renditions(self):
        m3u8_obj: m3u8.M3U8 = self.handler.document

        # Get info about renditions
        audio_renditions = {}
        video_renditions = {}

        for variant in m3u8_obj.playlists:
            resolution = variant.stream_info.resolution
            bandwidth = variant.stream_info.bandwidth
            frame_rate = variant.stream_info.frame_rate

            codecstrings = variant.stream_info.codecs
            codecs = CodecStringParser.parse_multi_codec_string(codecstrings)

            for codec in codecs:
                video_profile = "main"
                if codec["type"] == "video":
                    video_profile = codec.get("profile")
                    codec["resolution"] = resolution or self.get_resolution(
                        variant.absolute_uri
                    )
                    codec["bitrate"] = bandwidth
                    codec["framerate"] = frame_rate or self.get_framerate(
                        variant.absolute_uri
                    )
                    codec["audio-group"] = variant.stream_info.audio
                    video_renditions[variant.uri] = codec

                if codec["type"] == "audio":
                    # If the variant playlist has no resolution, it's a proper audio playlist
                    if not variant.stream_info.resolution:
                        key = variant.uri
                        codec["bitrate"] = bandwidth
                    else:
                        # We find the audio playlist through the associate media
                        key = variant.stream_info.audio
                        # TODO - better mechanism to actually extract audio info when muxed in
                        # TODO - support multiple languages and multiple bitrates
                        if video_profile == "baseline":
                            codec["bitrate"] = 64000
                        else:
                            codec["bitrate"] = 128000

                    audio_renditions[key] = codec

                    if len(variant.media) and variant.media[0].uri is None:
                        codec["muxed"] = True

                # TODO - when audio not muxed in (separate or adjoining streaminf),
                #  adjust bitrate of video to remove audio

                # TODO - extract audio bitrate and sample rate with ffprobe?

        return [*video_renditions.values(), *audio_renditions.values()]

    def extract_packaging_info(self):
        return {
            "packaging": "HLS",
            "version": self.handler.protocol_version(),
            "container": self.handler.container_format(),
            "segment_duration_max": self.handler.target_duration(),
            "segment_duration": self.handler.standard_segment_duration(),
            "audio_only": self.handler.has_audio_only(),
            "muxed_audio": self.handler.has_muxed_audio(),
        }

    @lru_cache()
    def _analyse_first_segment(self, playlist_url):
        sub = m3u8.load(playlist_url)
        if sub.segment_map:
            first_segment = sub.segment_map[0]
        else:
            first_segment = sub.segments[0]
        return MediaInfo.parse(first_segment.absolute_uri)

    def get_framerate(self, playlist_url):
        try:
            media_info = self._analyse_first_segment(playlist_url)
            for track in media_info.tracks:
                if track.track_type == "Video":
                    frame_rate = track.frame_rate
                    if not frame_rate:
                        if track.frame_rate_mode == "VFR":
                            self.messages.append(
                                WarningMessage(
                                    f"Variable frame rate found in segments in {playlist_url}"
                                )
                            )
                        else:
                            self.messages.append(
                                WarningMessage(
                                    f"No frame rate found in segments in {playlist_url}"
                                )
                            )
                    else:
                        return float(track.frame_rate)
        except Exception as e:
            self.messages.append(
                WarningMessage(message=f"Unable to analyze media: {e}")
            )
            return None

    def get_resolution(self, playlist_url):
        try:
            media_info = self._analyse_first_segment(playlist_url)
        except Exception as e:
            self.messages.append(WarningMessage(f"Unable to analyze media: {e}"))
            return None
        for track in media_info.tracks:
            if track.track_type == "Video":
                resolution = track.width, track.height
                if not resolution:
                    self.messages.append(
                        WarningMessage(
                            f"No resolution found in segments in {playlist_url}"
                        )
                    )
                else:
                    return resolution
