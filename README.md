# UPBGE (0.36.1) - control game objects using OSC messages (simple example)
https://www.youtube.com/watch?v=-7z1yCquJ2Q

[<img src="https://img.youtube.com/vi/-7z1yCquJ2Q/maxresdefault.jpg" width="90%">](https://youtu.be/-7z1yCquJ2Q)

1. Download this repository:
```
git clone https://github.com/zepadovani/upbge_osc_gamemode
```

2. Download pythonosc to the same folder of the blend file, so that the standalone app can find the module there

```
cd upbge_osc_gamemode
pip install --target ./ python-osc
```

3. Run the game (press 'p' to play the embedded game or select the standalone version in render options)

4. Run the SuperCollider code to send messages and move the cube

5. Run the /quit message to end the server, close the port and exit the game
