import re
from .Agent import Agent


class EvolutionaryTournament:
    def __init__(self, file_name):
        self.file_name = file_name
        self.chunks = None
        self.total_rounds = 0
        self.total_time_stamp = 0
        self.total_giving_encounters = 0
        self.total_gossip_encounters = 0
        self.total_generations = None
        self.time_stamp = 2
        self.giving_encounters = 0
        self.gossip_encounters = 0
        self.round = 0
        self.generation = 1
        self.encounter_type = "Gossip"
        self._agents = []
        self._conductor = None
        self.giver_agent = None
        self.receiver_agent = None
        self.gossiping_agents = []
        self.cooperate = None
        self.gossip = False
        self.belief_lines = []
        self.belief = {"time": [], "agents": {"overall": []}}
        self.load_file()

    def load_file(self):
        file = open(self.file_name)
        f = file.read()
        self.chunks = re.split("new_generation.*", f)
        self.chunks = [list(filter(''.__ne__, chunk.split("\n"))) for chunk in self.chunks]
        self.total_generations = len(self.chunks)
        file.close()

        agents = re.search(r"^:-dynamic (((\w*)/2[,\.])+)$", self.chunks[0][3])
        agents = agents.group(1).strip("/2.").split("/2,")
        for agent in agents:
            if cond := re.search(r"^conductor(\d+)", agent):
                index = cond.group(1)
                name = "conductor" + index
                self._conductor = Agent(int(index), name, "conductor")
            else:
                index = re.search(r"^generation(\d+)Player(\d+)", agent)
                generation = index.group(1)
                index = index.group(2)
                name = "generation" + generation + "player" + index
                self._agents.append(Agent(int(index), name))
                self.belief["agents"][name] = []

        for line in reversed(self.chunks[0]):
            if m := re.search(r"^.*\),(\d+)\)\.$", line):
                self.total_time_stamp = int(m.group(1))
                self.total_rounds = int(self.total_time_stamp / 3)
                break

    def find_agents(self, line):
        agent = re.search(r"^role_of\((\w*),player\).$", line)
        if agent:
            name = agent.group(1)
            index = re.search(r"^generation" + str(self.generation) + r"Player(\d+)", name).group(1)
            self._agents.append(Agent(int(index), name))

    def start(self):
        f = open(self.file_name, "r")

        cont = True
        new_generation = False
        while cont:
            for line in f:
                if line != "\n":
                    line = line.strip()
                    if not new_generation:
                        if re.search(r"new_generation.*", line):
                            new_generation = True
                            self._agents = []
                            self.round = 0
                            self.generation += 1
                            self.giving_encounters = 0
                            self.gossip_encounters = 0
                        elif re.search(r"^happens_at\(perform\(.*inform.*\)," + str(self.time_stamp) + r"\)\.$", line):
                            self.round += 1
                            self.perform_line(line)
                            break
                        self.gossip = False
                        self.cooperate = None
                        self.gossiping_agents = []
                        self.giver_agent = self.receiver_agent = None
                    else:
                        self.find_agents(line)
                        if re.search(r".*," + str(self.time_stamp) + r"\)\.$", line):
                            new_generation = False
                            yield True
                            yield
                            self.perform_line(line)
                            break
            else:
                yield False
            yield
            self.time_stamp += 3
        f.close()

    def perform_line(self, line):
        if m := re.search(
                r"^happens_at\(perform\(actuator(.*),inform\(\1,\[(.*),.*\],generation1encounter\d+,(\w+)\(.*\)\)\)," +
                str(self.time_stamp) + r"\)\.$", line):
            if m.group(3) == "gossip":
                self.encounter_type = "Gossip"
                index1 = int(re.search(r"^generation\d+Player(\d+)", m.group(1)).group(1)) - 1
                index2 = int(re.search(r"^generation\d+Player(\d+)", m.group(2)).group(1)) - 1
                self.gossiping_agents = [self._agents[index1], self._agents[index2]]
                self.gossip_encounters += 1
                self.gossip = True
            elif m.group(3) == ("defect" or "cooperate"):
                self.encounter_type = "Giving"
                index1 = int(re.search(r"^generation\d+Player(\d+)", m.group(1)).group(1)) - 1
                index2 = int(re.search(r"^generation\d+Player(\d+)", m.group(2)).group(1)) - 1
                self.giver_agent = self._agents[index1]
                self.receiver_agent = self._agents[index2]
                self.giving_encounters += 1
                self.cooperate = m.group(3) == "cooperate"

            print(m.group(1), m.group(2), m.group(3))

        # if m := re.search(r"^perform\(.*request.*giving_encounter\(\w*,(\w*),(\w*)\).*:" + str(self.time_stamp) + r"$",
        #                   line):
        #     if self.encounter_type == "Gossip":
        #         self.round += 1
        #         self.giving_encounters = 0
        #         self.gossip_encounters = 0
        #     agent1 = m.group(1)
        #     agent2 = m.group(2)
        #     index1 = int(re.search(r"^generation\d+Player(\d+)", agent1).group(1)) - 1
        #     index2 = int(re.search(r"^generation\d+Player(\d+)", agent2).group(1)) - 1
        #     self.giver_agent = self._agents[index1]
        #     self.receiver_agent = self._agents[index2]
        #     self.encounter_type = "Giving"
        #     self.giving_encounters += 1
        # elif m := re.search(
        #         r"^perform\(.*request.*gossip_encounter\(\w*,(\w*),(\w*)\).*:" + str(self.time_stamp) + r"$", line):
        #     agent1 = m.group(1)
        #     agent2 = m.group(2)
        #     index1 = int(re.search(r"^generation\d+Player(\d+)", agent1).group(1)) - 1
        #     index2 = int(re.search(r"^generation\d+Player(\d+)", agent2).group(1)) - 1
        #     self.gossiping_agents = [self._agents[index1], self._agents[index2]]
        #     self.encounter_type = "Gossip"
        #     self.giving_encounters = 0
        #     self.gossip_encounters += 1
        # elif re.search(r"^perform\(.*inform.*cooperate\((\w*)\).*:" + str(self.time_stamp) + r"$", line):
        #     self.cooperate = True
        #     self.encounter_type = "Giving"
        #     # self.giving_encounters += 1
        # elif re.search(r"^perform\(.*inform.*defect\((\w*)\).*:" + str(self.time_stamp) + r"$", line):
        #     self.cooperate = False
        #     self.encounter_type = "Giving"
        #     # self.giving_encounters += 1
        # elif re.search(r"^perform\(.*inform.*gossip\(.*\).*:" + str(self.time_stamp) + r"$", line):
        #     self.gossip = True
        #     self.encounter_type = "Gossip"
        #     # self.gossip_encounters += 1
        # elif re.search(r"^perform\(.*inform-done.*giving.*:" + str(self.time_stamp) + r"$", line):
        #     self.receiver_agent = None
        #     self.giver_agent = None
        #     self.cooperate = None
        #     self.encounter_type = "Giving"
        #     # self.giving_encounters += 1
        # elif re.search(r"^perform\(.*inform-done.*gossip.*:" + str(self.time_stamp) + r"$", line):
        #     self.gossiping_agents = []
        #     self.gossip = False
        #     self.encounter_type = "Gossip"
        #     # self.gossip_encounters += 1

    def get_agents(self):
        return self._agents

    def get_conductor(self):
        return self._conductor
