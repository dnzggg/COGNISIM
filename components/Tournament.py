import re
from .Agent import Agent


class Tournament:
    def __init__(self, file_name="./trail1eventHistory.pl"):
        self.file_name = file_name
        self.round = 0
        self.generation = 0
        self._agents = []
        self._conductors = []
        self.find_initial_agents()

    def find_initial_agents(self):
        self.find_agents(0)

    def start(self):
        f = open(self.file_name, "r")

        cont = True
        new_generation = False
        while cont:
            self.round += 1
            for line in f:
                if not new_generation:
                    line = line.strip()
                    if re.search(r"^new_generation\(\d*\):\d", line):
                        new_generation = True
                        self._agents = []
                        self.generation += 1
                    elif m := re.search(r"^perform\(.*:" + str(self.round) + r"$", line):
                        # print(m.group())
                        break
                else:
                    conductor = re.search(r"^initially\(goal_of\((\w*),coordinate\(\)\)=active\):" + str(self.round-1) + r"$", line)
                    agent = re.search(r"^initially\(fitness_of\((\w*)\)=0\):" + str(self.round-1) + r"$", line)
                    if conductor:
                        name = conductor.group(1)
                        index = re.search(r"^coordinator(\d+)", name).group(1)
                        self._conductors.append(Agent(int(index), name, conductor=True))
                    if agent:
                        name = agent.group(1)
                        index = re.search(r"^generation\d+Player(\d+)", name).group(1)
                        self._agents.append(Agent(int(index), name))
                    if m := re.search(r".*:"+str(self.round)+r"$", line):
                        new_generation = False
                        yield True
                        yield
                        # print(m.group())
                        break
            yield
        f.close()

    def find_agents(self, r):
        f = open(self.file_name, "r")

        for i in f:
            i = i.strip()
            conductor = re.search(r"^initially\(goal_of\((\w*),coordinate\(\)\)=active\):"+str(r)+r"$", i)
            agent = re.search(r"^initially\(fitness_of\((\w*)\)=0\):"+str(r)+r"$", i)
            if conductor:
                name = conductor.group(1)
                index = re.search(r"^coordinator(\d+)", name).group(1)
                self._conductors.append(Agent(int(index), name, conductor=True))
            if agent:
                name = agent.group(1)
                index = re.search(r"^generation\d+Player(\d+)", name).group(1)
                self._agents.append(Agent(int(index), name))
            if re.search(r".*:1", i):
                break
        f.close()

    def get_agents(self):
        return self._agents

    def get_conductors(self):
        return self._conductors
