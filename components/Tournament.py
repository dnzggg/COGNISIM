import re
import time

from .Agent import Agent


class Tournament:
    def __init__(self, file_name="./trail1eventHistory.pl"):
        self.file_name = file_name
        self.chunks = None
        self.total_rounds = 0
        self.total_giving_encounters = 0
        self.total_gossip_encounters = 0
        self.total_generations = None
        self.time_stamp = 0
        self.total_time_stamp = 0
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
        self.load_file()

    def load_file(self):
        file = open(self.file_name)
        f = file.read()
        self.chunks = re.split("new_generation.*", f)
        self.chunks = [list(filter(''.__ne__, chunk.split("\n"))) for chunk in self.chunks]

        twice = False

        for line in self.chunks[0]:
            self.find_agents(line, 0)
            if re.search(r"^perform\(.*inform-done.*giving.*:\d*$", line):
                if twice:
                    break
                self.total_giving_encounters += 1
            elif re.search(r"^perform\(.*inform-done.*gossip.*:\d*$", line):
                self.total_gossip_encounters += 1
                twice = True

        self.total_rounds = int((int(self.chunks[0][-1].split(":")[1]) / 3) / (self.total_giving_encounters + self.total_gossip_encounters))
        self.total_generations = len(self.chunks)
        self.total_time_stamp = self.total_generations * int(self.chunks[0][-1].split(":")[1]) / 3
        file.close()

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

    def run(self, generation=None, time_stamp=None):
        if generation and time_stamp:
            self.time_stamp = time_stamp
            self.generation = generation
        for chunk in self.chunks[generation:]:
            for line in chunk:
                if re.search(r"^perform\(.*:" + str(self.time_stamp) + "$", line):
                    self.perform_line(line)
                    yield
            # find new agents

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
