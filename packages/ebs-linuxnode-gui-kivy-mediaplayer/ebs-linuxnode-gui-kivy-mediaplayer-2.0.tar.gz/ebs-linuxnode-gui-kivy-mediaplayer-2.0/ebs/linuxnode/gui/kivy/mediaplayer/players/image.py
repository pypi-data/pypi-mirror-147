

from kivy_garden.ebs.core.image import StandardImage
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class ImagePlayer(MediaPlayerBase):
    _extensions = ['.png', '.jpg', '.bmp', '.gif', '.jpeg']

    def _play(self, filepath):
        self._player = StandardImage(source=filepath,
                                     allow_stretch=True,
                                     keep_ratio=True)
        return self._player

    def _stop(self):
        pass
