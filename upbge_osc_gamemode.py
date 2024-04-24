### This script is a simple study of how to use the pythonosc library to receive OSC messages in a BGE game.
### It requires an "Always" sensor with Pulse True Level activated in the controller of the object that will receive the OSC messages.
### The script will start an OSC server in a separate thread and will listen to messages on the "/move" address.

import bge
from bge import logic
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
import time
import queue

# -----------------------------------------------------
# Global variables and constants
# -----------------------------------------------------
ip = "127.0.0.1"                     # OSC server IP address of the UPBGE game
port = 9999                         # OSC server port

cont = logic.getCurrentController()  # Get the current game controller
scene = logic.getCurrentScene()      # Get the current game scene
objects = scene.objects              # Get all objects in the scene
cube = objects["Cube"]               # Get a reference to the "Cube" object
should_run = True                    # Flag to control the server loop    
q = queue.Queue()                    # Queue for communicating with the server thread

# -----------------------------------------------------
# Functions
# -----------------------------------------------------

def move(unused_addr, *args):
    """Handles OSC "/move" messages, moving the cube.

    Args:
        unused_addr (str): The OSC address (not used here).
        *args: A variable number of arguments representing the x, y, z movement values.
    """

    global cube  # Access the global cube object
    print(f"-> frame: {cube['frame']} --- moving cube with these vals: {args}")
    cube.position.x += args[0]
    cube.position.y += args[1]
    cube.position.z += args[2]

def quit(unused_addr, *args):
    """Handles OSC "/quit" messages, initiating the server shutdown.

    Args:
        unused_addr (str): The OSC address (not used here).
        *args: Additional arguments (not used here).
    """

    global should_run, q
    print(f"--- quit server / end game: {args}")
    print("threads running:")
    for thread in threading.enumerate():
        print(f"-- thread name: {thread.name}")

    print(f"should_run now will be false! / ending game")
    should_run = False  # Signal the server thread to stop
    quitthread = threading.Thread(target=shutdown_thread, args=(q,))
    quitthread.start()  # Start a thread to handle the clean shutdown

def server_thread(q):
    """Starts and runs the OSC server in a separate thread.

    Args:
        q (queue.Queue): A queue object for passing the server reference.
    """
    global ip, port
    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)  # Create the OSC server
    print("Serving on {}".format(server.server_address))
    q.put(server)  # Put the server reference on the queue

    # while should_run:  # Main server loop
    server.serve_forever()  # Handle incoming OSC requests

def shutdown_thread(q):
    """Shuts down the OSC server and ends the game.

    Args:
        q (queue.Queue): A queue object containing the server reference.
    """

    server = q.get()  # Retrieve the server object from the queue
    print("Shutting down server...")
    server.shutdown()      # Shut down the server
    time.sleep(0.5)
    print(' ... server shutdown!')
    print('running server_close...')
    server.server_close()  # Close the server cleanly
    print('... finished server_close!')
    time.sleep(0.5)
    print("Ending game")
    logic.endGame()  # End the Blender Game Engine

def main(cont):
    """Main game loop function, executed by the logic brick.
    """

    if cube['frame'] == 0:
        print("Starting server")
        thread = threading.Thread(target=server_thread, name="OSCserver", args=(q,))
        thread.start()

    cube['frame'] += 1  # Increment the frame counter

# -----------------------------------------------------
# OSC Setup
# -----------------------------------------------------
dispatcher = Dispatcher()
dispatcher.map("/move", move)  # Map OSC addresses to handler functions
dispatcher.map("/quit", quit)

# -----------------------------------------------------
# Start the game loop
# -----------------------------------------------------    
main(cont)
