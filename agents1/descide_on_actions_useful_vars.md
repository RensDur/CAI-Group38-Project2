# These are useful variables that we can use to adapt the robot's decisions


## Obviously: the trust beliefs:
I've created two functions that quickly extract the trust-belief values for the human-teammate

Willingness:    ```getCurrentWillingnessBelief()``` <Br>
Competence:     ```getCurrentCompetenceBelief()```

These are placed inside the scope of ```decide_on_actions()```.


<hr>

## Getters: provide information that we base our decision on

|Variable                   |Meaning                |Possible values|
|---------------------------|-----------------------|---------------|
|```self._searchedRooms```  |Rooms that have been searched by the robot or human | List[~Room]|
|```self._distanceHuman```  |Distance between the robot and the human   |'close' or 'far'|
|```self._distanceDrop```   |Distance from the robot to the drop-zone   |'close' or 'far'   |
|```self._roomVics```       |List of victims in the current room        |List[~Victim]|
|```self._recentVic```      |Recently (or currently) considered victim  |~Victim|
|```remainingZones```       |Remaining drop zones                       |List[~Zone-Info]   |
|```remainingVics```        |Remaining victims                          |List[~Victim]   |
|```remaining```            |Location of remaining victims|List[~Location]<Br>_indexed by ~Victims_|
|   |   |   |


<hr>

## Setters: means of changing robot's behaviour
|Variable                   |Meaning                |Possible values|
|---------------------------|-----------------------|---------------|
|```self._goalVic```        |Target victim to rescue next| ~Victim|
|```self._goalLoc```        |Target location to move next| ~Location|
|```self._rescue```         |Directive for the robot to start rescuing a victim   | None or 'alone' or 'together'|
|   |   |   |




# Decisions that are currently made by the robot

## Phase 1: FIND_NEXT_GOAL

**All areas have been searched, but there's still victims left.**
Define a previously found victim as target
```python
if vic in self._foundVictims and vic in self._todo and len(self._searchedRooms)==0:
```

**Otherwise, if not all areas have been searched and there's still victims left in the 'found' list**
Define a previously found victim as target
```python
if vic in self._foundVictims and vic not in self._todo:
```

**If there are no target victims found (found-list empty)**
Visit an unsearched area to search for victims
```python
if vic not in self._foundVictims or vic in self._foundVictims and vic in self._todo and len(self._searchedRooms)>0:
    PHASE -> PICK_UNSEARCHED_ROOM
```

## Phase 2: PICK_UNSEARCHED_ROOM

**If all areas have been searched but the task is not finished**
```python
if self._remainingZones and len(unsearchedRooms) == 0:
    PHASE -> FIND_NEXT_GOAL
```

_Start searching areas again_

**Otherwise, if there are still areas to search**
```python
else:
    PHASE -> PLAN_PATH_TO_ROOM
```

_Define which one to search next_

## Phase 3: PLAN_PATH_TO_ROOM

**NO IMPORTANT DECISIONS ARE MADE IN THIS PHASE**

## Phase 4: FOLLOW_PATH_TO_ROOM

**NO IMPORTANT DECISIONS ARE MADE IN THIS PHASE**

## Phase 5: REMOVE_OBSTACLE_IF_NEEDED

**If the human tells the agent not to remove the obstacle**
```python
if self.received_messages_content and self.received_messages_content[-1] == 'Continue' and not self._remove:
    PHASE -> FIND_NEXT_GOAL
```

_Determine the next area to explore_

**If the human tells the agent to (help) remove the rock**
```python
if self.received_messages_content and self.received_messages_content[-1] == 'Remove' or self._remove:
```

*** OBSTACLE: ROCK ***

_Wait for the human to help removing the obstacle and remove the obstacle together_

*** OBSTACLE: TREE ***

_Remove the obstacle if the human tells the agent to do so_

*** OBSTACLE: STONES ***

_Remove the obstacle alone if the human decides so_

OR:

