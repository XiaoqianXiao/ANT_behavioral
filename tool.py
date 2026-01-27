from psychopy import visual, event, core, data, logging
import os
import pandas as pd
import numpy as np

def init_intro(win, win_width):
    # Changed color to white for black background
    return visual.TextStim(win, 
        text="Please press F for LEFT arrows and J for RIGHT arrows.",
        height=1.0, wrapWidth=25, color="white", pos=(0, 0))

def init_goodbye(win, win_width):
    return visual.TextStim(win, text="Task Complete.", height=1.0, color="white")

def run_behav(win, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses):
    current_dir = os.getcwd()
    stimList_name = 'run-all.csv'
    stimList_dir = os.path.join(current_dir, 'experiment_design', 'stim_lists', stimList_name)
    stim_dir = os.path.join(current_dir, 'experiment_design', 'stimuli')
    stimList = pd.read_csv(stimList_dir)
    
    # Position math for degrees
    DEG_SCALE = 50 
    stimList['TargetPos_deg'] = (240 - stimList['TargetPosition']) / DEG_SCALE
    stimList['CuePos_deg'] = (240 - stimList['CuePositionY']) / DEG_SCALE

    # Calculate absolute trial onsets (assuming 4000ms per trial if not in CSV)
    # This mimics the 'onset_time' logic in SelfOther
    stimList['abs_onset'] = np.cumsum([0] + [4.0] * (len(stimList)-1))

    trials = stimList.sample(frac=1).reset_index(drop=True)
    trialClock.reset()

    for index, row in trials.iterrows():
        trial = row.to_dict()
        
        # --- SELF-OTHER TIMING LOGIC ---
        # Instead of core.wait, we loop until the clock reaches the target time
        while trialClock.getTime() < trial['abs_onset']:
            fixation_text.draw()
            win.flip()

        # 1. Cue/Warning
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        warning_image_1.setPos((0, trial['CuePos_deg']))
        
        warning_image_1.draw()
        fixation_text.draw()
        win.flip()
        core.wait(0.1) # Brief cue

        # 2. Target (Arrows)
        # Wait for Target Onset (Cue onset + 0.4s buffer)
        target_target_time = trialClock.getTime() + (trial['IntervalBetweenCueAndTarget'] / 1000)
        while trialClock.getTime() < target_target_time:
            fixation_text.draw()
            win.flip()

        target_image.setImage(os.path.join(stim_dir, trial['TargetImage'] + ".bmp"))
        target_image.setPos((0, trial['TargetPos_deg']))
        target_image.draw()
        fixation_text.draw()
        win.flip()
        
        onset_timestamp = trialClock.getTime()
        
        # 3. Response Collection
        keys = event.waitKeys(maxWait=1.5, keyList=used_keyList, timeStamped=trialClock)
        
        acc = 0
        rt = None
        if keys:
            response, end_time = keys[0]
            if response == 'escape': core.quit()
            rt = end_time - onset_timestamp
            acc = 1 if response == correct_responses[trial['TargetDirection']] else 0
        
        rt_list.append(rt)
        acc_list.append(acc)
        
        # Logging
        thisExp.addData('target_onset', onset_timestamp)
        thisExp.addData('rt', rt)
        thisExp.addData('acc', acc)
        thisExp.nextEntry()

    return np.mean(acc_list), np.mean([r for r in rt_list if r])
