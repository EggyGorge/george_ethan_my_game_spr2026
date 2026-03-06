
is_log_enabled: bool = False

# state class blueprint
class State():
    def __init__(self):
        pass
    def enter(self):
        pass
    def exit(self):
        pass
    def update(self):
        pass
    def get_state_name(self):
        return ""

# state machine class
class StateMachine():
    def __init__(self):
        self.current_state = State()
        self.states = {} # dictionary
        print(self.states)
    
    # starts the state machine using a list
    def start_machine(self, init_states = [State]):

        # gets the player's state and prints it
        for state in init_states:
            print(state.get_state_name())
            self.states[state.get_state_name()] = state
            print(self.states)

        self.current_state = init_states[0]

        if is_log_enabled:
            print('starting state machine...')
        # when a new state is entered it will update to account for that state
        self.current_state.enter()
        print("state machine started with state:", self.current_state.get_state_name())

    # keeps checking if there is no state for the player
    def update(self):
        if self.current_state == None:
            print('no current state...')
        else:
            self.current_state.update()
        
    def transition(self, new_state_name):
        new_state: State = self.states.get(new_state_name) # sets new state to the type of a "state" 
        self.current_state_name = self.current_state.get_state_name()
        # checks for if the state doesn't exist
        if new_state == None:
            print("attempting to transition to non existent state")

        # exits the current state if the new state is different
        elif new_state != self.current_state:
            self.current_state.exit()
            
            if is_log_enabled:
                print('exiting state...')
            
            self.current_state = self.states[new_state.get_state_name()] # resets the current state so that it matches the new one

            if is_log_enabled:
                print('entering new state...')

            self.current_state.enter() # enters the new state
        # if the new state is the same as the current one then ignore it
        else:
            if is_log_enabled:
                print("attempt to transition to " + new_state_name + " ignored since it is the current state...")
    