_Remove the obstacle together if the human decides so_

## Phase 6: ENTER_ROOM

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**

## Phase 7: PLAN_ROOM_SEARCH_PATH

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**

## Phase 8: FOLLOW_ROOM_SEARCH_PATH

**The robot has found a mildly- or critically-injured victim**

_Describe the action that the robot takes accordingly_

```python
if 'mild' in vic and self._answered == False and not self._waiting:
    self._sendMessage('Found ' + vic + ' in ' + self._door['room_name'] + '. Please decide whether to "Rescue together", "Rescue alone", or "Continue" searching. \n \n \
        Important features to consider are: \n safe - victims rescued: ' + str(self._collectedVictims) + '\n explore - areas searched: area ' + str(self._searchedRooms).replace('area ','') + '\n \
        clock - extra time when rescuing alone: 15 seconds \n afstand - distance between us: ' + self._distanceHuman,'RescueBot')
    self._waiting = True
        
if 'critical' in vic and self._answered == False and not self._waiting:
    self._sendMessage('Found ' + vic + ' in ' + self._door['room_name'] + '. Please decide whether to "Rescue" or "Continue" searching. \n\n \
        Important features to consider are: \n explore - areas searched: area ' + str(self._searchedRooms).replace('area','') + ' \n safe - victims rescued: ' + str(self._collectedVictims) + '\n \
        afstand - distance between us: ' + self._distanceHuman,'RescueBot')
    self._waiting = True
```


<hr>

**The robot discovered that the victim, about which it learned it was located in room A, is in fact not there**

_Communicate that the agent did not find the target victim in the are, while the human previously communicted the victim was located there._

```python
if self._goalVic in self._foundVictims and self._goalVic not in self._roomVics and self._foundVictimLocs[self._goalVic]['room'] == self._door['room_name']:
```

<hr>

**The RescueBot received a message from the human saying it wants to rescue a critically injured victim**

_Rescue the victim, together with the human_

```python
if self.received_messages_content and self.received_messages_content[-1] == 'Rescue' and 'critical' in self._recentVic:
    self._rescue = 'together'
```

<hr>

**The RescueBot received a message from the human saying it wants to rescue a mildly injured victim, together**

_Rescue the victim, together with the human_

```python
if self.received_messages_content and self.received_messages_content[-1] == 'Rescue together' and 'mild' in self._recentVic:
    self._rescue = 'together'
```

<hr>

**The RescueBot received a message from the human saying it should rescue a mildly injured victim alone.**

_Rescue the victim, without help from the human_

```python
if self.received_messages_content and self.received_messages_content[-1] == 'Rescue alone' and 'mild' in self._recentVic:
    [...]
    self._rescue = 'alone'
```

<hr>

**The human says that the robot should continue searching rooms**

_Do as the human instructed_

```python
if self.received_messages_content and self.received_messages_content[-1] == 'Continue':
    [...]
    self._todo.append(self._recentVic)
    self._recentVic = None
    PHASE -> FIND_NEXT_GOAL
```

<hr>

**The robot hasn't heard from the human yet, about whether to rescue the victim or not**

_Wait indefinetely_

```python
if self.received_messages_content and self._waiting and self.received_messages_content[-1] != 'Rescue' and self.received_messages_content[-1] != 'Continue':
    return None, {}
```


## Phase 9: PLAN_PATH_TO_VICTIM

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**

## Phase 10: FOLLOW_PATH_TO_VICTIM

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**

## Phase 11: TAKE_VICTIM

_Some interesting decisions are made, but I don't think we should take these into consideration_ ~Rens

## Phase 12: PLAN_PATH_TO_DROPPOINT

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**

## Phase 13: FOLLOW_PATH_TO_DROPPOINT

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**

## Phase 14: DROP_VICTIM

**NO INTERESTING DECISIONS ARE MADE IN THIS PHASE**



Willingness = eigen initiatief | beschikbaarbaarheid voor hulp | motivatie om de taak te voltooien
Competence  = goed geheugen | snelste route kiezen | weak/normal/strong | 



