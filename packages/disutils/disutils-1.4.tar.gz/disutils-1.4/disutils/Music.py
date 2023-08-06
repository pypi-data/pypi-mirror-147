import aiohttp
import re

try:
    import youtube_dl
    import discord

    has_voice = True
except ImportError:
    has_voice = False

if has_voice:
    youtube_dl.utils.bug_reports_message = lambda: ""
    ytdl = youtube_dl.YoutubeDL(
        {
            "format": "bestaudio/best",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "source_address": "0.0.0.0",
        }
    )


class EmptyQueue(Exception):
    """Cannot skip because queue is empty"""


class NotConnectedToVoice(Exception):
    """Cannot create the player because bot is not connected to voice"""


class NotPlaying(Exception):
    """Cannot <do something> because nothing is being played"""


class Song(object):
    def __init__(
        self,
        source,
        url,
        title,
        description,
        likes,
        views,
        duration,
        thumbnail,
        channel,
        channel_url,
        is_looping,
    ):
        self.source = source
        self.url = url
        self.title = title
        self.description = description
        self.likes = likes
        self.views = views
        self.name = title
        self.duration = duration
        self.thumbnail = thumbnail
        self.channel = channel
        self.channel_url = channel_url
        self.is_looping = is_looping


async def ytbettersearch(query):
    """This opens youtube.com and searches for the query, then returns the first result"""
    url = f"https://www.youtube.com/results?search_query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
    regex = r"(?<=watch\?v=)\w+"
    v = re.search(regex, html).group()
    url = f"https://www.youtube.com/?v={v}"
    return url


def is_url(url):
    """This checks if url is a url or not"""
    if re.match(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        url,
    ):
        return True
    else:
        return False


async def get_video_data(self, query, bettersearch, loop) -> Song:
    """This gets the video data from youtube.com and returns it as a Song object"""
    if not has_voice:
        raise RuntimeError("disutils[voice] install needed in order to use voice")

    if not is_url(query) and not bettersearch:
        ytdl_ = youtube_dl.YoutubeDL(
            {
                "format": "bestaudio/best",
                "restrictfilenames": True,
                "noplaylist": True,
                "nocheckcertificate": True,
                "ignoreerrors": True,
                "logtostderr": False,
                "quiet": True,
                "no_warnings": True,
                "default_search": "auto",
                "source_address": "0.0.0.0",
            }
        )
        data = await loop.run_in_executor(
            None, lambda: ytdl_.extract_info(query, download=False)
        )
        try:
            data = data["entries"][0]
        except KeyError or TypeError:
            pass
        del ytdl_
    else:
        if not is_url(query) and bettersearch:
            url = await ytbettersearch(query)
        elif is_url(query):
            url = query
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=False)
        )

    return Song(
        data["url"],
        "https://www.youtube.com/watch?v=" + data["id"],
        data["title"],
        data["description"],
        data["like_count"],
        data["view_count"],
        data["duration"],
        data["thumbnail"],
        data["uploader"],
        data["uploader_url"],
        False,
    )


# TODO: Rewrite this whole shit
def check_queue(ctx, opts, music, after, loop):
    if not has_voice:
        raise RuntimeError("disutils[voice] install needed in order to use voice")
    try:
        queue = music.get_player(ctx).song_queue
    except NotConnectedToVoice:
        return
    try:
        song = queue[0]
    except IndexError:
        return
    if not song.is_looping:
        try:
            queue.pop(0)
        except IndexError:
            return
        if len(queue) > 0:
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(queue[0].source, **opts)
            )
            ctx.voice_client.play(
                source,
                after=lambda error: after(ctx, opts, music, after, loop),
            )
            song = queue[0]
    else:
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(queue[0].source, **opts)
        )
        ctx.voice_client.play(
            source, after=lambda error: after(ctx, opts, music, after, loop)
        )
        song = queue[0]


class Music(object):
    def __init__(self):
        if not has_voice:
            raise RuntimeError("disutils[voice] install needed in order to use voice")
        self.players = []  # List of MusicPlayers

    def create_player(self, ctx, **kwargs):
        if not ctx.voice_client:
            raise NotConnectedToVoice(
                "Cannot create the player because bot is not connected to voice"
            )
        player = MusicPlayer(ctx, self, **kwargs)
        self.players.append(player)
        return player

    def get_player(self, ctx):
        """This gets the player from the ctx or creates a new one if there is none in that context"""
        for player in self.players:
            if player.voice_client.channel == ctx.voice_client.channel:
                return player
        return self.create_player(ctx)
        # for player in self.players:
        #     if (
        #         and player.ctx.guild.id == guild
        #         and player.voice.channel.id == channel
        #     ):
        #         return player
        #     elif not guild and channel and player.voice.channel.id == channel:
        #         return player
        #     elif not channel and guild and player.ctx.guild.id == guild:
        #         return player
        # else:
        #     return None


