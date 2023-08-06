from email.policy import default
from subprocess import Popen, PIPE
import sys
import click
import os
import logging
import json
import core

@click.group(invoke_without_command=True, chain=True)
@click.option('--pw', default='', help='Password')
@click.option('--session', default=None, help='Sessionkey')
@click.option('--savepath', default='./export/', help='savepath')
@click.option('--debug', is_flag = True, help='Debug mode')
@click.option('--debugpath', default=None, help='Debug to file', type=click.Path(exists=True))
@click.option('--apppath', default=None, type=click.Path(exists=True), help='Path to bitwarden cli')
@click.pass_context
def cli(ctx : click.Context, pw, session, savepath, debug, apppath, debugpath):
    bw_path = core.bw_path

    if apppath is not None:
        bw_path = apppath
    
    if not bw_path:
        print("cannot find bw cli")
        sys.exit(1)

    if debug and debugpath is not None:
        logging.basicConfig(filename=debugpath, level=logging.DEBUG)
    elif debug:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

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
@click.argument('username', type=str, default=None)
@click.pass_context
def login(ctx, username):
    print("> login")
    
    if "username" in ctx.obj:
        new_username = ctx.obj['username']

    if not username:
        username = new_username

    if not username:
        username = input("username: ")

    if not username:
        print("no username given")
        sys.exit(1)

    if 'pw' not in ctx.obj:
        pw = click.prompt("Password", hide_input=True)
        ctx.obj['pw'] = pw
        ctx.obj['pwb'] = str.encode(pw)
    else:
        pw = ctx.obj['pw']
    if core.login(pw, username):
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

    if core.sync(pw_byte):
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

    if not(sessionkey:= core.unlock(pw_byte)):
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

    if not core.save_json(pw_byte, savepath):
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

    core.export(pw_byte, savepath, session, dump)

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
    