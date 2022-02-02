import re
from .Agent import Agent


class Tournament:
    def __init__(self, file_name="./trail1eventHistory.pl"):
        self.file_name = file_name
        self.total_rounds = 0
        self.total_giving_encounters = 0
        self.total_gossip_encounters = 0
        self.total_generations = None
        self.time_stamp = 0
        self.giving_encounters = 0
        self.gossip_encounters = 0
        self.round = 0
        self.generation = 0
        self.encounter_type = "Gossip"
        self._agents = []
        self._conductors = []
        self.giver_agent = None
        self.receiver_agent = None
        self.gossiping_agents = []
        self.cooperate = None
        self.gossip = False
        self.find_initial_agents()

    def find_initial_agents(self):
        f = open(self.file_name, "r")
        giving = False

        for line in f:
            if line != "\n":
                line = line.strip()
                self.find_agents(line, 0)
                if re.search(r"^new_generation\(\d*\):(\d*)", line):
                    break
                if re.search(r"^perform\(.*inform-done.*giving.*:\d*$", line):
                    if not giving:
                        self.total_rounds += 1
                    self.total_giving_encounters += 1
                    giving = True
                elif re.search(r"^perform\(.*inform-done.*gossip.*:\d*$", line):
                    self.total_gossip_encounters += 1
                    giving = False
        f.close()

        self.total_gossip_encounters = int(self.total_gossip_encounters / self.total_rounds)
        self.total_giving_encounters = int(self.total_giving_encounters / self.total_rounds)

        f = open(self.file_name, "r")

        for line in reversed(list(f)):
            if line != "\n":
                line = line.strip()
                if m := re.search(r"^new_generation\((\d*)\):(\d*)", line):
                    self.total_generations = int(m.group(1))
                    break
        f.close()

    def find_agents(self, line, r):
        conductor = re.search(r"^initially\(goal_of\((\w*),coordinate\(\)\)=active\):" + str(r) + r"$", line)
        agent = re.search(r"^initially\(fitness_of\((\w*)\)=0\):" + str(r) + r"$", line)
        if conductor:
            name = conductor.group(1)
            index = re.search(r"^coordinator(\d+)", name).group(1)
            self._conductors.append(Agent(int(index), name, conductor=True))
        if agent:
            name = agent.group(1)
            index = re.search(r"^generation\d+Player(\d+)", name).group(1)
            self._agents.append(Agent(int(index), name))

    def start(self):
        f = open(self.file_name, "r")

        cont = True
        new_generation = False
        while cont:
            self.time_stamp += 1
            for line in f:
                if line != "\n":
                    line = line.strip()
                    if not new_generation:
                        if re.search(r"^new_generation\(\d*\):\d*", line):
                            new_generation = True
                            self._agents = []
                            self.round = 0
                            self.generation += 1
                            self.giving_encounters = 0
                            self.gossip_encounters = 0
                        elif re.search(r"^perform\(.*:" + str(self.time_stamp) + r"$", line):
                            self.perform_line(line)
                            break
                    else:
                        self.find_agents(line, self.time_stamp - 1)
                        if re.search(r".*:" + str(self.time_stamp) + r"$", line):
                            new_generation = False
                            yield True
                            yield
                            self.perform_line(line)
                            break
            else:
                yield False
            yield
        f.close()

    def perform_line(self, line):
        if m := re.search(r"^perform\(.*request.*giving_encounter\(\w*,(\w*),(\w*)\).*:" + str(self.time_stamp) + r"$", line):
            if self.encounter_type == "Gossip":
                self.round += 1
                self.giving_encounters = 0
                self.gossip_encounters = 0
            agent1 = m.group(1)
            agent2 = m.group(2)
            index1 = int(re.search(r"^generation\d+Player(\d+)", agent1).group(1)) - 1
            index2 = int(re.search(r"^generation\d+Player(\d+)", agent2).group(1)) - 1
            self.giver_agent = self._agents[index1]
            self.receiver_agent = self._agents[index2]
            self.encounter_type = "Giving"
            self.giving_encounters += 1
        elif m := re.search(r"^perform\(.*request.*gossip_encounter\(\w*,(\w*),(\w*)\).*:" + str(self.time_stamp) + r"$", line):
            agent1 = m.group(1)
            agent2 = m.group(2)
            index1 = int(re.search(r"^generation\d+Player(\d+)", agent1).group(1)) - 1
            index2 = int(re.search(r"^generation\d+Player(\d+)", agent2).group(1)) - 1
            self.gossiping_agents = [self._agents[index1], self._agents[index2]]
            self.encounter_type = "Gossip"
            self.giving_encounters = 0
            self.gossip_encounters += 1
        elif re.search(r"^perform\(.*inform.*cooperate\((\w*)\).*:" + str(self.time_stamp) + r"$", line):
            self.cooperate = True
            self.encounter_type = "Giving"
            # self.giving_encounters += 1
        elif re.search(r"^perform\(.*inform.*defect\((\w*)\).*:" + str(self.time_stamp) + r"$", line):
            self.cooperate = False
            self.encounter_type = "Giving"
            # self.giving_encounters += 1
        elif re.search(r"^perform\(.*inform.*gossip\(.*\).*:" + str(self.time_stamp) + r"$", line):
            self.gossip = True
            self.encounter_type = "Gossip"
            # self.gossip_encounters += 1
        elif re.search(r"^perform\(.*inform-done.*giving.*:" + str(self.time_stamp) + r"$", line):
            self.receiver_agent = None
            self.giver_agent = None
            self.cooperate = None
            self.encounter_type = "Giving"
            # self.giving_encounters += 1
        elif re.search(r"^perform\(.*inform-done.*gossip.*:" + str(self.time_stamp) + r"$", line):
            self.gossiping_agents = []
            self.gossip = False
            self.encounter_type = "Gossip"
            # self.gossip_encounters += 1

    def get_agents(self):
        return self._agents

    def get_conductors(self):
        return self._conductors