class MusicPlayer(object):
    def __init__(self, ctx, music):
        if not has_voice:
            raise RuntimeError("disutils[voice] install needed in order to use voice")
        self.ctx = ctx
        self.voice_client = ctx.voice_client
        self.loop = ctx.bot.loop
        self.bot = ctx.bot
        self.music = music
        self.song_queue = []
        self.after_func = check_queue
        self.ffmpeg_options = {
            "options": "-vn -loglevel quiet -hide_banner -nostats",
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0 -nostdin",
        }

    def disable(self):
        self.music.players.remove(self)

    # TODO: Rewrite the event stuff using discords builtin events (bot.dispatch)

    async def queue(self, query, bettersearch=True):
        song = await get_video_data(self, query, bettersearch, self.loop)
        self.song_queue.append(song)
        self.bot.dispatch("disutils_music_queue", self.ctx, song)
        return song

    async def play(self):
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(self.song_queue[0].source, **self.ffmpeg_options)
        )
        self.voice_client.play(
            source,
            after=lambda error: self.after_func(
                self.ctx,
                self.ffmpeg_options,
                self.music,
                self.after_func,
                self.loop,
            ),
        )
        song = self.song_queue[0]
        self.bot.dispatch("disutils_music_play", self.ctx, song)
        return song

    async def skip(self, force=False):
        if len(self.song_queue) == 0:
            raise NotPlaying("Cannot loop because nothing is being played")
        elif not len(self.song_queue) > 1 and not force:
            raise EmptyQueue("Cannot skip because queue is empty")
        else:
            old = self.song_queue[0]
            old.is_looping = (
                False if old.is_looping else False
            )  # WTF ITS ALWAYS FALSE ! FIX THIS LATER TODO
            self.voice_client.stop()
            try:
                new = self.song_queue[1]
                self.bot.dispatch("disutils_music_skip", self.ctx, old, new)
                return (old, new)
            except IndexError:
                self.bot.dispatch("disutils_music_skip", self.ctx, old)
                return old

    async def stop(self):
        try:
            self.song_queue = []
            self.voice_client.stop()
            self.music.players.remove(self)
        except:
            raise NotPlaying("Cannot loop because nothing is being played")
        self.bot.dispatch("disutils_music_stop", self.ctx)

    async def pause(self):
        try:
            self.voice_client.pause()
            song = self.song_queue[0]
        except:
            raise NotPlaying("Cannot pause because nothing is being played")
        self.bot.dispatch("disutils_music_pause", self.ctx, song)
        return song

    async def resume(self):
        try:
            self.voice_client.resume()
            song = self.song_queue[0]
        except:
            raise NotPlaying("Cannot resume because nothing is being played")
        self.bot.dispatch("disutils_music_resume", self.ctx, song)
        return song

    def current_queue(self):
        return self.song_queue

    def now_playing(self):
        try:
            return self.song_queue[0]
        except:
            return None

    async def toggle_song_loop(self):
        try:
            song = self.song_queue[0]
        except:
            raise NotPlaying("Cannot loop because nothing is being played")
        if not song.is_looping:
            song.is_looping = True
        else:
            song.is_looping = False
        self.bot.dispatch("disutils_music_toggle_loop", self.ctx, song)
        return song

    async def change_volume(self, vol):
        self.voice_client.source.volume = vol
        try:
            song = self.song_queue[0]
        except:
            raise NotPlaying("Cannot loop because nothing is being played")
        self.bot.dispatch("disutils_music_volume_change", self.ctx, song, vol)
        return (song, vol)

    async def remove_from_queue(self, index):
        if index == 0:
            try:
                song = self.song_queue[0]
            except:
                raise NotPlaying("Cannot loop because nothing is being played")
            await self.skip(force=True)
            return song
        song = self.song_queue[index]
        self.song_queue.pop(index)
        self.bot.dispatch("disutils_music_remove_from_queue", self.ctx, song)
        return song

    def delete(self):
        self.music.players.remove(self)
