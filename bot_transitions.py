from transitions import Machine


class Bot_transition(object):
    states = ['start', 'new', 'english', 'russian', 'method_english', 'method_russian']

    def __init__(self):
        self.machine = Machine(model=self, states=Bot_transition.states, initial='start')

        self.machine.add_transition(trigger='english', source='start', dest='method_english')
        self.machine.add_transition(trigger='russian', source='start', dest='method_russian')

        self.machine.add_transition('new', '*', 'start')
