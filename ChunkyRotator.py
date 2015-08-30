import json
import argparse
import os

# Argument parser
parser = argparse.ArgumentParser(description='Generate a 360 degrees video of your build')
parser.add_argument(
  '-d', '--dir', type=str, help='Scene directory', required=True)
parser.add_argument(
  '-s', '--scene', type=str, help='Scene name', required=True)

args = parser.parse_args()
dir = args.dir
scene = args.scene

# Keeps track of how much renders have been made
iteration = 0

# To maintain compatibility on both Unix and Windows we
# use the OS specific path separator
sep = os.sep

# Stop program if ChunkyLauncher.jar does not exist
if not os.path.isfile("ChunkyLauncher.jar"): 
  print("ChunkyLauncher.jar could not be found. Put ChunkyLauncher.jar in the same folder as this program!")
  raise SystemExit(0)

# Create separate folder for all of the images
imagepath = dir + sep + "ChunkyRotate-" + scene
if not os.path.exists(imagepath): os.makedirs(imagepath)


# Starts Chunky to render the scene
def render():
  global iteration
  
  # Only render if it doesn't exist yet, this allows you to stop
  # and start the program without having to render everything again
  if not os.path.isfile(imagepath + sep + scene + "-" + str(iteration) + ".png"): 
    os.system("java -jar ChunkyLauncher.jar -scene-dir " + dir + " -render " + scene)
    
    # Remove the dump file and move image in separate directory
    os.remove(dir + sep + scene + ".dump")
    os.rename(dir + sep + scene + "-" +str(spp) + ".png",
    imagepath + sep + scene + "-" + str(iteration) + ".png")
  
  iteration += 1


# Main loop, stops when all 360 frames are rendered
while iteration < 360:
  # Open the scene file to alter the yaw
  with open(str(dir + sep + scene + ".json"), 'r') as f:
    data = json.load(f)
    data['camera']['orientation']['yaw'] = iteration * 0.01745329251
    spp = data['sppTarget']
    f.close()
  
  # Save the scene file with altered yaw  
  with open(str(dir + sep + scene + ".json"), 'w') as f:
    f.write(json.dumps(data))
    f.close()
    
  render()
  print("Render: " + str(iteration) + " finished. " + str(360-iteration) + " renders left.")
  
print("ChunkyRotate finished. Output can be found in: " + imagepath)
