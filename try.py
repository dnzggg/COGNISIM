import re
import time
from components import Agent

s = time.time()
# new file read
file = open("belief_hist.pl").read()
chunks = re.split("new_generation.*", file)
chunks = [list(filter(''.__ne__, chunk.split("\n"))) for chunk in chunks]

self_players = []
self_conductor = None
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
                self_conductor = conductor
            else:
                index = re.search(r"^player(\d+)", agent).group(1)
                name = "player" + index
                self_players.append(Agent(int(index), name))
        break

for line in reversed(chunks[0]):
    if m := re.search(r"^.*\),(\d+)\)\.$", line):
        ts = m.group(1)
        break

temp = self_players.copy()
for s in self_players:
    temp.append(Agent(s.index + len(self_players), "twin" + s.name))
self_players = temp
print([s.name for s in self_players])


def perform_line(ln, ts, p1, p2, coop):
    if m := re.search(
            r"^happens_at\(perform\(actuator" + conductor.name + r",performEnc\(" + conductor.name + r",\[(.*)\].*\)," + str(
                    ts) + r"\)\.$", ln):
        player = m.group(1)
        if i := re.search(r"^twinplayer(.*)", player):
            player = self_players[int(i.group(1)) + int(len(self_players) / 2) - 1]
        else:
            i = re.search(r"^player(.*)", player).group(1)
            player = self_players[int(i) - 1]
        if not p1:
            ts += 1
            p1 = player
        else:
            p2 = player
        print("Perform " + player.name)
    elif m := re.search(
            r"^happens_at\(perform\(actuator" + p1.name + r",inform\(" + p1.name + r",\[.*\],encounter\d+,(.*)\(" + p2.name + "\)\)\)," + str(
                ts) + r"\)\.$", ln):
        if m.group(1) == "cooperate" and coop is not False:
            coop = True
        else:
            coop = False
        print(coop)
        ts += 1
    elif m := re.search(
            r"^happens_at\(perform\(actuator" + p2.name + r",inform\(" + p2.name + r",\[.*\],encounter\d+,(.*)\(" + p1.name + "\)\)\)," + str(
                    ts) + r"\)\.$", ln):
        if m.group(1) == "cooperate" and coop is not False:
            coop = True
        else:
            coop = False
        print(coop)
        ts += 1
    elif m := re.search(
            r"^happens_at\(perform\(actuator" + conductor.name + r",resultEnc\(" + conductor.name + r",\[(.*)\].*\)," + str(
                    ts) + r"\)\.$", ln):
        ts += 1
        p1 = p2 = None
        coop = None
    return ts, p1, p2, coop


time_stamp = 1
player1 = None
player2 = None
cooperate = None
for line in chunks[0]:
    if re.search(r"^happens_at\(perform\(.*\)," + str(time_stamp) + r"\)\.$", line):
        # 5 different performs
        # conductor performEnc to player 1
        # conductor performEnc to player 2
        # player 1 inform decision to conductor
        # player 2 inform decision to conductor
        # conductor resultEnc to player 1 and 2
        time_stamp, player1, player2, cooperate = perform_line(line, time_stamp, player1, player2, cooperate)