self._sendMessage('Our score is ' + str(state['rescuebot']['score']) + '.', 'RescueBot')
If you are ready to begin our mission, you can simply start moving.', 'RescueBot')
self._sendMessage('Moving to ' + self._foundVictimLocs[vic]['room'] + ' to pick up ' + self._goalVic +'. Please come there as well to help me carry ' + self._goalVic + ' to the drop zone.', 'RescueBot')
self._sendMessage('Going to re-search all areas.', 'RescueBot')
self._sendMessage('Moving to ' + str(self._door['room_name']) + ' to pick up ' + self._goalVic + ' together with you.', 'RescueBot')
self._sendMessage('Moving to ' + str(self._door['room_name']) + ' to pick up ' + self._goalVic + '.', 'RescueBot')
self._sendMessage('Moving to ' + str(self._door['room_name']) + ' because it is the closest unsearched area.', 'RescueBot')
self._sendMessage('Reaching ' + str(self._door['room_name']) + ' will take a bit longer because I found stones blocking my path.', 'RescueBot')
\n clock - removal time: 5 seconds \n afstand - distance between us: ' + self._distanceHuman ,'RescueBot')
self._sendMessage('Please come to ' + str(self._door['room_name']) + ' to remove rock.','RescueBot')
self._sendMessage('Lets remove rock blocking ' + str(self._door['room_name']) + '!','RescueBot')
\n clock - removal time: 10 seconds','RescueBot')
self._sendMessage('Removing tree blocking ' + str(self._door['room_name']) + '.','RescueBot')
self._sendMessage('Removing tree blocking ' + str(self._door['room_name']) + ' because you asked me to.', 'RescueBot')
\n clock - removal time together: 3 seconds \n afstand - distance between us: ' + self._distanceHuman + '\n clock - removal time alone: 20 seconds','RescueBot')
self._sendMessage('Removing stones blocking ' + str(self._door['room_name']) + '.','RescueBot')
self._sendMessage('Please come to ' + str(self._door['room_name']) + ' to remove stones together.','RescueBot')
self._sendMessage('Lets remove stones blocking ' + str(self._door['room_name']) + '!','RescueBot')
self._sendMessage('Found ' + vic + ' in ' + self._door['room_name'] + ' because you told me ' + vic + ' was located here.','RescueBot')
clock - extra time when rescuing alone: 15 seconds \n afstand - distance between us: ' + self._distanceHuman,'RescueBot')
afstand - distance between us: ' + self._distanceHuman,'RescueBot')
self._sendMessage(self._goalVic + ' not present in ' + str(self._door['room_name']) + ' because I searched the whole area without finding ' + self._goalVic + '.','RescueBot')
self._sendMessage('Please come to ' + str(self._door['room_name']) + ' to carry ' + str(self._recentVic) + ' together.', 'RescueBot')
self._sendMessage('Lets carry ' + str(self._recentVic) + ' together! Please wait until I moved on top of ' + str(self._recentVic) + '.', 'RescueBot')
self._sendMessage('Please come to ' + str(self._door['room_name']) + ' to carry ' + str(self._recentVic) + ' together.', 'RescueBot')
self._sendMessage('Lets carry ' + str(self._recentVic) + ' together! Please wait until I moved on top of ' + str(self._recentVic) + '.', 'RescueBot')
self._sendMessage('Picking up ' + self._recentVic + ' in ' + self._door['room_name'] + '.','RescueBot')
self._sendMessage('Transporting ' + self._goalVic + ' to the drop zone.', 'RescueBot')
self._sendMessage('Delivered ' + self._goalVic + ' at the drop zone.', 'RescueBot')
self._sendMessage('Moving to ' + str(self._door['room_name']) + ' to help you remove an obstacle.','RescueBot')
self._sendMessage('Will come to ' + area + ' after dropping ' + self._goalVic + '.','RescueBot')