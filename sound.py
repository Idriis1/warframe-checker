import pygame.mixer

# Initialize pygame mixer for sound effects
pygame.mixer.init()
global sound_enabled
sound_enabled = True

def play_sound():
    sound_file = "wf.mp3"
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")

def toggle_sound(x):
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        x.config(text="Sound: ON")
    else:
        x.config(text="Sound: OFF")
