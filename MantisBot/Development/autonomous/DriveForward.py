from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

# this is one of your components
from componentsDrive import DriveTrainModule as DriveTrain


class DriveForward(AutonomousStateMachine):
    MODE_NAME = "Drive Forward"
    DEFAULT = False

    # Injected from the definition in robot.py
    drivetrain: DriveTrain

    @timed_state(duration=3.0, first=True, must_finish=True)
    def drive_forward(self):
        self.drivetrain.setInput((-0.25, 0.25))

    @state()
    def stop_state(self):
        self.drivetrain.setInput((0, 0))

    # def on_enable(self) -> None:
    #     return None
    
    # def on_iteration(self, tm: float) -> None:
    #     return None

    # def on_disable(self) -> None:
    #     return None

