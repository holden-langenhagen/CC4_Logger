# Files Involved
evaluation_metrics.py  
 f006vqm@lisplab4:/scratch/f006vqm/CASTLE/CC4/blue-agent-v3/h-marl-3policy/subpolicies/evaluation_metrics.py  
logger.py  
 f006vqm@lisplab4:/scratch/f006vqm/CASTLE/CC4/blue-agent-v3/h-marl-3policy/subpolicies/logger.py

# Description
 This program logs the actions and results of blue, red, and green agents in the CAGE Challenge 4 environment to human-readable text files. 
 
 After running the evaluation script, the following log files are generated:  
  1) globallog.txt: Includes information all agents collectively produce (including actions/results of every agent).  
  2) bluelog.txt: Contains only what the blue agent can perceive.  
  3) redlog.txt: Contains only what the red agent can perceive.  

Purpose: This logging system lays the groundwork for integrating large language models (LLMs) to improve state-of-the-art reinforcement learning in cyber security simulations.

# CASTLE Installation (Skip if already completed)
1) Follow https://cage-challenge.github.io/cage-challenge-4/pages/tutorials/01_Getting_Started/1_Introduction/ to set up CC4.  
2) Clone the CASTLE repository into the same directory as CC4.  
3) Follow the instructions at https://github.com/BU-Lisp/CASTLE/tree/main/CC4/blue-agent-v3, some of these steps repeat what was done for CC4, there are some necessary steps. It is worthwhile to perform all steps unless you are confident in what you are doing  
4) Your home folder should contain:  
cage-challenge-4/ – the cloned CC4 environment  
CASTLE/ – the CASTLE repository  
(Optional) A Python virtual environment directory

# Logger Implementation Steps
1) Ensure logger.py is in the same folder as evaluation_metrics.py:  
 /scratch/f006vqm/CASTLE/CC4/blue-agent-v3/h-marl-3policy/subpolicies/logger.py  
2) Modify line 123 of evaluation_metrics.py:  
Replace:  
 observations, rew, term, trunc, info = wrapped_cyborg.step(actions)  
With:  
 observations, rew, term, trunc, info = logging_step(actions, log_path, observations, cyborg, wrapped_cyborg, j, i, EPISODE_LENGTH, red_agents, 1, 1, 1) # The last three numbers are flags for global log, blue log, and red log.  
3) Import logging_step at the top of evaluation_metrics.py:  
from logger import logging_step

# Run Evaluation with Logger
Execute the following in your terminal:  
```bash
tmux new -s eval_metrics_test
cd /scratch/f006vqm/CASTLE/CC4/blue-agent-v3/h-marl-3policy
export CHECKPOINT_PATH=/scratch/f006vqm/CASTLE/CC4/blue-agent-v3/h-marl-3policy/saved_policies/sub/iter_49
source /scratch/f006vqm/env/bin/activate
export PYTHONPATH=/scratch/f006vqm/CASTLE/CC4/evasion-extensions/cage-challenge-4-main:$PYTHONPATH
mkdir -p /scratch/f006vqm/results/eval_metrics_test_01
python3 -u subpolicies/evaluation_metrics.py submission.py --max-eps 100 /scratch/f006vqm/results/eval_metrics_test_01
```

**\*Script Modification Notes**  
 Be sure to replace all file paths with ones relevant to your specific system and file structure, especially the base folder /scratch/f006vqm and the results directory in the final two steps.
