import re
import time
from components import Agent

s = time.time()
# new file read
file = open("historyexp1-2.pl").read()
chunks = re.split("new_generation.*", file)
chunks = [list(filter(''.__ne__, chunk.split("\n"))) for chunk in chunks]

self_agents = []
number_of_rounds = 0

for line in chunks[0]:
    agents = re.search(r"^:-dynamic (((\w*)/2[,\.])+)$", line)
    if agents:
        agents = agents.group(1).strip("/2.").split("/2,")
        for agent in agents:
            if cond := re.search(r"^conductor(\d+)", agent):
                index = cond.group(1)
                name = "conductor" + index
                conductor = True
            else:
                index = re.search(r"^player(\d+)", agent).group(1)
                name = "generation" + index + "Player" + index
                conductor = False
            self_agents.append(Agent(int(index), name, conductor=conductor))


