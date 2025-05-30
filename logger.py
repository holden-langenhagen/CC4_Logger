import os
import json
import os

def storeRecent(agent_name, action, json_path):
    """Store the 4 most recent actions for each agent in a JSON file."""
    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    if agent_name not in data:
        data[agent_name] = []
    data[agent_name].append(action)
    # Keep only the last 4 actions
    data[agent_name] = data[agent_name][-4:]
    with open(json_path, 'w') as f:
        json.dump(data, f)

def loadNonSleep(agent_name, json_path):
    """Load the most recent non-'Sleep' action for the agent from the JSON file. Returns 'Sleep' if none found."""
    if not os.path.exists(json_path):
        return "Sleep"
    with open(json_path, 'r') as f:
        data = json.load(f)
    actions = data.get(agent_name, [])
    for action in reversed(actions):
        if action != "Sleep":
            return action
    return "Sleep"

def logging_step(actions, log_path, observations, cyborg, wrapped_cyborg, pseudostep, episode, EPISODE_LENGTH, red_agents, globalflag, blueFlag, redFlag): # Numbers are flags for global log, blue log, and red log
    globallog_path = log_path + "globallog.txt"
    bluelog_path = log_path + "bluelog.txt"
    redlog_path = log_path + "redlog.txt"
    global_json_path = log_path + "tempglobal.json"
    
    if (episode == 0 and pseudostep == 0):
        open(log_path + "bluelog.txt", mode="w").close() # Clear log files
        open(log_path + "globallog.txt", mode="w").close()
        open(log_path + "redlog.txt", mode="w").close()
        open(log_path + "tempglobal.json", mode="w").close() # Clear temp json files
    
    if any("master" in agent_name for agent_name in actions): # Skip step if master agents are present
        observations, rew, term, trunc, info = wrapped_cyborg.step(actions)
        return observations, rew, term, trunc, info

    if globalflag:
        with open(globallog_path, mode="a") as file: # Global consists of Blue-(step)-Green-Red
            file.write("\n")
            file.write(f"Episode #{episode+1}\tStep #{pseudostep//2+1}\n")

            observations, rew, term, trunc, info = wrapped_cyborg.step(actions)

            """BLUE AGENTS LOGGING"""
            for (agent_name, action) in actions.items():
                action_label = wrapped_cyborg.action_labels(agent_name[:12])[action]
                storeRecent(agent_name, action_label, global_json_path) # Store recent actions
                action_label = loadNonSleep(agent_name, global_json_path) # Load last non-sleep action
                file.write(f"Agent: {agent_name}\tAction: {action_label}\tResult: {cyborg.get_observation(agent_name[:12])['success']}\n")
            
            """GREEN + RED AGENTS LOGGING"""
            for agent_name in cyborg.active_agents:
                if "blue" not in agent_name:
                    action_label = cyborg.get_last_action(agent_name)[0]
                    file.write(f"Agent: {agent_name}\tAction: {action_label}\tResult: {cyborg.get_observation(agent_name)['success']}\n")
            
    else:
        observations, rew, term, trunc, info = wrapped_cyborg.step(actions)

    if redFlag:
        with open(redlog_path, mode="a") as file: # Red logging after step because we don't know the planned actions
            file.write("\n")
            file.write(f"Episode #{episode+1}\tStep #{pseudostep//2+1}\n")

            """GREEN + RED AGENTS LOGGING"""
            for agent_name in cyborg.active_agents:
                if "blue" not in agent_name and "green" not in agent_name:
                    action_label = cyborg.get_last_action(agent_name)[0]
                    file.write(f"Agent: {agent_name}\tAction: {action_label}\tResult: {cyborg.get_observation(agent_name)['success']}\n")

    if blueFlag:
        with open(bluelog_path, mode="a") as file: # Blue logging before step because we have the planned actions
            file.write("\n")
            file.write(f"Episode #{episode+1}\tStep #{pseudostep//2+1}\n")

            """BLUE AGENTS LOGGING"""
            for (agent_name, action) in actions.items():
                action_label = wrapped_cyborg.action_labels(agent_name[:12])[action]
                file.write(f"Agent: {agent_name}\tAction: {action_label}\n")

    if pseudostep//2+1 == EPISODE_LENGTH:
        # Delete temp json files at the end of the episode
        if os.path.exists(global_json_path):
            os.remove(global_json_path)

    return observations, rew, term, trunc, info