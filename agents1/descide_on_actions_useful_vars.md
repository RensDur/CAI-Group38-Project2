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
|```self._searchedRooms```  |Rooms that have been searched by the robot or human | List[~Rooms]|
|```self._distanceHuman```  |Distance between the robot and the human   |'close' or 'far'|
|```self._distanceDrop```   |Distance from the robot to the drop-zone   |'close' or 'far'   |
|```remainingZones```       |Remaining drop zones                       |List[~Zone-Info]   |
|```remainingVics```        |Remaining victims                          |List[~Victims]   |
|```remaining```            |Location of remaining victims|List[~Locations]<Br>_indexed by ~Victims_|
|   |   |   |


<hr>

## Setters: means of changing robot's behaviour
|Variable                   |Meaning                |Possible values|
|---------------------------|-----------------------|---------------|
|```self._goalVic```        |Target victim to rescue next| ~Victim|
|```self._goalLoc```        |Target location to move next| ~Location|
|```self._rescue```         |   | None or 'alone' or 'together'|
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

## Phase 9: PLAN_PATH_TO_VICTIM

**_Descibe the condition_**

_Describe the action that the robot takes accordingly_

```python

```

## Phase 10: FOLLOW_PATH_TO_VICTIM

**_Descibe the condition_**

_Describe the action that the robot takes accordingly_

```python

```

## Phase 11: TAKE_VICTIM

**_Descibe the condition_**

_Describe the action that the robot takes accordingly_

```python

```

## Phase 12: PLAN_PATH_TO_DROPPOINT

**_Descibe the condition_**

_Describe the action that the robot takes accordingly_

```python

```

## Phase 13: FOLLOW_PATH_TO_DROPPOINT

**_Descibe the condition_**

_Describe the action that the robot takes accordingly_

```python

```

## Phase 14: DROP_VICTIM

**_Descibe the condition_**

_Describe the action that the robot takes accordingly_

```python

```
