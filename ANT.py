#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
import pandas as pd
from datetime import datetime

#%%
# --- MONITOR CALIBRATION (Adjust these for your specific lab setup) ---
MON_WIDTH = 70       # Physical width of monitor in cm
MON_DISTANCE = 120    # Distance from participant eyes to monitor in cm
MON_SIZE = [1920, 1080]  # Pixel resolution

# --- STIMULUS PARAMETERS (Degrees of Visual Angle) ---
# These values are now independent of your screen resolution
FIXATION_HEIGHT = 1.0  
TARGET_SIZE = (5.0, 1.2)   # The arrow block size in degrees
WARNING_SIZE = (1.0, 1.0)  # The star size in degrees
INSTRUCTION_HEIGHT = 0.8   # Font size for instructions

#%%
input_subID = 0
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID)}
expInfo['runID'] = ['1', '2', '3']
expInfo['sessionID'] = ['Baseline', 'Repeat_Baseline', 'T3', 'T6', 'T9', 'T12']

dlg = gui.DlgFromDict(dictionary=expInfo, title='Attention Network Test')
if dlg.OK == False:
    core.quit()

used_keyList = ['s', 'escape', 'f', 'j']
trigger_keyList = ['s']
correct_responses = {"left": "f", "right": "j"}

# --- DIRECTORY AND FILENAME SETUP ---
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Data formatting for filename safety
run_str = str(expInfo['runID']).zfill(2)
sub_str = str(expInfo['subID']).zfill(3)
session_str = str(expInfo['sessionID'])
experiment_time = datetime.now().strftime("%Y-%m-%d_%H%M%S") 

resultFile_name = f"sub-{sub_str}_ses-{session_str}_run-{run_str}_{experiment_time}"
resultFile_path = os.path.join(results_dir, resultFile_name)

thisExp = data.ExperimentHandler(
    name=expName, version='1.0',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='',
    savePickle=True, saveWideText=True
)

#%%
# --- WINDOW INITIALIZATION ---
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(
    monitor=my_monitor,
    fullscr=True,
    screen=0, 
    allowGUI=True, 
    color="white",
    units='deg'  # Using degrees of visual angle for all stimuli
)

win.mouseVisible = False

# --- STIMULI INITIALIZATION ---
# These are passed into the behavioral loop
fixation_text = visual.TextStim(
    win, text="+", height=FIXATION_HEIGHT,
    color='black', pos=(0, 0), font='Arial'
)

warning_image_1 = visual.ImageStim(
    win, size=WARNING_SIZE, opacity=1
)

target_image = visual.ImageStim(
    win, size=TARGET_SIZE, opacity=1
)

# Initialize instructions using updated tools.py logic
# win.size[0] in 'deg' is the horizontal field of view
intro_text = init_intro(win, win.size[0]) 
goodbye_text = init_goodbye(win, win.size[0])

rt_list = []
acc_list = []
trialClock = core.Clock()

#%%
# --- EXECUTION ---

# 1. Instructions
run_intro(win, intro_text, trigger_keyList)

# 2. Main Task Loop
# The function name in your tools.py is 'run_behav'
mean_rt, mean_acc = run_behav(
    win, thisExp, fixation_text, warning_image_1, target_image, 
    trialClock, rt_list, acc_list, results_dir, resultFile_name, 
    used_keyList, correct_responses
)

# 3. Goodbye
run_goodbye(win, goodbye_text)

# --- FINAL DATA SAVING ---
masked_rt_list = np.ma.masked_equal(rt_list, None)
masked_acc_list = np.ma.masked_equal(acc_list, None)

if len(masked_rt_list.compressed()) > 0:
    m_rt = round(np.mean(masked_rt_list) * 1000)
    m_acc = round(np.mean(masked_acc_list) * 100)
    print(f"Mean RT: {m_rt}ms | Mean ACC: {m_acc}%")

thisExp.saveAsWideText(resultFile_path + ".csv")
logging.flush()
thisExp.abort()
win.close()
core.quit()
