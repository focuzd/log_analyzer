import argparse
import parser 
import os
import sys
import utils

p = argparse.ArgumentParser()
p.add_argument('--file', help='Path to input log file')
p.add_argument('--level', help='Level to be filtered in log file')
p.add_argument('--format', choices=['log', 'csv'], help='Format of output file')
p.add_argument('--tag_env', action='store_true', help='Add APP_ENV tag to output file')
p.add_argument('--max_lines', type=int, help='Specify the maximum number of lines in output')

args = p.parse_args()

if not args.file:
    print("Error: File not specified.")
    sys.exit(1)

if not os.path.exists(args.file):
    print("Error: File does not exist.")
    sys.exit(2)

if not args.level:
    args.level = 'all'

if not args.tag_env:
    args.tag_env = False

if not args.max_lines:
    args.max_lines = 1000000

input_log = parser.LogAnalyzer(args.file, args.max_lines, args.tag_env, args.level)

input_log.count_Levels()

if args.format:
    input_log.write_summary(args.format)

else:
    input_log.write_summary()

print("Summary generated successfully.")
print(f"Path to output files : {utils.ensure_output_dir()}")
