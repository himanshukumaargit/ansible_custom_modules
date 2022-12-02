import pprint
import difflib
import re
import argparse
import os

def main(changed_cfg,original_cfg,stdout_,changes_to_file):
    result=[]
    original_file = open(original_cfg).readlines()
    changed_file = open(changed_cfg).readlines()
    changes = []
    for line in difflib.ndiff(original_file,changed_file):
        if re.match(re.compile("[-+]"),line):
            if "!" not in line:
                line_ = re.sub("[-+]","",line)
                changes.append({(line_.replace(" ","")).strip("\n"):line.strip("\n")})
    changes_key_list = []

    for i in  changes:
        changes_key_list.append(list(i.keys())[0])    
    for i in changes_key_list:
        if changes_key_list.count(i)>1:
            while (i in changes_key_list):
                changes_key_list.remove(i)
    for changed_key in changes_key_list:
        if changed_key:
            for _item in changes:
                for key,value in _item.items():
                    if key==changed_key:
                        result.append(value)
    if stdout_=='True':                    
        pprint.pprint({"changes":result})
    if changes_to_file != 'False':
        with open(changes_to_file,"w") as file_handler: 
            for line in result:
                file_handler.write(line+"\n")  
    return {"changes":result}

if __name__ == '__main__':
    parser=argparse.ArgumentParser(prog='cisco ios config deltas generator',
                                   description='compare 2 cisco config files and return the deltas or difference between them',
                                   )
    parser.add_argument('--original_cfg',help="Original Config File or Base Config File to compare")
    parser.add_argument('--changed_cfg',help="changed Config File to compare with original config")
    parser.add_argument('--stdout_changes',help="show changes to screen",choices=('True','False'))
    parser.add_argument('--changes_to_file',help="file write delta to file",default='False')
    args=parser.parse_args()
    changed_cfg = args.changed_cfg
    original_cfg = args.original_cfg
    stdout_ = args.stdout_changes
    change_to_file = args.changes_to_file
    try:
        main(changed_cfg=changed_cfg,original_cfg=original_cfg,stdout_=stdout_,changes_to_file=change_to_file)
    except Exception as e:
        print(e)    
        print("run: \npython3 cisco_ios_config_diff.py --help")
    
        
