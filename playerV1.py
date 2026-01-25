import vlc
from gpiozero import Button
import os
import time

# GPIO pin configuration using GPIO Zero
start_button = Button(17, pull_up=True)
stop_button = Button(18, pull_up=True)
pause_button = Button(27, pull_up=True)
next_button = Button(22, pull_up=True)
back_button = Button(23, pull_up=True)
shutdown_button = Button(24, pull_up=True)

# Media playlist
PLAYLIST = [
    "/home/pi/videosTest/1m30s.mp4",
    "/home/pi/videosTest/2m.mp4",
    "/home/pi/videosTest/3m.mp4",
    "/home/pi/videosTest/7m.mp4",
]

# VLC player setup
instance = vlc.Instance()
player = instance.media_list_player_new()
media_list = instance.media_list_new(PLAYLIST)
player.set_media_list(media_list)

# Global state variables
current_index = 0
playlist_length = len(PLAYLIST)
is_playing = False


def play_video(index):
    """Play video at the given index."""
    global is_playing, current_index
    if 0 <= index < playlist_length:
        current_index = index
        is_playing = True
        media = instance.media_new(PLAYLIST[current_index])
        player.get_media_player().set_media(media)
        player.play()
        print(f"Playing: {PLAYLIST[current_index]}")


def play_next_video():
    """Play the next video in the playlist."""
    global current_index, is_playing
    if current_index + 1 < playlist_length:
        current_index += 1
        play_video(current_index)
    else:
        print("End of playlist. Returning to the first video.")
        current_index = 0
        is_playing = False


def play_previous_video():
    """Play the previous video in the playlist."""
    global current_index, is_playing
    if current_index > 0:
        current_index -= 1
        play_video(current_index)
    else:
        print("Already at the first video.")
        play_video(0)


def start_callback():
    """Callback for Start button."""
    global is_playing
    if not is_playing:
        print("Starting playback.")
        play_video(current_index)


def stop_callback():
    """Callback for Stop button."""
    global is_playing
    print("Stopping playback.")
    player.stop()
    is_playing = False


def pause_callback():
    """Callback for Pause button."""
    if player.is_playing():
        player.pause()
        print("Playback paused.")
    else:
        player.play()
        print("Playback resumed.")


def next_callback():
    """Callback for Next button."""
    print("Next button pressed.")
    play_next_video()


def back_callback():
    """Callback for Back button."""
    print("Back button pressed.")
    play_previous_video()


def shutdown_callback():
    """Callback for Shutdown button."""
    print("Shutdown button pressed. Shutting down Raspberry Pi.")
    os.system("sudo shutdown now")


def main():
    """Main function to set up button event handlers."""
    # Attach button press callbacks
    start_button.when_pressed = start_callback
    stop_button.when_pressed = stop_callback
    pause_button.when_pressed = pause_callback
    next_button.when_pressed = next_callback
    back_button.when_pressed = back_callback
    shutdown_button.when_pressed = shutdown_callback

    print("Ready. Press the start button to begin.")
    try:
        while True:
            # Monitor playback status
            if is_playing and not player.is_playing():
                print("Video ended. Waiting for next button.")
                is_playing = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting program.")
        player.stop()


if __name__ == "__main__":
    main()