import re
import time

from .Agent import Agent


class Tournament:
    def __init__(self, file_name="./historyexp1.pl"):
        self.file_name = file_name
        self.chunks = None
        self.total_rounds = 0
        self.time_stamp = 1
        self.total_time_stamp = 0
        self.total_cooperation = 0
        self.round = 0
        self.generation = 0
        self.encounter_type = "Gossip"
        self._agents = []
        self._conductor = None
        self.player1 = None
        self.player2 = None
        self.cooperate = None
        self.belief_lines = []
        self.belief = {"time": [], "agents": {"overall": []}}
        self.load_file()
        self._agents_data = dict()

    def load_file(self):
        file = open(self.file_name)
        f = file.read()
        self.chunks = re.split("new_generation.*", f)
        self.chunks = [list(filter(''.__ne__, chunk.split("\n"))) for chunk in self.chunks]
        file.close()

        agents = re.search(r"^:-dynamic (((\w*)/2[,\.])+)$", self.chunks[0][0])
        agents = agents.group(1).strip("/2.").split("/2,")
        for agent in agents:
            if cond := re.search(r"^conductor(\d+)", agent):
                index = cond.group(1)
                name = "conductor" + index
                self._conductor = Agent(int(index), name, conductor=True)
            else:
                index = re.search(r"^player(\d+)", agent).group(1)
                name = "player" + index
                self._agents.append(Agent(int(index), name))
                self.belief["agents"][name] = []

        # temp = self._agents.copy()
        # for agent in self._agents:
        #     temp.append(Agent(agent.index + len(self._agents), "twin" + agent.name))
        #     self._agents_data[agent.name] = []
        #     self._agents_data[temp[-1].name] = []
        # self._agents = temp

        for line in reversed(self.chunks[0]):
            if m := re.search(r"^.*\),(\d+)\)\.$", line):
                self.total_time_stamp = int(m.group(1))
                self.total_rounds = int(self.total_time_stamp / 4)
                break

        file = open(self.file_name)
        self.belief_lines = [f.split("\n")[0] for f in file]
        self.belief_lines = [line for line in self.belief_lines if re.search(r"^conductor1\(fitness.*\.$", line)]
        file.close()
        self.belief["time"].append(0)
        self.update_belief()

    def update_belief(self):
        overall = 0
        for agent in self._agents:
            for belief in self.belief_lines:
                if m := re.search(r"^conductor1\(fitness\(" + agent.name + r"\)=(\d*),\[(\d*),(\d*)\]\)\.$", belief):
                    if self.time_stamp in range(int(m.group(2)), int(m.group(3))):
                        self.belief["agents"][agent.name].append(m.group(1))
                        overall += int(m.group(1))
                        break
            else:
                self.belief["agents"][agent.name].append(self.belief["agents"][agent.name][-1])
                overall += int(self.belief["agents"][agent.name][-1])
        self.belief["agents"]["overall"].append(overall)

    def run(self):
        for line in self.chunks[0]:
            if re.search(r"^happens_at\(perform\(.*\)," + str(self.time_stamp) + r"\)\.$", line) and self.round < self.total_rounds:
                self.belief["time"].append(self.belief["time"][-1] + 1)
                self.update_belief()
                if self.perform_line(line):
                    yield

    def perform_line(self, line):
        if m := re.search(r"^happens_at\(perform\(actuator" + self._conductor.name + r",performEnc\(" +
                          self._conductor.name + r",\[(.*)\].*\)," + str(self.time_stamp) + r"\)\.$", line):
            player = m.group(1)
            if i := re.search(r"^twinplayer(.*)", player):
                p = self._agents[int(i.group(1)) - 1]
                player = Agent(p.index, "twin" + p.name)
            else:
                i = re.search(r"^player(.*)", player).group(1)
                player = self._agents[int(i) - 1]
            if not self.player1:
                self.time_stamp += 1
                self.player1 = player
                self.round += 1
                return True
            else:
                self.player2 = player
                return True
        elif m := re.search(r"^happens_at\(perform\(actuator" + self.player1.name + r",inform\(" + self.player1.name +
                            r",\[.*\],encounter\d+,(.*)\(" + self.player2.name + "\)\)\)," + str(self.time_stamp) +
                            r"\)\.$", line):
            if m.group(1) == "cooperate" and self.cooperate is not False:
                self.cooperate = True
            else:
                self.cooperate = False
            self.time_stamp += 1
        elif m := re.search(r"^happens_at\(perform\(actuator" + self.player2.name + r",inform\(" + self.player2.name +
                r",\[.*\],encounter\d+,(.*)\(" + self.player1.name + "\)\)\)," + str(self.time_stamp) + r"\)\.$", line):
            if m.group(1) == "cooperate" and self.cooperate is not False:
                self.cooperate = True
            else:
                self.cooperate = False
            self.time_stamp += 1
            return True
        elif m := re.search(r"^happens_at\(perform\(actuator" + self._conductor.name + r",resultEnc\(" +
                            self._conductor.name + r",\[(.*)\].*\)," + str(self.time_stamp) + r"\)\.$", line):
            self.time_stamp += 1
            self.player1 = self.player2 = None
            self.cooperate = None
            return True

    def get_agents(self):
        return self._agents

    def get_agents_data(self):
        return self.belief

    def get_conductor(self):
        return self._conductor
