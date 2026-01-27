#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
import pandas as pd
from datetime import datetime

#%%
# --- MONITOR CALIBRATION (CRITICAL) ---
MON_WIDTH = 70      
MON_DISTANCE = 120   
MON_SIZE = [1920, 1080]  

# --- STIMULUS PARAMETERS (Increased for visibility) ---
# 1.0 to 2.0 degrees is standard for text/fixation in these units
FIXATION_HEIGHT = 1.2  
# Arrows usually need to be wider to show the flankers (e.g., << < <<)
# If your target_image contains 5 arrows, it needs a wider aspect ratio
TARGET_SIZE = (5.0, 1.5)  
WARNING_SIZE = (1.5, 1.5)
TEXT_SIZE_UI = 1.0 # For instructions

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

# --- FILENAME SETUP ---
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

run_str = str(expInfo['runID']).zfill(2)
sub_str = str(expInfo['subID']).zfill(3)
session_str = str(expInfo['sessionID'])
experiment_time = datetime.now().strftime("%Y-%m-%d_%H%M%S") 

resultFile_name = f"sub-{sub_str}_ses-{session_str}_run-{run_str}_{experiment_time}"
resultFile_path = os.path.join(results_dir, resultFile_name)

thisExp = data.ExperimentHandler(
    name=expName, version='0.1',
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
    color="white",
    units='deg'  
)

win.mouseVisible = False

# --- STIMULI INITIALIZATION ---
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

# Text objects for intro/outro
intro_text = visual.TextStim(win, text="Initializing...", height=TEXT_SIZE_UI, color='black', wrapWidth=25)
goodbye_text = visual.TextStim(win, text="Thank you!", height=TEXT_SIZE_UI, color='black', wrapWidth=25)

rt_list = []
acc_list = []
trialClock = core.Clock()

#%%
# --- EXECUTION ---
run_intro(win, intro_text, trigger_keyList)

# Execute behavioral task
# Note: Ensure warning_image_1 and target_image have .image paths set inside run_behav
mean_rt, mean_acc = run_behav(
    win, thisExp, fixation_text, warning_image_1, target_image, 
    trialClock, rt_list, acc_list, results_dir, resultFile_name, 
    used_keyList, correct_responses
)

run_goodbye(win, goodbye_text)

# --- CLEANUP ---
thisExp.saveAsWideText(resultFile_path + ".csv")
logging.flush()
win.close()
core.quit()
