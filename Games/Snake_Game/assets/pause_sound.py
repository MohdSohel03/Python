from pydub import AudioSegment
from pydub.generators import Sine
import os

# Function to create a sine wave beep sound
def create_pause_sound(frequency=500, duration_ms=300):
    # Create a sine wave tone at the given frequency and duration
    sound = Sine(frequency).to_audio_segment(duration=duration_ms)
    sound = sound.fade_in(50).fade_out(50)  # Optional: add smooth fade-in and fade-out
    return sound

# Function to save the generated sound to a .wav file
def save_sound(sound, filename):
    # Ensure the target directory exists, create it if it doesn't
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    sound.export(filename, format="wav")  # Export the sound as a .wav file

# Generate a pause beep sound (500Hz, 300ms duration)
pause_sound = create_pause_sound(frequency=500, duration_ms=300)

# Specify the assets directory to save the file
asset_dir = "assets"  # Directory for your sound assets
sound_file = os.path.join(asset_dir, "pause_sound.wav")  # File name with .wav extension

# Save the generated sound in .wav format
save_sound(pause_sound, sound_file)

print(f"Pause sound saved as {sound_file}")
