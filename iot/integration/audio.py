import wave
from typing import List

import pyaudio
from loguru import logger

from iot.utils import process_bar


class AudioClient:

    @staticmethod
    def record(format=pyaudio.paInt16,
               channels: int = 1,
               rate: int = 16000,
               input: bool = True,
               frames_per_buffer: int = 1024,
               time: int = 5) -> List[bytes]:
        audio = pyaudio.PyAudio()
        ret_value: List[bytes] = []
        logger.info("Recording starts")
        stream = audio.open(format=format,
                            channels=channels,
                            rate=rate,
                            input=input,
                            frames_per_buffer=frames_per_buffer)
        for i in range(0, int(rate / frames_per_buffer * time)):
            process_bar(i, int(rate / frames_per_buffer * time), "⚪ Recording")
            data: bytes = stream.read(frames_per_buffer)
            ret_value.append(data)
        print('\n')
        logger.info("Recording ends")
        stream.stop_stream()
        audio.terminate()
        return ret_value

    @staticmethod
    def save(data: List[bytes],
             path: str,
             format=pyaudio.paInt16,
             channels: int = 1,
             rate: int = 16000) -> None:
        audio = pyaudio.PyAudio()
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(data))
            logger.info("wave saved")

    @staticmethod
    def play(path: str, frames_per_buffer: int = 1024):
        with wave.open(path, 'rb') as wf:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)
            data = wf.readframes(frames_per_buffer)
            logger.info("playing starts")
            while data:
                stream.write(data)
                data = wf.readframes(frames_per_buffer)
            stream.stop_stream()
            stream.close()
            logger.info("playing ends")
            audio.terminate()

