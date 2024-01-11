import sys
sys.path.append(".")

from voice_input_core.AudioRecorder import AudioRecorder

recorder = AudioRecorder()

print("press Enter to start recording")
input()

recorder.start()
print("start recording")

print("press Enter to stop recording")
input()

recorder.stop()
print("stop recording")

recorder.save('./test/test_audio_recorder.wav')