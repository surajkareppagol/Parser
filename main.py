import sys
from xml_parser import xml_to_json_parser

if len(sys.argv) < 2:
    print("Usage: python main.py <file_path>\n\n-o = output file name")
    sys.exit(1)

if sys.argv[1] == "--help":
    print("Usage: python main.py <file_path>\n\n-o = output file name")
    sys.exit(0)

try:
    output_data = ''
    output_file_name = 'output.json'
    with open(sys.argv[1], "rb") as xml_file:
        data = xml_file.readlines()
    output_data = xml_to_json_parser(data)

    if len(sys.argv) > 3 and '-o' in sys.argv:
        output_file_name = sys.argv[3]
    with open(output_file_name, "w") as output_file:
        output_file.write(output_data)

    print(
        f"Success: Parsed '{sys.argv[1]}' file and generated '{output_file_name}' file.")

except FileNotFoundError:
    print("Usage: python main.py <file_path>\n\n-o = output file name")
    sys.exit(1)
