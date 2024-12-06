from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, VideoClip
from typing import Union


class FlipVerticallyVideoEffect(VideoEffect):
    """
    This effect flips the video vertically.
    """

    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
        Applies the effect to the provided 'video'.
        """
        video = VideoEffect.parse_moviepy_video(video)

        effect_name = VideoEffect.get_moviepy_vfx_effect('mirror_y')
        parameters = {}

        return video.fx(effect_name, **parameters)