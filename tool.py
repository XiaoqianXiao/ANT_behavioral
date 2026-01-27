from psychopy import visual, event, core, data, logging
import os
import pandas as pd
import numpy as np

def init_intro(win, screen_height):
    return visual.TextStim(win, 
        text="Please press F for LEFT arrows and J for RIGHT arrows.",
        height=screen_height * 0.08, # Adaptive font size
        wrapWidth=screen_height * 2, 
        color="white", pos=(0, 0))

def init_goodbye(win, screen_height):
    return visual.TextStim(win, text="Task Complete.", 
                           height=screen_height * 0.08, color="white")

def run_intro(win, intro_text, trigger_keyList):
    intro_text.draw()
    win.flip()
    event.waitKeys(keyList=trigger_keyList)
    core.wait(0.5)

def run_goodbye(win, goodbye_text):
    goodbye_text.draw()
    win.flip()
    core.wait(2.0)

def run_behav(win, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses):
    current_dir = os.getcwd()
    stim_dir = os.path.join(current_dir, 'experiment_design', 'stimuli')
    stimList = pd.read_csv(os.path.join(current_dir, 'experiment_design', 'stim_lists', 'run-all.csv'))
    
    # --- ADAPTIVE POSITION MATH ---
    screen_h = win.size[1]
    # Place stimuli at 25% of the screen height away from the center
    stimList['TargetPos_deg'] = np.where(stimList['TargetPosition'] > 0, screen_h * 0.25, screen_h * -0.25)
    stimList['CuePos_deg'] = np.where(stimList['CuePositionY'] > 0, screen_h * 0.25, screen_h * -0.25)
    
    # Trial timing logic (4 seconds per trial)
    stimList['abs_onset'] = np.cumsum([0] + [4.0] * (len(stimList)-1))
    trialClock.reset()

    for index, row in stimList.iterrows():
        trial = row.to_dict()
        
        # Timing sync
        while trialClock.getTime() < trial['abs_onset']:
            fixation_text.draw()
            win.flip()

        # Warning
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        warning_image_1.setPos((0, trial['CuePos_deg']))
        warning_image_1.draw()
        fixation_text.draw()
        win.flip()
        core.wait(0.1)

        # Target
        target_wait = trialClock.getTime() + 0.4 # 400ms delay after cue
        while trialClock.getTime() < target_wait:
            fixation_text.draw()
            win.flip()

        target_image.setImage(os.path.join(stim_dir, trial['TargetImage'] + ".bmp"))
        target_image.setPos((0, trial['TargetPos_deg']))
        target_image.draw()
        fixation_text.draw()
        win.flip()
        
        onset = trialClock.getTime()
        keys = event.waitKeys(maxWait=1.5, keyList=used_keyList, timeStamped=trialClock)
        
        acc, rt = 0, None
        if keys:
            key, k_time = keys[0]
            if key == 'escape': core.quit()
            rt = k_time - onset
            acc = 1 if key == correct_responses[trial['TargetDirection']] else 0
        
        rt_list.append(rt)
        acc_list.append(acc)
        thisExp.addData('rt', rt)
        thisExp.addData('acc', acc)
        thisExp.nextEntry()

    return np.mean(acc_list), np.mean([r for r in rt_list if r])
