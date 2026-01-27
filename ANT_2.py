#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
import pandas as pd
from datetime import datetime

#%%
# --- MONITOR CALIBRATION ---
# Update these values based on your actual laboratory setup
MON_WIDTH = 70      # Physical width of monitor in cm
MON_DISTANCE = 120   # Distance from participant eyes to monitor in cm
MON_SIZE = [1920, 1080]  # Resolution in pixels

# --- STIMULUS PARAMETERS (in Degrees of Visual Angle) ---
FIXATION_HEIGHT = 0.5
TARGET_SIZE = (1.5, 0.5)  # Width, Height in deg
WARNING_SIZE = (0.5, 0.5)

#%%
input_subID = 0
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID)}
expInfo['runID'] = ['1', '2', '3']
expInfo['sessionID'] = ['Baseline', 'Repeat_Baseline', 'T3', 'T6', 'T9', 'T12']

dlg = gui.DlgFromDict(dictionary=expInfo, title='My Experiment')
if dlg.OK == False:
    core.quit()

used_keyList = ['s', 'escape', 'f', 'j']
trigger_keyList = ['s']
correct_responses = {"left": "f", "right": "j"}

# --- DIRECTORY AND FILENAME SETUP ---
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Ensure values are strings before zfill
run_str = str(expInfo['runID']).zfill(2)
sub_str = str(expInfo['subID']).zfill(3)
session_str = str(expInfo['sessionID'])
experiment_time = datetime.now().strftime("%Y-%m-%d_%H%M%S") # Removed colons

resultFile_name = f"sub-{sub_str}_ses-{session_str}_run-{run_str}_time-{experiment_time}"
resultFile_path = os.path.join(results_dir, resultFile_name)

thisExp = data.ExperimentHandler(
    name=expName, version='0.1',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='',
    savePickle=True, saveWideText=True
)

logFile = logging.LogFile(resultFile_path + ".log", level=logging.EXP)
logging.console.setLevel(logging.ERROR)

#%%
# --- WINDOW INITIALIZATION ---
# Using the Monitor object to handle deg-to-pixel math
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(
    monitor=my_monitor,
    fullscr=True,
    screen=0, 
    allowGUI=True, 
    color="white",
    units='deg'  # Changed from 'norm' to 'deg'
)

win.mouseVisible = False

# --- STIMULI INITIALIZATION ---
# Using degrees ensures the "+" and images look the same on any screen
fixation_text = visual.TextStim(
    win, text="+", height=FIXATION_HEIGHT,
    color='black', pos=(0, 0)
)

warning_image_1 = visual.ImageStim(
    win, size=WARNING_SIZE, opacity=1
)

target_image = visual.ImageStim(
    win, size=TARGET_SIZE, opacity=1
)

# Intro/Goodbye components (may need width in deg for wrapWidth)
win_width_deg = win.size[0] # Note: in 'deg' units, win.size returns deg if available
intro_text = init_intro(win, 20) # 20 degrees is a safe wrap width
goodbye_text = init_goodbye(win, 20)

rt_list = []
acc_list = []
trialClock = core.Clock()

#%%
# --- EXECUTION ---
run_intro(win, intro_text, trigger_keyList)

# Execute behavioral task
mean_rt, mean_acc = run_behav(
    win, thisExp, fixation_text, warning_image_1, target_image, 
    trialClock, rt_list, acc_list, results_dir, resultFile_name, 
    used_keyList, correct_responses
)

run_goodbye(win, goodbye_text)

# --- DATA PROCESSING ---
masked_rt_list = np.ma.masked_equal(rt_list, None)
masked_acc_list = np.ma.masked_equal(acc_list, None)

if len(masked_rt_list.compressed()) > 0:
    mean_rt = round(np.mean(masked_rt_list) * 1000)
    mean_acc = round(np.mean(masked_acc_list) * 100)
    print(f"Your mean reaction time is: {mean_rt} ms")
    print(f"Your mean ACC is: {mean_acc} %")

# --- CLEANUP ---
thisExp.saveAsWideText(resultFile_path + ".csv")
thisExp.saveAsPickle(resultFile_path)
logging.flush()
thisExp.abort()
win.close()
core.quit()
