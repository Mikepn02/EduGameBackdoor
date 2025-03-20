# Installation Guide

## Prerequisites
To run **SpaceInvadersEdu**, ensure you have the following installed on your system:

- **Python 3.x**: Download and install from [python.org](https://www.python.org/downloads/).
- **Pygame**: The game requires Pygame for rendering graphics and handling user input.
- **Netcat**: Required for the networking feature (e.g., `nc` on Linux, available via `sudo apt install netcat` on Kali Linux).
- **Assets**:
  - `plane.png`: Image for the player ship.
  - `alien.png`: Image for the enemy aliens.

## Installation Steps

### 1. Clone the Repository
Clone the project to your local machine:
```bash
git clone https://github.com/Mikepn02/EduGameBackdoor.git
cd  EduGameBackdoor
```


### 2. Install Dependencies

```python
    pip install pygame
```
### 3. Verify Assets
Ensure the following image files are in the project directory:

***plane.png***
**alien.png***

## NOTE: If these files are missing, the game will use basic shapes (a triangle for the player and a circle for enemies) as a fallback.


## Running the Game

### 1. Start the Local Listener
The game includes a networking feature that connects to a local server for testing purposes. Open a terminal and start a listener:
```bash
nc -lvp 8888
```

### 2. Launch the Game
In another terminal, navigate to the project directory and run the game:

```python
python3 game.py
```

### 3. Acknowledge the Notice Screen
Upon launching, a notice screen will appear:

It informs you that the game saves settings for auto-restart and connects to a local server for testing.
It includes an ethical note about responsible use.
Click Yes to proceed or No to exit.

### 4. Play the Game

***Controls:***

**Left Arrow**: Move the player ship left.
**Right Arrow**: Move the player ship right.
**Spacebar**: Shoot bullets to destroy enemies.
**Quit**: Close the window to exit the game.

**Objective:**
Shoot down enemy aliens to increase your score.
Avoid letting enemies reach the bottom of the screen or collide with your ship.

**Game Over:**
The game ends if an enemy reaches the bottom or hits the player.
Your final score will be displayed.


### Using the Networking Feature
The game connects to **127.0.0.1:8888** to simulate network communication.
In the listener terminal **(nc -l 8888)**, you can send commands to test file system interactions:
**ls**: List files in the current directory.
**cd** ..: Change to the parent directory.
**exit**: Close the connection.


### 5. Cleanup
The game saves settings to auto-restart on system boot. To remove these settings:

```bash
python3 space_invaders_cleanup.py
```

This script will remove the auto-restart settings from your system:

**Windows**: Removes the Registry entry.
**Linux**: Deletes the .desktop file from **~/.config/autostart**.
**macOS**: Removes the LaunchAgent from **~/Library/LaunchAgents**.
