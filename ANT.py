#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
from datetime import datetime

#%%
# --- MONITOR CALIBRATION (CRITICAL: Measure your actual screen) ---
MON_WIDTH = 70       # Physical width of monitor in cm
MON_DISTANCE = 60    # Distance from eyes to monitor in cm (standard desk)
MON_SIZE = [1920, 1080] # Screen resolution

# --- STIMULUS PARAMETERS (Degrees of Visual Angle) ---
FIXATION_HEIGHT = 1.2  
TARGET_SIZE = (8.0, 2.5)   # Width, Height of arrow image in degrees
WARNING_SIZE = (2.0, 2.0)  # Size of the star/cue in degrees
INSTRUCTION_HEIGHT = 1.0   # Font size in degrees

#%%
input_subID = 0
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID)}
expInfo['runID'] = ['1', '2', '3']
expInfo['sessionID'] = ['Baseline', 'Repeat_Baseline', 'T3', 'T6', 'T9', 'T12']

dlg = gui.DlgFromDict(dictionary=expInfo, title='Attention Network Test')
if dlg.OK == False: core.quit()

used_keyList = ['s', 'escape', 'f', 'j']
trigger_keyList = ['s']
correct_responses = {"left": "f", "right": "j"}

# --- FILENAME SETUP ---
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir): os.makedirs(results_dir)

run_str = str(expInfo['runID']).zfill(2)
sub_str = str(expInfo['subID']).zfill(3)
session_str = str(expInfo['sessionID'])
experiment_time = datetime.now().strftime("%Y-%m-%d_%H%M%S") 

resultFile_name = f"sub-{sub_str}_ses-{session_str}_run-{run_str}_{experiment_time}"
resultFile_path = os.path.join(results_dir, resultFile_name)

thisExp = data.ExperimentHandler(
    name=expName, version='1.0', extraInfo=expInfo,
    savePickle=True, saveWideText=True
)

#%%
# --- WINDOW INITIALIZATION ---
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(
    monitor=my_monitor, fullscr=True, screen=0,
    color="white", units='deg' 
)
win.mouseVisible = False

# --- STIMULI INITIALIZATION ---
fixation_text = visual.TextStim(win, text="+", height=FIXATION_HEIGHT, color='black')
warning_image_1 = visual.ImageStim(win, size=WARNING_SIZE)
target_image = visual.ImageStim(win, size=TARGET_SIZE)

# Initialize instructions (wrapWidth of 25 degrees is a safe central column)
intro_text = init_intro(win, 25) 
goodbye_text = init_goodbye(win, 25)

rt_list, acc_list = [], []
trialClock = core.Clock()

#%%
# --- EXECUTION ---
run_intro(win, intro_text, trigger_keyList)

# Run the behavioral task
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
