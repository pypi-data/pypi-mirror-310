Spectrogram Recorder Library
A Python library for recording audio, generating spectrograms, and managing session data. This library helps you capture audio, visualize it as spectrograms, save those images, and organize them into session folders. It also offers utilities to manage and delete session folders and calculate their sizes.

Features
Audio Recording: Record audio data using the sounddevice library.
Spectrogram Generation: Plot spectrograms from recorded audio.
Session Management: Create and manage folders for each recording session.
Cross-platform Support: Compatible with Windows, macOS, and Linux.
Directory Management: Automatically selects default directories based on the OS.
File Size Calculation: Calculate and print the size of directories and session folders.

Dependencies:
    numpy
    sounddevice
    matplotlib
    shutil (comes with Python)
    platform (comes with Python)
Functions
```python
get_default_directory()
```
Returns the default directory for saving spectrograms based on the current operating system.

Example:
```python
default_directory = get_default_directory()
print(default_directory)
create_session_folder(directory=None)
```
Creates a new session folder inside the provided directory (or default directory if None). The folder is named with a unique session number.

Parameters:
directory: Optional; path to the directory where session folders will be created.
Returns:
The path to the newly created session folder.
Example:
```python
session_folder = create_session_folder()
print(f"Session created at {session_folder}")
get_latest_session_folder(directory=None)
Finds the session folder with the highest number and returns its path.
```

Parameters:
directory: Optional; path to the directory where session folders are stored.
Returns:
The path to the latest session folder, or None if no sessions exist.
Example:
```python
latest_session = get_latest_session_folder()
print(f"Latest session folder: {latest_session}")
```

```python
plot_spectrogram(audio_data, rate=44100)
```
Generates and plots a spectrogram for the given audio data.

Parameters:
audio_data: Audio data to generate the spectrogram.
rate: Sampling rate (default is 44100).
Returns:
fig: Matplotlib figure object.
ax: Matplotlib axis object.
Example:
```python
audio_data = np.random.randn(44100 * 3)  # Simulate 3 seconds of audio
fig, ax = plot_spectrogram(audio_data)
plt.show()
save_spectrogram(fig, session_folder)
```
Saves the spectrogram figure to the session folder with a timestamped filename.

Parameters:
fig: The Matplotlib figure object to save.
session_folder: The path to the session folder where the figure will be saved.
Returns:
The filename of the saved spectrogram.
Example:
```python
save_spectrogram(fig, session_folder)
record_audio(duration=3, rate=44100, channels=1)
Records audio for a specified duration and returns the audio data.
```

Parameters:
duration: Duration of the recording in seconds (default is 3 seconds).
rate: Sampling rate (default is 44100).
channels: Number of audio channels (default is 1).
Returns:
audio_data: A numpy array containing the recorded audio data.
Example:
```python
Копировать код
audio_data = record_audio()
delete_latest_session_folder(directory=None)
Deletes the latest session folder.
```

Parameters:
directory: Optional; path to the directory where session folders are stored.
Example:
```python
delete_latest_session_folder()
```

```python
get_folder_size(directory=None)
Calculates the total size of a directory by summing the sizes of all files inside it.
```

Parameters:
directory: Optional; path to the directory whose size will be calculated.
Returns:
Total size of the directory in bytes.
Example:
```python
folder_size = get_folder_size(session_folder)
print(f"Folder size: {folder_size / (1024 * 1024):.2f} MB")
print_folder_size(directory=None)
Prints the total size of the latest session folder.
```

Parameters:
directory: Optional; path to the directory where session folders are stored.
Example:
```python
print_folder_size()
Platform Support
The library automatically selects the default directory based on your operating system:

Windows: C:\Users\<username>\SOUNDS\spectrograms
macOS: /Users/<username>/SOUNDS/spectrograms
Linux: /home/<username>/SOUNDS/spectrograms
```

Usage Example:
```python
# Record audio
audio_data = record_audio(duration=5)

# Create a new session folder
session_folder = create_session_folder()

# Generate a spectrogram for the recorded audio
fig, ax = plot_spectrogram(audio_data)

# Save the spectrogram image to the session folder
save_spectrogram(fig, session_folder)

# Print the size of the session folder
print_folder_size(session_folder)
```

License
This project is licensed under the MIT License - see the LICENSE file for details.