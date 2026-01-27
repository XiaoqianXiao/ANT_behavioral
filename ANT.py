#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
from datetime import datetime

#%%
# --- MONITOR CALIBRATION ---
# If things are too small, DECREASE MON_DISTANCE.
# If things are too big, INCREASE MON_DISTANCE.
MON_WIDTH = 70       
MON_DISTANCE = 50    # Distance in cm (reduced to make things look larger)
MON_SIZE = [1920, 1080] 

# --- STIMULUS PARAMETERS (Fixed Degrees - High Visibility) ---
# These are the numbers you should change to adjust size manually
FIX_H = 2.0         # Height of fixation cross
TARG_SIZE = (12.0, 3.5) # Width, Height of arrows
WARN_S = 2.5        # Size of the star/cue
INST_H = 1.2        # Font size

#%%
input_subID = 0
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID), 'runID': '1'}

dlg = gui.DlgFromDict(dictionary=expInfo, title='Attention Network Test')
if dlg.OK == False: core.quit()

# --- FILENAME SETUP ---
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir): os.makedirs(results_dir)
experiment_time = datetime.now().strftime("%Y%m%d_%H%M%S") 
resultFile_name = f"sub-{expInfo['subID']}_run-{expInfo['runID']}_{experiment_time}"
resultFile_path = os.path.join(results_dir, resultFile_name)
thisExp = data.ExperimentHandler(name=expName, extraInfo=expInfo, savePickle=True, saveWideText=True)

#%%
# --- WINDOW INITIALIZATION ---
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)
my_monitor.setSizePix(MON_SIZE)

# Using a standard grey background for better visibility of all stimuli
win = visual.Window(
    monitor=my_monitor, 
    fullscr=True, 
    color=(0, 0, 0), # Neutral Grey (using 0 to 1 scale or -1 to 1 depending on version)
    colorSpace='rgb',
    units='deg'
)
win.mouseVisible = False

# --- STIMULI INITIALIZATION ---
fixation_text = visual.TextStim(win, text="+", height=FIX_H, color='white', bold=True)
warning_image_1 = visual.ImageStim(win, size=(WARN_S, WARN_S))
target_image = visual.ImageStim(win, size=TARG_SIZE)

# Instructions
intro_text = init_intro(win, INST_H) 
goodbye_text = init_goodbye(win, INST_H)

rt_list, acc_list = [], []
trialClock = core.Clock()

#%%
# --- EXECUTION ---
run_intro(win, intro_text, ['s', 'space'])

# Behavioral task
mean_rt, mean_acc = run_behav(
    win, thisExp, fixation_text, warning_image_1, target_image, 
    trialClock, rt_list, acc_list, results_dir, resultFile_name, 
    ['f', 'j', 'escape'], {"left": "f", "right": "j"}
)

run_goodbye(win, goodbye_text)
win.close()
core.quit()
