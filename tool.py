from psychopy import visual, event, core, data, logging
import os
import pandas as pd
import numpy as np

def init_intro(win, inst_height):
    return visual.TextStim(win, 
        text="Press F for LEFT ( < ) and J for RIGHT ( > ).\n\nPress SPACE or S to start.",
        height=inst_height, wrapWidth=25, color="white", pos=(0, 0))

def init_goodbye(win, inst_height):
    return visual.TextStim(win, text="Task Complete. Please wait...", 
                           height=inst_height, color="white")

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
    stim_list_path = os.path.join(current_dir, 'experiment_design', 'stim_lists', 'run-all.csv')
    
    if not os.path.exists(stim_list_path):
        print(f"Error: Could not find {stim_list_path}")
        core.quit()
        
    stimList = pd.read_csv(stim_list_path)
    
    # Position Math: Moving them 4 degrees up/down is standard for ANT
    stimList['TargetPos_deg'] = np.where(stimList['TargetPosition'] > 0, 4.0, -4.0)
    stimList['CuePos_deg'] = np.where(stimList['CuePositionY'] > 0, 4.0, -4.0)
    
    trialClock.reset()

    for index, row in stimList.iterrows():
        trial = row.to_dict()
        
        # 1. Baseline Fixation
        fixation_text.draw()
        win.flip()
        core.wait(getAttrib(trial, "DurationOfFixation") / 1000)

        # 2. Warning Cue
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        warning_image_1.setPos((0, trial['CuePos_deg']))
        warning_image_1.draw()
        fixation_text.draw()
        win.flip()
        core.wait(0.1)

        # 3. Post-cue Fixation
        fixation_text.draw()
        win.flip()
        core.wait(getAttrib(trial, "IntervalBetweenCueAndTarget") / 1000)

        # 4. Target Slide
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

    # Mask None values for mean calculation
    valid_rts = [r for r in rt_list if r is not None]
    m_rt = np.mean(valid_rts) if valid_rts else 0
    m_acc = np.mean(acc_list) if acc_list else 0
    
    return m_acc, m_rt

def getAttrib(dict_obj, key):
    return dict_obj.get(key, 0)
