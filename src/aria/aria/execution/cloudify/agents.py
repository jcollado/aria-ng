
class Agent(object):
    pass

class MockAgent(Agent):
    pass

class AgentExecutor(object):
    def __init__(self, agent=MockAgent()):
        self.agent = agent
