from random import randrange
import winsound
from ctypes import windll as h5
from os import listdir
from pathlib import Path

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import BaseAgent


class Jukebox:
    def __init__(self, agent: BaseAgent, goal_music: bool = True) -> None:
        self.agent: BaseAgent = agent
        self.score = 0
        self.last_team_touch = -1
        self.music_files = []
        self.goal_music = goal_music
        self.demolitions = 0

    def play_sound(self, file_name: str, music: bool = False):
        try:
            path = f"{Path(__file__).absolute().parent.parent}\\{'music' if music else 'audio'}\\{file_name}"
            winsound.PlaySound(path, winsound.SND_FILENAME)
        except Exception as e:
            print(e)

    def update(self, packet: GameTickPacket) -> None:
        if not self.goal_music:
            return

        if packet.game_ball.latest_touch.team == self.agent.team:
            self.last_team_touch = packet.game_ball.latest_touch.player_index
        if packet.teams[self.agent.team].score > self.score:
            self.score = packet.teams[self.agent.team].score
            if self.last_team_touch == self.agent.index:
                if len(self.music_files) < 1:
                    self.music_files = listdir(
                        f"{Path(__file__).absolute().parent.parent}\\music"
                    )
                randomness = randrange(len(self.music_files))
                self.play_sound(self.music_files[randomness], music=True)
                print("Give me a high five!")
                h5.WINMM.mciSendStringW("set cdaudio door open", None, 0, None)
                self.music_files.pop(randomness)
