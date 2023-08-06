from subprocess import Popen, PIPE
import sys
import click
import os
import logging
import json


def get_bw_path():
    if "BW_PATH" in os.environ:
        return os.environ["BW_PATH"]

    if os.name == 'nt' and os.path.exists("./bw.exe"):
        return "bw.exe"
    
    return None

def remove_illegal_chars(s):
    invalid = '<>:"/\|?*'

    for c in invalid:
        s = s.replace(c, '')
    
    return s

bw_path = get_bw_path()

def parse_comm(comm):
    if not isinstance(comm, tuple):
        return 
    for c in comm:
        if c is None:
            continue
        # on stderr
        logging.debug(c.decode('utf-8'))
        yield c.decode('utf-8')

def login(pw, username):
    if not pw:
        print("password is empty", file=sys.stderr)
        return False
    if not username:
        print("username is empty", file=sys.stderr)
        return False

    p = Popen([bw_path, 'login',username,pw], stdin=PIPE, stdout=PIPE)
    trigger_error = True
    out = p.communicate()
    for line in parse_comm(out):
        if "already logged in" in line:
            trigger_error = False

    p.terminate()

    if trigger_error:
        return False
    return True

def unlock(pw_byte):
    p = Popen([bw_path, 'unlock'], stdin=PIPE, stdout=PIPE, shell=True)
    out = p.communicate(input=pw_byte)
    sessionkey = None
    for line in parse_comm(out):
        if "export BW_SESSION=" in line:
            # get sessionkey
            sessionkey = line.split('=')[1]
            break
            
    p.terminate()

    if sessionkey:
        return sessionkey[1:-1]

def sync(pw_byte):
    p = Popen([bw_path, 'sync'], stdin=PIPE, stdout=PIPE)
    out = p.communicate(input=pw_byte)
    p.terminate()
    for line in parse_comm(out):
        if "Syncing complete" in line:
            return True

    return False

def save_json(pw_byte, savepath):
    p = Popen([bw_path, 'export', '--output', os.path.join(savepath, "bitwarden.json"), "--format","json"], stdin=PIPE, stdout=PIPE)
    out = p.communicate(input=pw_byte)
    for line in parse_comm(out):
        if "Saved" in line:
            break

    if os.path.exists(os.path.join(savepath, "bitwarden.json")):
        return True
    else:
        return False

def export(pw_byte, savepath, session, dump_flag):
    p = Popen([bw_path, "list" , "items" , "--session", session], stdin=PIPE, stdout=PIPE)
    out = p.communicate(input=pw_byte)[0]
    out.decode('utf-8')
    p.terminate()
    json_data = json.loads(out)
    # save to file
    if dump_flag:
        with open(os.path.join(savepath, "bitwarden_list.json"), "w") as f:
            json.dump(json_data, f, indent=4)

    # parse
    for item in json_data:
        itemid = item['id']
        # name strip for windows compatibility
        i : str ="asfsafasf"

        if "attachments" in item:
            for attachment in item["attachments"]:
                p = Popen(
                    [
                        bw_path, 
                        "get" , 
                        "attachment" , 
                        attachment["fileName"], 
                        "--itemid", itemid, 
                        "--session", session,
                        "--output", os.path.join(savepath, remove_illegal_chars(item["name"]), attachment["fileName"])
                    ],
                    stdin=PIPE, stdout=PIPE)
                out = p.communicate(input=pw_byte)
                for i, line in enumerate(parse_comm(out)):
                    if i == 0:
                        print(line)
                    else:
                        logging.debug(line)
                    
                p.terminate()
        # open folder in explorer
        os.startfile(os.path.join(savepath))