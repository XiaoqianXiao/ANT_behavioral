#%%
from psychopy import visual, event, core, data, logging, gui
from tools import *
import time
import os
import pandas as pd
import random
import numpy as np
from datetime import datetime
#%%
input_subID = 0
input_runID = 1
input_session = 'pre'
sessionID = input_session
current_dir = os.getcwd()
expName = 'ANT'
expInfo = {'subID': str(input_subID), 'sessionID': sessionID, 'runID':str(input_runID)}
expInfo['time'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
expInfo['location'] = ['CHN', 'CONNECTLAB']
#%%
dlg = gui.DlgFromDict(dictionary=expInfo, title='My Experiment')
if dlg.OK == False:
    core.quit()  # User pressed cancel
if expInfo['location'] == 'CHN':
    used_keyList = ['t', 'escape', '2', '3']
    trigger_keyList = ['t']
    correct_responses = {
        "left": "2",
        "right": "3"
    }
else:
    used_keyList = ['s', 'escape', 'f', 'j']
    trigger_keyList = ['s']
    correct_responses = {
        "left": "f",
        "right": "j"
    }
#Initialize the results file
results_dir = os.path.join(current_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)
runID = expInfo['runID'].zfill(2)
subID = expInfo['subID'].zfill(3)
resultFile_name = 'sub-' + subID + '_ses-' + sessionID + '_run-' + runID + '_time-' + expInfo['time']
thisExp = data.ExperimentHandler(
    name=expName, version='0.1',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='',
    savePickle=True, saveWideText=True
)
# Set the logging level to ERROR to suppress warnings
resultFile_path = os.path.join(results_dir, resultFile_name)
logFile = logging.LogFile(resultFile_path+".log", level=logging.EXP)
logging.console.setLevel(logging.ERROR)
#%%
# Initialize PsychoPy window
win = visual.Window(
    # size=(640, 480),
    fullscr=True,
    screen=0, allowGUI=True, allowStencil=False,
    monitor='testMonitor',
    color="white",
    blendMode='avg', useFBO=True,
    #units='pix'
    units='norm'
)
# Hide the cursor
win.mouseVisible = False
# Get the size of the window
win_width, win_height = win.size
# Initialize components
intro_text = init_intro(win, win_width)
goodbye_text = init_goodbye(win, win_width)

# Initialize components for the experiment
warning_image_1 = visual.ImageStim(win,
                                   size=(0.00002 * win_width, 0.000035 * win_height),
                                   opacity=1)
#warning_image_2 = visual.ImageStim(win)
target_image = visual.ImageStim(win,
                                size=(win_width * 0.00025, win_height * 0.0006),
                                opacity=1)
fixation_text = visual.TextStim(
    win,
    text="+",
    height=0.08,  # Font size
    bold=False,  # Font bold
    pos=(0, 0),  # Position in the center of the screen
    wrapWidth=0.8 * win_width,  # 5% of window width
    color='black',
    opacity=1
)
rt_list = []
acc_list = []
# Clock for timing
globalClock = core.Clock()
trialClock = core.Clock()

run_intro(win, intro_text, trigger_keyList)
# Run IFISBlockList equivalent
mean_rt, mean_acc = run_runs(win, runID, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses)
# Run Goodbye
run_goodbye(win, goodbye_text)
masked_rt_list = np.ma.masked_equal(rt_list, None)
masked_acc_list = np.ma.masked_equal(acc_list, None)
mean_rt = round(np.mean(masked_rt_list) * 1000)
mean_acc = round(np.mean(masked_acc_list) * 100)
print("Your mean reaction time is: ", mean_rt, "ms")
print("Your mean ACC is: ", mean_acc, "%")
# Save the experiment data
thisExp.saveAsWideText(resultFile_path)
thisExp.saveAsPickle(resultFile_path)
logging.flush()
thisExp.abort()  # Ensure the data is saved
win.close()
core.quit()
