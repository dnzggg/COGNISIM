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
                conductor = agent = Agent(int(index), name, conductor=True)
            else:
                index = re.search(r"^player(\d+)", agent).group(1)
                name = "player" + index
                agent = Agent(int(index), name)
                self_agents.append(Agent(int(index) + 3, "twin" + name))
            self_agents.append(agent)
        break


def perform_line(line, time_stamp, player1, player2):
    if m := re.search(
            r"^happens_at\(perform\(actuator" + conductor.name + r",performEnc\(" + conductor.name + r",\[(.*)\].*\)," + str(
                    time_stamp) + r"\)\.$", line):
        if not player1:
            player1 = m.group(1)
            time_stamp += 1
        else:
            player2 = m.group(1)
        print("Perform " + m.group(1))
    elif m := re.search(
            r"^happens_at\(perform\(actuator" + player1 + r",inform\(" + player1 + r",\[.*\],encounter\d+,(.*)\)\)," + str(
                    time_stamp) + r"\)\.$", line):
        print(m.group(1))
        time_stamp += 1
    elif m := re.search(
            r"^happens_at\(perform\(actuator" + player2 + r",inform\(" + player2 + r",\[.*\],encounter\d+,(.*)\)\)," + str(
                    time_stamp) + r"\)\.$", line):
        print(m.group(1))
        time_stamp += 1
    elif m := re.search(
            r"^happens_at\(perform\(actuator" + conductor.name + r",resultEnc\(" + conductor.name + r",\[(.*)\].*\)," + str(
                    time_stamp) + r"\)\.$", line):
        time_stamp += 1
        player1 = player2 = None
    return time_stamp, player1, player2


time_stamp = 1
player1 = None
player2 = None
for line in chunks[0]:
    if re.search(r"^happens_at\(perform\(.*\)," + str(time_stamp) + r"\)\.$", line):
        # 5 different performs
        # conductor performEnc to player 1
        # conductor performEnc to player 2
        # player 1 inform decision to conductor
        # player 2 inform decision to conductor
        # conductor resultEnc to player 1 and 2
        time_stamp, player1, player2 = perform_line(line, time_stamp, player1, player2)

