from execute_command import execute_command
import string

import sys
def execute_group_command(query):
    log = sys.stderr.write

    args = string.split(query, "|")
    group = args[0]
    command = args[1]


    if len(args) == 2:
        if command == "create":
            with open("groups.txt") as group_file:
                lines = group_file.readlines()
            with open("groups.txt", "w") as group_file:
                group_file.writelines(lines)
                group_file.write(group + "|\n")
        if command == "delete":
            with open("groups.txt") as group_file:
                lines = group_file.readlines()
            with open("groups.txt","w") as group_file:
                for line in lines:
                    group_data = string.split(line, "|")
                    group_name = group_data[0]
                    if group != group_name:
                        group_file.write(line)
        if command == "on" or command == "off":
            with open("groups.txt", "r") as group_file:
                lines = group_file.readlines()
                for line in lines:
                    group_data = string.split(line, "|")
                    group_name = group_data[0]
                    if group == group_name:
                        group_endpoints = string.split(group_data[1], ",")
                        group_endpoints = filter(None, group_endpoints)

            if group_endpoints:
                for device in group_endpoints:
                    full_command = "{device}|{command}".format(device=device, command=command)
                    print(execute_command(full_command))
    if len(args) == 3:
        device = args[2]
        if command == "add":
            print "add to group"
            with open("groups.txt") as group_file:
                lines = group_file.readlines()
            with open("groups.txt", "w") as group_file:
                for line in lines:
                    group_data = string.split(line, "|")
                    group_name = group_data[0]
                    if group != group_name:
                        group_file.write(line)
                    else:
                        group_endpoints = string.split(str.strip(group_data[1]), ",")
                        group_endpoints = filter(None, group_endpoints)
                        group_endpoints.append(device)
                        group_file.write(group_name + "|" + string.join(group_endpoints, ",") + "\n")
        if command == "remove":
            print "remove from group"
            with open("groups.txt") as group_file:
                lines = group_file.readlines()
            with open("groups.txt", "w") as group_file:
                for line in lines:
                    group_data = string.split(line, "|")
                    group_name = group_data[0]
                    if group != group_name:
                        group_file.write(line)
                    else:
                        group_endpoints = string.split(str.strip(group_data[1]), ",")
                        group_endpoints = filter(None, group_endpoints)
                        group_endpoints = filter((lambda x: x != device), group_endpoints)
                        log(str(group_endpoints))
                        group_file.write(group_name + "|" + string.join(group_endpoints, ",") + "\n")

