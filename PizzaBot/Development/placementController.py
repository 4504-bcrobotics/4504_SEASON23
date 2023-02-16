from magicbot import StateMachine, state, timed_state

class PlacementController(StateMachine):
    elevator: ElevatorModule
    intake: IntakeModule

    level = 1

    def placeHigh(self):
        self.level = 3
        self.engage()
    
    def placeMid(self):
        self.level = 2
        self.engage()

    def placeLow(self):
        self.level = 1
        self.engage()

    @timed_state(first=True, duration=1, must_finish=True)
    def raise_elevator(self):
        if self.level == 3:
            self.elevator.moveToTop()

        elif self.level == 2:
            self.elevator.moveToMid()

        else:
            self.elevator.moveToLow()

        if self.is_atLevel():
            self.next_state_now('release_gamepiece')

    @state()
    def release_gamepiece(self):
        self.intake.open()

    def is_atLevel(self):
        if self.level == self.elevator.currentLevel:
            return True
        else:
            return False


        