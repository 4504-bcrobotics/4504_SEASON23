from magicbot import StateMachine, state, timed_state

from componentsGrabber import GrabberModule
from componentsElevator import ElevatorModule
from componentsHMI import HMIModule

class PlacementController(StateMachine):
    elevator: ElevatorModule
    grabber: GrabberModule

    targetLevel = 0

    def place(self, level):
        self.targetLevel = level
        self.engage()
        return False

    @state(first=True, must_finish=True)
    def state_elevatorRaise(self):
        if self.elevator.nextLevel != self.targetLevel:
            self.elevator.setNextLevel(self.targetLevel)

        if self.elevator.isAtLevel():
            self.next_state_now('state_extendGrabber')

    @state(must_finish=True)
    def state_extendGrabber(self):
        if self.grabber.nextLevel != self.targetLevel:
            self.grabber.setNextLevel(self.targetLevel)

        if self.grabber.isAtLevel():
            self.next_state_now('state_openGrabber')

    @state(must_finish=True, timed_state=0.25)
    def state_openGrabber(self):
        if not self.grabber.is_open():
            self.grabber.setOpen()

        self.next_state('state_retractGrabber')

    @state(must_finish=True)
    def state_retractGrabber(self):
        self.targetLevel = 0
        if self.grabber.nextLevel != self.targetLevel:
            self.grabber.setNextLevel(self.targetLevel)

        if self.grabber.isAtLevel():
            self.next_state_now('state_elevatorLower')

    @state(must_finish=True)
    def state_elevatorLower(self):
        self.targetLevel = 0
        if self.elevator.nextLevel != self.targetLevel:
            self.elevator.setNextLevel(self.targetLevel)

    
