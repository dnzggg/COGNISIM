import re
from components.Agent import Agent
import os

file_name = "./historyexp1.pl"
file = open(file_name)
lines = [f.split("\n")[0] for f in file]
file.close()

a = re.search(r"^:-dynamic (((\w*)/2[,\.])+)$", lines.pop(0))
a = a.group(1).strip("/2.").split("/2,")
agents = []
for agent in a:
    if cond := re.search(r"^conductor(\d+)", agent):
        index = cond.group(1)
        name = "conductor" + index
        conductor = Agent(int(index), name, conductor=True)
    else:
        index = re.search(r"^player(\d+)", agent).group(1)
        name = "player" + index
        agents.append(Agent(int(index), name))

try:
    os.mkdir(file_name.strip("./pl"))
except FileExistsError:
    pass

os.chdir(file_name.strip("./pl"))

for agent in [*agents, conductor]:
    try:
        os.mkdir(agent.name)
        os.chdir(agent.name)
    except FileExistsError:
        os.chdir(agent.name)
    file = open("fluents.pl", "w")
    file.write(":-dynamic " + agent.name + "/2.\n")
    file.close()
    file = open("events.pl", "w")
    file.write(":-dynamic " + agent.name + "/2.\n")
    file.close()
    os.chdir("..")

for line in lines:
    for agent in [*agents, conductor]:
        if re.search(r"^role_of\(" + agent.name + r",(.*)\.$", line):
            file = open(agent.name + "/fluents.pl", "a")
            file.write(line + "\n")
            file.close()
            break
        elif re.search(r"^rule\(" + agent.name + r",(.*)\.$", line):
            file = open(agent.name + "/fluents.pl", "a")
            file.write(line + "\n")
            file.close()
            break
        elif re.search(r"^" + agent.name + r"\(.*\)\.$", line):
            file = open(agent.name + "/fluents.pl", "a")
            file.write(line + "\n")
            file.close()
            break
        elif re.search(r"^happens_at\(in\(" + agent.name + r",(.*)\.$", line):
            file = open(agent.name + "/events.pl", "a")
            file.write(line + "\n")
            file.close()
            break
        elif re.search(r"^happens_at\(initially\((.*)" + agent.name + r"(.*)\.$", line):
            file = open(agent.name + "/events.pl", "a")
            file.write(line + "\n")
            file.close()
            break
