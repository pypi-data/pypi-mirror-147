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

        yield c.decode('utf-8')

def _login(pw, username):
    p = Popen([bw_path, 'login',username,pw], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    trigger_error = True
    out = p.communicate()
    for line in parse_comm(out):
        if "already logged in" in line:
            trigger_error = False

    p.terminate()

    if trigger_error:
        return False
    return True

def _unlock(pw_byte):
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

def _sync(pw_byte):
    p = Popen([bw_path, 'sync'], stdin=PIPE, stdout=PIPE)
    out = p.communicate(input=pw_byte)
    p.terminate()
    for line in parse_comm(out):
        if "Syncing complete" in line:
            return True

    return False

def _save_json(pw_byte, savepath):
    p = Popen([bw_path, 'export', '--output', os.path.join(savepath, "bitwarden.json"), "--format","json"], stdin=PIPE, stdout=PIPE)
    out = p.communicate(input=pw_byte)
    for line in parse_comm(out):
        if "Saved" in line:
            break

    if os.path.exists(os.path.join(savepath, "bitwarden.json")):
        return True
    else:
        return False

@click.group(invoke_without_command=True, chain=True)
@click.option('--pw', default='', help='Password')
@click.option('--session', default=None, help='Sessionkey')
@click.option('--savepath', default='./export/', help='savepath')
@click.option('--debug', default=0, help='Debug', type=int)
@click.option('--apppath', default=None, type=click.Path(exists=True), help='Path to bitwarden cli')
@click.pass_context
def cli(ctx : click.Context, pw, session, savepath, debug, apppath):
    global bw_path

    if apppath is not None:
        bw_path = apppath
    
    if not bw_path:
        print("cannot find bw cli")
        sys.exit(1)

    if debug <= 0:
        pass
    elif debug == 1:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    elif debug >= 2:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    if ctx.invoked_subcommand is None:
        print("no subcommand given")
        sys.exit(1)

    ctx.obj = {}
    ctx.ensure_object(dict)

    if pw:
        ctx.obj['pw'] = pw
        ctx.obj['pwb'] = str.encode(pw)

    if session:
        os.environ['BW_SESSION'] = session

    if "BW_SESSION" in os.environ:
        ctx.obj['session'] = os.environ['BW_SESSION']

    if savepath:
        ctx.obj['savepath'] = savepath

    def on_close():
        if "BW_SESSION" in os.environ:
            del os.environ['BW_SESSION']

    ctx.call_on_close(on_close)

@cli.command()
@click.argument('username', required=True, type=str)
@click.pass_context
def login(ctx, username):
    print("> login")

    if 'pw' not in ctx.obj:
        pw = click.prompt("Password", hide_input=True)
        ctx.obj['pw'] = pw
        ctx.obj['pwb'] = str.encode(pw)
    else:
        pw = ctx.obj['pw']
    if _login(pw, username):
        print("Login successful")
    else:
        print("Login failed")

@cli.command()
@click.pass_context
def sync(ctx):
    print("> sync")

    if "pw" not in ctx.obj:
        print("No password set")
        sys.exit(1)
    
    pw_byte = ctx.obj['pwb']
    pw = ctx.obj['pw']

    if _sync(pw_byte):
        print("Sync successful")
        
    else:
        print("Sync failed")

@cli.command()
@click.pass_context
def unlock(ctx):
    print("> unlock")

    if "BW_SESSION" in os.environ:
        print("There is already a session set in environ, will be overwritten")

    pw_byte = ctx.obj['pwb']

    if not(sessionkey:= _unlock(pw_byte)):
        print("unlock failed")
        sys.exit(1)

    os.environ['BW_SESSION'] = sessionkey
    ctx.obj['session'] = sessionkey
    

@cli.command()
@click.pass_context
def saveJson(ctx):
    ctx_dict : dict = ctx.obj
    savepath =ctx_dict.get('savepath', None)
    pw_byte = ctx_dict.get('pwb', None)

    if not savepath:
        print("No savepath set")
        sys.exit(1)
    if not pw_byte:
        print("No password set")
        sys.exit(1)

    if not _save_json(pw_byte, savepath):
        print("Save failed")
        sys.exit(1)

@cli.command()
@click.option('--dump', is_flag=True, default=False, help='Dump all data')
@click.pass_context
def export(ctx, dump):
    ctx.invoke(unlock)

    ctx_dict : dict = ctx.obj
    savepath =ctx_dict.get('savepath', None)
    session =ctx_dict.get('session', None)
    pw_byte = ctx_dict.get('pwb', None)
    if not savepath:
        print("No savepath set")
        sys.exit(1)
    if not session:
        print("No session set")
        sys.exit(1)

    p = Popen([bw_path, "list" , "items" , "--session", session], stdin=PIPE, stdout=PIPE)    
    out = p.communicate(input=pw_byte)[0]
    out.decode('utf-8')
    p.terminate()
    json_data = json.loads(out)
    # save to file
    if dump:
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

@cli.command()
@click.pass_context
def autoe(ctx : click.Context):
    ctx.invoke(unlock)
    ctx.invoke(sync)
    ctx.invoke(saveJson)
    ctx.invoke(export)
    print("Autoe successful")

if __name__ == '__main__':
    cli(obj={})
    