import numpy as np
import tifffile
from PIL import Image
import subprocess
import yaml, os, cv2, time
import boto3, botocore
import logging
import os
from datetime import datetime
import json

images = []

def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))

def tiffify(paths, foldername, name, note):
    arrays = []
    for p in paths:
        print("PATH IS: " + p)
        arr = np.array(Image.open(p))
        arrays.append(arr)
        print("DTYPE " + str(arr.dtype))
        print("SHAPE " + str(arr.shape))

    newpath = "C:/Users/somet/OneDrive/Documents/zstacks/tiffs/" + name+foldername + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    data = {
        "samplename":name,
        "note":note
    }
    
    with open("C:/Users/somet/OneDrive/Documents/zstacks/tiffs/" + name+foldername + "/" + name+foldername + '.json', "w") as write_file:
        json.dump(data, write_file)

    output_filename = "C:/Users/somet/OneDrive/Documents/zstacks/tiffs/" + name+foldername + "/" + name+foldername + '.tiff'
    s = np.stack(arrays,axis=0)
    tifffile.imwrite(output_filename, s)
    print(os.getcwd())

    s3 = boto3.client('s3', endpoint_url="https://s3.braingeneers.gi.ucsc.edu")
    try:
        response = s3.upload_file(output_filename, "streamscope", "zstacks/" + name+foldername + "/" + name+foldername + '.tiff')
        print(response)
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        print(e)

    jsonname = "C:/Users/somet/OneDrive/Documents/zstacks/tiffs/" + name+foldername + "/" + name+foldername + '.json'
    try:
        response = s3.upload_file(jsonname, "streamscope", "zstacks/" + name+foldername + "/" + name+foldername + '.json')
        print(response)
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        print(e)

def upbyx(x, mid):
    status = yaml.load(ticcmd('-s', '--full'), Loader=yaml.Loader)
    
    position = status['Current position']
    print("Current position is {}.".format(position))
    
    new_target = position+x
    print("Setting target position to {}.".format(new_target))
    ticcmd('--exit-safe-start', '--position', str(new_target), '-d', mid)
def downbyx(x, mid):
    status = yaml.load(ticcmd('-s', '--full'), Loader=yaml.Loader)
 
    position = status['Current position']
    print("Current position is {}.".format(position))
    
    new_target = position-x
    print("Setting target position to {}.".format(new_target))
    ticcmd('--exit-safe-start', '--position', str(new_target), '-d', mid)

def deenergize(mid):
    print("Deenergizing")
    ticcmd('--deenergize', '-d', mid)

def energize(mid):
    print("Energizing")
    ticcmd('--energize', '-d', mid)

#####################################################
import tkinter as tk
import re  # Import the regular expression module

def set_default_values():
    name_var.set("Cell Type Here")
    default_images_var.set(5)
    default_steps_var.set(100)
    default_id_var.set("00381252")

# Create the main window
root = tk.Tk()
root.title("ZStacker GUI")

# Create StringVar or IntVar variables for default values
name_var = tk.StringVar()
default_images_var = tk.IntVar()
default_steps_var = tk.IntVar()
default_id_var = tk.StringVar()
# Set default values
set_default_values()

# Function to validate the input
def validate_input_filename(P):
    # Define a regular expression pattern for a valid filename
    # You can customize this pattern based on your requirements
    pattern = r'^[a-zA-Z0-9_\-]*$'

    # Check if the input matches the pattern
    if re.match(pattern, P) is not None:
        return True  # Input is valid
    else:
        return False  # Input is invalid

def validate_numeric(P):
    # Check if the input is empty or consists of digits only
    return P == "" or P.isdigit()

def get_text():
    text_content = note_widget.get("1.0", "end-1c")  # Get the text content
    return text_content

def submit():
    name = name_entry.get()
    ips = images_per_stack_entry.get()
    spi = steps_per_image_entry.get()
    mid = motorid_entry.get() 
    print(f"Name: {name}")
    print(f"Images Per Stack: {ips}")
    print(f"Steps Per Image: {spi}")
    print(f"Stepper Motor ID {mid}")
    print(f"Additional Notes: {get_text()}")
    experimentname = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    newpath = "C:/Users/somet/OneDrive/Documents/zstacks/raw/" + name.strip()+experimentname.strip() + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for i in range(int(ips)):
        energize(mid)
        downbyx(int(spi), mid)
        time.sleep(2)
        deenergize(mid)
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        return_value, image = camera.read()
        if return_value:
                    writepath = "C:/Users/somet/OneDrive/Documents/zstacks/raw/" + name.strip()+experimentname.strip() + "/" + str(i) + ".png"
                    windowspath = "C:\\Users\\somet\\OneDrive\\Documents\\zstacks\\raw\\" + name.strip()+experimentname.strip() + "\\" + str(i) + ".png"
                    cv2.imwrite(writepath, image)
                    images.append(windowspath)
                    print("IMAGE SAVED TO: " + writepath)
        del(camera)

    note = get_text()
    print("IMAGES", images)
    tiffify(images, experimentname,name,note)

# Create a label and an Entry widget with input validation
name_label = tk.Label(root, text="Experiment Name")
name_label.pack()

validate_filename = root.register(validate_input_filename)
name_entry = tk.Entry(root, textvariable=name_var, validate="key", validatecommand=(validate_filename, "%P"))
name_entry.pack()

# Create a label and an Entry widget with input validation
images_per_stack_label = tk.Label(root, text="Images Per Stack")
images_per_stack_label.pack()

validate_numeric = root.register(validate_numeric)
images_per_stack_entry = tk.Entry(root, textvariable=default_images_var, validate="key", validatecommand=(validate_numeric, "%P"))
images_per_stack_entry.pack()

# Create a label and an Entry widget with input validation
steps_per_image_label = tk.Label(root, text="Steps Per Image")
steps_per_image_label.pack()

steps_per_image_entry = tk.Entry(root, textvariable=default_steps_var, validate="key", validatecommand=(validate_numeric, "%P"))
steps_per_image_entry.pack()

# Create a label and an Entry widget with input validation
motorid_label = tk.Label(root, text="Stepper Driver ID")
motorid_label.pack()

motorid_entry = tk.Entry(root, textvariable=default_id_var, validate="key", validatecommand=(validate_numeric, "%P"))
motorid_entry .pack()

note_widget_label = tk.Label(root, text="Additional Notes")
note_widget_label.pack()

note_widget = tk.Text(root, wrap=tk.WORD, height=5, width=20)
note_widget.pack()

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Start the GUI event loop
root.mainloop()