import sys
import json


xml_arr = []
xml_tags_and_values = ''
xml_object_list = []
xml_tag_stack = []
xml_to_json_data = {}
xml_current_object = {}
xml_root_tag = ''
xml_object_temp_key = ''

is_stack_updated = False


def get_tag_and_value(line):
    # Because the line starts with b'<?xml ....
    start_index = 2
    if "\\n\'" in line:
        end_index = len(line) - 3
    else:
        end_index = len(line) - 1
    xml_opening_tag = ''
    xml_value = ''
    xml_closing_tag = ''

    for i in range(start_index, end_index):
        if line[i] == '<' or line[i] == ' ':
            continue
        elif line[i] == '>':
            start_index = i + 1
            break
        else:
            xml_opening_tag += line[i]

    for i in range(start_index, end_index):
        if line[i] == '<':
            start_index = i + 1
            break
        else:
            xml_value += line[i]

    for i in range(start_index, end_index):
        if line[i] == '<':
            continue
        elif line[i] == '>':
            break
        else:
            xml_closing_tag += line[i]

    return [xml_opening_tag, xml_value, xml_closing_tag]


def insertObject():
    preivious_object = xml_object_list[0]
    temp_object = xml_object_list.pop()
    for key_value in preivious_object.keys():
        xml_object_temp_key = key_value
    temp_object[tag][xml_object_temp_key] = preivious_object[xml_object_temp_key]
    xml_object_list.append(temp_object)
    del xml_object_list[0]


def insertIntoJson():
    temp_object = xml_object_list.pop()
    for key_value in temp_object.keys():
        xml_object_temp_key = key_value
    xml_to_json_data[xml_root_tag][xml_object_temp_key] = temp_object[xml_object_temp_key]
    print(xml_to_json_data)


if len(sys.argv) < 2:
    print("Usage: python xml_parser.py <file_path>")
    sys.exit(1)

if sys.argv[1] == "--help":
    print("Usage: python3 xml_parser.py <file-path> or --help\nNote: The XML file should not contain same tags on the same level.")
    sys.exit(0)

try:
    with open(sys.argv[1], "rb") as xml_file:
        data = xml_file.readlines()
        for line in data:
            str_line = str(line)
            if '<?' in str_line or '<!--' in str_line or '-->' in str_line:
                continue

            if '<' in str_line:
                xml_opening_tag, xml_value, xml_closing_tag = get_tag_and_value(
                    str_line)

                # Identify Root Tag
                if '/' not in xml_opening_tag and len(xml_closing_tag) == 0 and len(xml_value) == 0:
                    xml_tag_stack.append(xml_opening_tag)
                    is_stack_updated = True
                    if is_stack_updated and len(xml_tag_stack) > 2:
                        # Add a placeholder "{["
                        xml_tags_and_values += '{['
                    if len(xml_tag_stack) == 1:
                        xml_root_tag = xml_tag_stack[0]
                        xml_to_json_data[xml_root_tag] = {}

                # Identify Children Tags
                if len(xml_closing_tag) > 0 and '/' not in xml_opening_tag:
                    is_stack_updated = False
                    # Add placeholders "{[" and "____"
                    xml_tags_and_values += f"{xml_opening_tag}____{xml_value}]]"

                # Identify Closing Tags
                if '/' in xml_opening_tag and len(xml_closing_tag) == 0:
                    tag = xml_tag_stack.pop()
                    xml_current_object[tag] = {}
                    for item in xml_tags_and_values.split('{[')[-1].split(']]'):
                        if '____' in item:
                            value = item.split('____')[1]
                            if value.isdigit():
                                value = int(value)
                            elif ',' in value and len(value.split(',')) == value.count(',') - 1:
                                for element in value.split(','):
                                    if element.strip().isdigit():
                                        xml_arr.append(int(element.strip()))
                                    else:
                                        xml_arr.append(element)
                                value = xml_arr
                            xml_current_object[tag][item.split('_')[0]] = value
                    xml_object_list.append(xml_current_object)

                    if len(xml_object_list) > 1 and len(xml_tag_stack) > 1:
                        insertObject()

                    elif len(xml_tag_stack) == 1:
                        if (len(xml_object_list) == 2):
                            insertObject()
                            insertIntoJson()
                        else:
                            insertIntoJson()

                    xml_current_object = {}
                    xml_tags_and_values = '+'.join(
                        xml_tags_and_values.split('+')[:-1])
                    continue

    with open("output.json", "w") as output_json_file:
        output_json_file.write(json.dumps(xml_to_json_data))

    print("Success: Generated \"output.json\" file.")

except FileNotFoundError:
    print("Error: Please provide a valid file name.")
    sys.exit(1)
