import argparse
import sys
from src.controllers import xml_controller,data_controller

parser = argparse.ArgumentParser(description="use XML editor in CLI mode")
commands =parser.add_subparsers(dest='command', help='Available functionalities',required=True)

verify_arg = commands.add_parser('verify', help= 'verify the structure of the XML provided')
verify_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
verify_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')
verify_arg.add_argument('-f', "--fix", required=False, action='store_true', help='fix the XML file...')

format_arg = commands.add_parser('format', help= 'formatting the xml file to the standard format')
format_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
format_arg.add_argument('-o',"--output",required=True,type=str,help='Path to the output XML file')

json_arg = commands.add_parser('json', help= 'transform the XMl file to a json format file')
json_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
json_arg.add_argument('-o',"--output",required=True,type=str,help='Path to the output XML file')

mini_arg = commands.add_parser('mini', help= 'strip spaces in XML file')
mini_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
mini_arg.add_argument('-o',"--output",required=True,type=str,help='Path to the output XML file')

compress_arg = commands.add_parser('compress', help= 'compressing XML file to specified destination')
compress_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
compress_arg.add_argument('-o',"--output",required=True,type=str,help='Path to the output XML file')

decompress_arg = commands.add_parser('decompress', help= 'decompressing XML file to specified destination')
decompress_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
decompress_arg.add_argument('-o',"--output",required=True,type=str,help='Path to the output XML file')


if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
editor = xml_controller.XMLController()
data_editor = data_controller.DataController()
args = parser.parse_args()
if args.command == 'verify':
    if args.fix and args.output is None:
        print("invalid usage")

    ack = editor.validate_xml_structure(args.input)
    if ack[0]:
        print(ack[1])
    else:
        print(f"error occurred, {ack[2]}")

if args.command == 'format':
    ack = editor.format_xml_file(file_path=args.input ,dest_path=args.output)
    if ack[0]:
        print(ack[1])
    else:
        print(f"error occurred -> {ack[2]}")

if args.command == 'json':
    ack = editor.parse_xml_file(args.input)
    if ack[0]:
        xml_data = editor.get_xml_data()
        data_editor.set_xml_data(xml_data)
        summary = data_editor.export_to_json(file_path=args.output)

        if summary[0]:
            print(summary[1])
    else:
        print("invalid argument")

