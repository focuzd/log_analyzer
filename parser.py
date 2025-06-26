import re
import os
import csv
import utils

class LogAnalyzer:
    def __init__(self, filename, max_lines, add_env_tag, level):
        self.logfile = filename
        self.searchKeys = level
        self.output_dir = utils.ensure_output_dir()
        self.add_env_tag = add_env_tag
        self.max_lines = max_lines

        if level != 'all':
            self.searchKeys = level.strip().split(',')
            self.searchKeys = ['['+key+']' for key in self.searchKeys]
    
    def filter_lines(self):
        filteredLines = list()

        with open(self.logfile) as file:
            if self.searchKeys == 'all':
                return file.readlines()
            
            for line in file.readlines():
                for key in self.searchKeys:
                    if key in line:
                        filteredLines.append(line)

        triage_file = os.path.join(self.output_dir, "triage.log")
        
        with open(triage_file, 'w') as file:
            file.writelines(filteredLines)

        if not filteredLines:
            print("Specified level not found.")

        return filteredLines
    
    def extract_details(self, line):
        userPattern = r"user=([\w\.\-]+)"
        filePattern = r"file=([\w\.\- ]+)"
        errorPattern = r"error=(.+)"
        timeStampPattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})" #based on timestamp format 
        #assumed format = YYYY-MM-DD hours:minutes:seconds
        levelPattern = r"\[(\w+)\] (.+)"

        username = re.search(userPattern, line) 
        
        #filename = re.search(filePattern, line)
        #error = re.search(errorPattern, line)
        time = re.search(timeStampPattern, line)
        level = re.search(levelPattern, line)

        detailsDict = dict()
        detailsDict['User'] = username.group(1) if not username is None else ''
        #detailsDict['filename'] = filename.group(1) if not filename is None else ''
        #detailsDict['error'] = error.group(1) if not error is None else ''
        detailsDict['Timestamp'] = time.group(1) if not time is None else ''
        detailsDict['Level'] = level.group(1) if not level is None else ''
        detailsDict['Message'] = level.group(2) if not level is None else ''

        return detailsDict
    
    def write_summary(self, format='csv'):
        
        filteredLines = self.filter_lines()
        summaryFile = os.path.join(self.output_dir, "summary."+format)

        if format == 'csv':
            summaryFields = ['Timestamp', 'Level', 'User', 'Message']

            if self.add_env_tag:
                summaryFields.append('ENV_TAG')

            with open(summaryFile, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=summaryFields)
                writer.writeheader()

                for line_number, line in enumerate(filteredLines):
                    if line_number >= self.max_lines:
                        break
                    summaryDict = self.extract_details(line)

                    if self.add_env_tag:
                        summaryDict['ENV_TAG'] = utils.get_env_tag()

                    writer.writerow(summaryDict)

        elif format == 'log':
            with open(summaryFile, 'w', newline='') as file:
                
                for line_number ,line in enumerate(filteredLines):
                    if line_number >= self.max_lines:
                        break

                    summaryDict = self.extract_details(line)
                    if self.add_env_tag:
                        file.write(f"[SUMMARY] {summaryDict['Timestamp']} | {summaryDict['Level']} | {summaryDict['Message']} | user={summaryDict['User']} | ENV={utils.get_env_tag()}\n")
                    else:
                        file.write(f"[SUMMARY] {summaryDict['Timestamp']} | {summaryDict['Level']} | {summaryDict['Message']} | user={summaryDict['User']}\n")
                    
    def count_Levels(self): 
        levelpattern = r"\[(\w+)\]"
        levelDict = dict()

        with open(self.logfile) as file:
            for line in file.readlines():
                result = re.search(levelpattern, line)
                if not result is None:
                    levelDict[result.group(1)] = levelDict.get(result.group(1), 0) + 1
                    
        level_summary_file = os.path.join(self.output_dir, "level_summary.log")

        with open(level_summary_file, 'w', newline='') as file:
            file.write("Log Level Counts:\n")
            for key in levelDict.keys():
                file.write(f"{key}: {levelDict[key]}\n")
