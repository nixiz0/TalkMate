import pyaudio
import numpy as np
import os
import wave
import collections


def record_audio(filename="./speech_to_text/temp_audio/audio.wav", device_index=0, rate=44100, chunk=1024, threshold=500, pre_recording_buffer_length=2):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index=device_index)

    print(f"\nListen...")
    frames = collections.deque(maxlen=int(rate / chunk * pre_recording_buffer_length))  # buffer to store 2 seconds of audio
    recording_frames = []
    recording = False
    silence_count = 0
    while True:
        data = stream.read(chunk)
        rms = np.linalg.norm(np.frombuffer(data, dtype=np.int16)) / np.sqrt(len(data))
        frames.append(data)
        if rms >= threshold:
            if not recording:  # start recording
                recording = True
                recording_frames.extend(frames)  # add the buffered audio
            silence_count = 0
        elif recording and rms < threshold:
            silence_count += 1
            if silence_count > rate / chunk * 3:  # if 3 seconds of silence, stop recording
                break
        if recording:
            recording_frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Only create the file if there is audio data
    if recording_frames:
        print(f"Transcription in progress...")
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(recording_frames))
        wf.close()
        return True
    else:
        print(f"No audio detected.")
        return False