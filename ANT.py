#%%
from psychopy import visual, event, core, data, logging, gui, monitors
from tools import *
import os
import numpy as np
from datetime import datetime

#%%
# --- MONITOR CALIBRATION ---
MON_WIDTH = 70       # Physical width of monitor in cm
MON_DISTANCE = 60    # Distance from eyes to monitor in cm
MON_SIZE = [1920, 1080] 

#%%
input_subID = 0
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID), 'runID': ['1', '2', '3'], 'sessionID': ['T1', 'T2']}

dlg = gui.DlgFromDict(dictionary=expInfo, title='Adaptive ANT')
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

win = visual.Window(monitor=my_monitor, fullscr=True, color=(-1, -1, -1), units='deg')
win.mouseVisible = False

# --- ADAPTIVE SIZE LOGIC (Proportional to Screen Height) ---
screen_height_deg = win.size[1]

# Set sizes as percentages of screen height
FIX_H  = screen_height_deg * 0.10   # 10% of screen height
TARG_H = screen_height_deg * 0.25   # 25% of screen height
TARG_W = TARG_H * 4.0               # Maintain 4:1 aspect ratio
WARN_S = screen_height_deg * 0.15   # 15% of screen height

# --- STIMULI INITIALIZATION ---
fixation_text = visual.TextStim(win, text="+", height=FIX_H, color='white', bold=True)
warning_image_1 = visual.ImageStim(win, size=(WARN_S, WARN_S))
target_image = visual.ImageStim(win, size=(TARG_W, TARG_H))

# Instructions
intro_text = init_intro(win, screen_height_deg) 
goodbye_text = init_goodbye(win, screen_height_deg)

rt_list, acc_list = [], []
trialClock = core.Clock()

#%%
# --- EXECUTION ---
run_intro(win, intro_text, ['s'])

mean_rt, mean_acc = run_behav(
    win, thisExp, fixation_text, warning_image_1, target_image, 
    trialClock, rt_list, acc_list, results_dir, resultFile_name, 
    ['f', 'j', 'escape'], {"left": "f", "right": "j"}
)

run_goodbye(win, goodbye_text)
win.close()
core.quit()
