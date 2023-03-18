class ReceivedMessageState:

    def __init__(self, msg="", time=0, dist='', robot_msg=[], found_vic=[], collected_vic=[]):
        # The message itself
        self.message = msg

        # Record time
        self.time = time

        # Store the distance between the human and the robot at the moment the message was received
        self.distanceHumanRobot = dist

        # Store the messages sent by the robot at the moment the message was received
        self.messagesSentByRobot = robot_msg

        # Store lists of found and collected victims at the moment this message was received
        self.foundVictims = found_vic
        self.collectedVictims = collected_vic
