

from kivy_garden.ebs.pdfplayer import PDFPlayer
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class PdfPlayer(MediaPlayerBase):
    _extensions = ['.pdf']

    def _play(self, filepath, interval=None):
        self._player = PDFPlayer(source=filepath,
                                 temp_dir=self.actual.temp_dir)
        if interval:
            self._player.interval = interval
        return self._player

    def _stop(self):
        self._player.stop()
