import xbmc
from .discordIPC import DiscordIPC
import time

CLIENT_ID = '750797452453478629'

def run():
    monitor = xbmc.Monitor()
    player = xbmc.Player()
    discord = None
    startTime = -1
    gameStarted = False
    caption = ""

    while not monitor.abortRequested():
        if monitor.abortRequested():
            break

        if player.isPlayingGame():
            if not gameStarted:
                discord = DiscordIPC(CLIENT_ID)
                startTime = int(time.time())
                gameStarted = True

            new_caption = player.getCaption()
            if new_caption != caption:
                caption = new_caption
                data = player.getGameInfoTag()
                activity = {
                    'assets': {'large_image': 'kodi', 'large_text': 'Kodi'},
                    'state': data.getTitle(),
                    'details': caption,
                    'timestamps': {'start': startTime}
                }
                discord.update_activity(activity)
        else:
            if gameStarted:
                discord.close()
                startTime = -1
                gameStarted = False
                caption = ""

        monitor.waitForAbort(5)
