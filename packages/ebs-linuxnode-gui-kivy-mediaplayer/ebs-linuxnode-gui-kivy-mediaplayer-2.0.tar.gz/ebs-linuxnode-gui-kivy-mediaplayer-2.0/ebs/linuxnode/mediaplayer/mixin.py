

import os
from twisted.internet.defer import Deferred
from ebs.linuxnode.core.basemixin import BaseMixin

from .base import MediaPlayerBase


class MediaPlayerBusy(Exception):
    def __init__(self, now_playing, collision_count):
        self.now_playing = now_playing
        self.collision_count = collision_count

    def __repr__(self):
        return "<MediaPlayerBusy Now Playing {0}" \
               "".format(self.now_playing)


class MediaPlayerCoreMixin(BaseMixin):
    def __init__(self, *args, **kwargs):
        super(MediaPlayerCoreMixin, self).__init__(*args, **kwargs)
        self._players = []
        self._current_player = None
        self._media_player_deferred = None
        self._mediaplayer_now_playing = None
        self._end_call = None
        self._mediaplayer_collision_count = 0
        self._media_playing = None

    def install_player(self, player, index=0):
        self.log.info("Installing Media Player {}".format(player.__class__))
        self._players.insert(index, player)

    def _install_builtin_players(self):
        pass

    def install(self):
        super(MediaPlayerCoreMixin, self).install()
        self._install_builtin_players()

    def media_play(self, content, duration=None, **kwargs):
        # kwargs : loop=False, interval=None
        # Play the media file at filepath. If loop is true, restart the media
        # when it's done. You probably would want to provide a duration with
        # an image or with a looping video, not otherwise.
        if self._mediaplayer_now_playing:
            self._mediaplayer_collision_count += 1
            if self._mediaplayer_collision_count > 30:
                self.media_stop(forced=True)
            raise MediaPlayerBusy(self._mediaplayer_now_playing,
                                  self._mediaplayer_collision_count)
        self._mediaplayer_collision_count = 0
        if hasattr(content, 'filepath'):
            content = content.filepath
        if not os.path.exists(content):
            self.log.warn("Could not find media to play at {filepath}",
                          filepath=content)
            return
        if duration:
            self._end_call = self.reactor.callLater(duration, self.media_stop)
        self._mediaplayer_now_playing = os.path.basename(content)

        player: MediaPlayerBase
        for player in self._players:
            if player.check_support(content):
                self.log.info("Showing content '{filename}' using <{player}>",
                              filename=os.path.basename(content),
                              player=player.__class__.__name__)
                self._current_player = player
                self._media_playing = player.play(content, **kwargs)
                break

        self._media_player_deferred = Deferred()
        return self._media_player_deferred

    def media_stop(self, forced=False):
        if not self._mediaplayer_now_playing:
            return
        self.log.info("Stopping Media : {0}".format(self._mediaplayer_now_playing))
        if self._mediaplayer_collision_count:
            self.log.info("End Offset by {0} collisions."
                          "".format(self._mediaplayer_collision_count))
        self._mediaplayer_collision_count = 0

        assert isinstance(self._current_player, MediaPlayerBase)
        self._current_player.stop()
        self._current_player = None
        self._media_playing = None

        if self._end_call and self._end_call.active():
            self._end_call.cancel()

        if self._mediaplayer_now_playing:
            self._mediaplayer_now_playing = None

        if self._media_player_deferred:
            self._media_player_deferred.callback(forced)
            self._media_player_deferred = None

    def stop(self):
        self.media_stop(forced=True)
        super(MediaPlayerCoreMixin, self).stop()
