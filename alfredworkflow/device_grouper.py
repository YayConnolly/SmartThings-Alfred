import string
import sys
import re
from alfred import Feedback

def device_grouper(query=""):
    feedback = Feedback()
    args = string.split(query.lstrip(), " ")
    title_template = "{group} {action} {device_name}"
    # ensure groups.txt exists
    group_file = open("groups.txt", "a"); group_file.close()
    with open("groups.txt", "r") as group_file:
      groups = {}
      for group_data_string in group_file.readlines():
        group_data = string.split(group_data_string.strip(), "|")
        group_name = group_data[0].strip()
        devices = string.split(group_data[1], ",")
        groups[group_name] = devices

    group = args[0]
    if len(args) == 1:
      # add option to create this as a new group if doesn't exist
      if len(group) == 0:
        title = title_template.format(group="[group]", action="[action]", device_name="[device_name]")
        feedback.addItem(title=title, subtitle=title, valid=False,
                         autocomplete=" ")
      if len(group) > 0 and group not in groups:
        title = "Create group: {group}".format(group=group)
        arg = "{group}|create".format(group=group)
        feedback.addItem(title=title, subtitle=title, valid=True, arg=arg,
                         autocomplete=" " + group + " create")
      for existing_group in groups:
        # filter for entered group
        if not group.lower() in existing_group.lower():
          continue
        title = title_template.format(group=existing_group, action="[action]", device_name="[device_name]")
        feedback.addItem(title=title, subtitle=title, valid=False,
                         autocomplete=" " + existing_group + " ")
      return feedback


    action = args[1]
    allowed_device_actions = ['add', 'remove']
    allowed_group_actions = ['create', 'delete', 'on', 'off']
    allowed_actions = allowed_group_actions + allowed_device_actions
    if len(args) > 2:
        if action not in allowed_actions:
            return ''
    if len(args) == 2:
        for device_action in allowed_device_actions:
            # filtering
            if not action in device_action:
                continue
            title = title_template.format(group=group, action=device_action, device_name="[device_name]")
            feedback.addItem(title=title, subtitle=title, valid=False,
                             autocomplete=" " + group + " " + device_action + " ")
        for group_action in allowed_group_actions:
            if not action in group_action:
                continue
            title = "{group} {action}".format(group=group, action=group_action)
            arg = "{group}|{action}".format(group=group, action=group_action)
            autocomplete = " " + group + " " + group_action
            feedback.addItem(title=title, subtitle=title, valid=True, autocomplete=autocomplete, arg=arg)
        return feedback
    elif len(args) > 2:
        device_filter = ' '.join(args[2:])
        with open("devices.txt") as device_file:
          for device_data_string in device_file.readlines():
              device_data = string.split(device_data_string, "|")
              device_endpoint = device_data[0].strip()
              device_label = device_data[1].strip()

              if not device_filter.lower() in device_label.lower():
                  continue

              if action == "add":
                # skip existing
                if device_endpoint in groups[group]:
                  continue

              if action == "remove":
                # skip if not in group
                if device_endpoint not in groups[group]:
                  continue

              title = "{group} {action} {device_label}".format(action=action, device_label=device_label, group=group)
              autocomplete = " " + group + " " + action + " " + device_label
              arg = "{group}|{action}|{device_endpoint}".format(group=group,
                                                          action=action,
                                                          device_endpoint=device_endpoint)
              feedback.addItem(title=title, subtitle=title, valid=True, arg=arg, autocomplete=autocomplete)
        return feedback

