from random import choice
from time import sleep

SLEEP_TIME = 0.5

# %% State Machine
class StateMachine:
    def __init__(self):

        # Transition Table
        self.transitionTable = {
        ('WAIT', False): (self.checkMove, self.turnOnMotors, 'MOVE'),
        ('MOVE', 'onChargingStation'): (self.checkBalance, self.turnOnBalance, 'BALANCE'),
        ('BALANCE', 'teleopBegins'): (self.checkWait, self.turnOffBalance, 'WAIT'),
        ('PLACE', 'noGamePiece'): (self.checkMove, self.turnOnMotors, 'MOVE'),
        ('MOVE', 'teleopBegins'): (self.checkWait, self.turnOffMotors, 'WAIT'),
        ('MOVE', 'hasGamePiece'): (self.checkPlace, self.turnOnArm, 'PLACE'),
        ('PLACE', 'teleopBegins'): (self.checkWait, self.turnOffArm, 'WAIT')  
    }

    # Conditions
    def checkWait(self, value):
        return False
        
    def checkMove(self, value):
        return choice(['onChargingStation', 'teleopBegins', 'hasGamePiece'])
        
    def checkBalance(self, value):
        return 'teleopBegins'

    def checkPlace(self, value):
        return choice(['noGamePiece', 'teleopBegins'])

    # Transitions
    def turnOnMotors(self):
        sleep(SLEEP_TIME)
        print('Motors On!')
        return False 
    
    def turnOnBalance(self):
        sleep(SLEEP_TIME)
        print('Balance on')
        return False 
    
    def turnOffBalance(self):
        sleep(SLEEP_TIME)
        print('Balance off')
        return False
    
    def turnOffArm(self):
        sleep(SLEEP_TIME)
        print('Arm off')
        return False
    
    def turnOffMotors(self):
        sleep(SLEEP_TIME)
        print('Motors off')
        return False
    
    def turnOnArm(self):
        sleep(SLEEP_TIME)
        print('Arm On')
        return False
        
    
    # Run the state machine
    def run(self, initialState, input):
        state = initialState
        while state is not None:

            # Get {condition: transition} pair
            # {(currentState, input): (condition, transition, nextState)}
            tuple_key = (state, input)
            assert tuple_key in self.transitionTable, f'[!] Key {tuple_key} does not exist in transition table.'
            (condition, transition, nextState) = self.transitionTable[tuple_key]
            
            if condition is not None:
                if condition(input) is True: 
                    continue # Failed test
                input = condition(input)

            if transition is not None:
                transition()
            
            state = nextState


if __name__ == '__main__':

    FSM = StateMachine()
    FSM.run('WAIT', False)