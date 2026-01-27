#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
from datetime import datetime

# --- MONITOR CALIBRATION ---
MON_WIDTH = 70       
MON_DISTANCE = 60    
MON_SIZE = [1920, 1080] 

# --- STIMULUS PARAMETERS (Degrees) ---
FIX_HEIGHT = 1.0
TARG_SIZE = (8.0, 2.5)   
WARN_SIZE = (1.5, 1.5)

#%%
input_subID = 0
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID), 'runID': ['1', '2', '3'], 
           'sessionID': ['Baseline', 'T3', 'T6']}

dlg = gui.DlgFromDict(dictionary=expInfo, title='Attention Network Test')
if dlg.OK == False: core.quit()

# Keyboard setup
QUIT_KEYS = ['escape']
RESPONSE_KEYS = ['f', 'j']
trigger_keyList = ['s']
correct_responses = {"left": "f", "right": "j"}

# --- FILENAME SETUP ---
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir): os.makedirs(results_dir)

run_str = str(expInfo['runID']).zfill(2)
sub_str = str(expInfo['subID']).zfill(3)
session_str = str(expInfo['sessionID'])
experiment_time = datetime.now().strftime("%Y%m%d_%H%M%S") 

resultFile_name = f"sub-{sub_str}_ses-{session_str}_run-{run_str}_{experiment_time}"
resultFile_path = os.path.join(results_dir, resultFile_name)

thisExp = data.ExperimentHandler(name=expName, extraInfo=expInfo, savePickle=True, saveWideText=True)

#%%
# --- WINDOW INITIALIZATION (Using SelfOther's dark theme) ---
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(
    monitor=my_monitor, fullscr=True, 
    color=(-1, -1, -1), # Black background like SelfOther
    units='deg'
)
win.mouseVisible = False

# --- STIMULI ---
# Changed color to 'white' to contrast with black background
fixation_text = visual.TextStim(win, text="+", height=FIX_HEIGHT, color='white', bold=True)
warning_image_1 = visual.ImageStim(win, size=WARN_SIZE)
target_image = visual.ImageStim(win, size=TARG_SIZE)

intro_text = init_intro(win, 25) 
goodbye_text = init_goodbye(win, 25)

rt_list, acc_list = [], []
trialClock = core.Clock()

#%%
# --- EXECUTION ---
run_intro(win, intro_text, trigger_keyList)

# Start global timing
start_time = trialClock.getTime()

mean_rt, mean_acc = run_behav(
    win, thisExp, fixation_text, warning_image_1, target_image, 
    trialClock, rt_list, acc_list, results_dir, resultFile_name, 
    RESPONSE_KEYS + QUIT_KEYS, correct_responses
)

run_goodbye(win, goodbye_text)
win.close()
core.quit()
