import subprocess
import sys
from .keys import *
from .scope import Scope
from subprocess import Popen, PIPE, STDOUT
import jmespath
import json

def is_dict(d): return isinstance(d, dict)

def shell(args):
    result = subprocess.run(args, stdout=subprocess.PIPE)
    msg = result.stdout.decode("utf-8").strip()
    return msg

def pipe(args, prior):
    p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    result = p.communicate(input=prior.encode())[0]
    return result.decode()

def match(body, prior):
    jdata = json.loads(prior)
    print(f'match.body: {body}')
    print(f'match.prior: {jdata}')
    matches = jmespath.search(body, jdata)
    print('match: ',end='')
    print(matches)
    return matches

class YMM:
    def __init__(self, yaml):
        self.env = Scope()
        self.env.push("ymm", yaml)
        self.actions = self.env.actions()
        self.printOutput = True

    def run(self,action=DEFAULT_ACTION, hide=False):
        currentOutput = self.printOutput
        if hide: self.printOutput = False
        if not action in self.actions:
            msg = f'ERROR: action [{action}] not found' if action != DEFAULT_ACTION else "Exiting"
            sys.exit(msg)
        self.env.push(action)
        cmds = self.env.get(action)
        self.log(cmds, action)

        cdict = cmds if is_dict(cmds) else {f'{action}#{i}': cmd for i,cmd in enumerate(cmds)}
        results = [self.execute(v, k) for k,v in cdict.items()]
        self.printOutput = currentOutput
        return results

    def execute(self, cmd, key):
        self.log(f'! {key}: {cmd}', "execute")
        if not isinstance(cmd,str): return self.save(cmd, key)
        variables = self.env.flatstr()
        text = cmd.format(**variables)
        self.log(text, "formatted")
        args = text.split(" ")
        sigil = args.pop(0)
        body = " ".join(args)
        self.log(sigil, "sigil")
        self.log(body, "body")
        if sigil == kCall: return "\n".join(self.run(body)) # run named action
        if sigil == kShell: text = shell(args)
        if sigil == kEval: text = eval(body)
        if sigil == kPipe: text = pipe(args, self.env.get(kLast))
        if sigil == kMatch: text = match(body, self.env.get(kLast))
        self.log(text, "text")
        #if text and not isinstance(text,dict):
        return self.save(text, key)

    def save(self, msg, key):
        if self.printOutput: print(f'# {key}: {msg}')
        #if kLast in self.env: self.env[kPrior] = self.env[kLast]
        self.env.set(kLast, msg)
        self.env.set(key, msg)
        return msg

    def log(self, event, caption=False):
        if self.env.get(kLog, False):
            prefix = f'DEBUG:{caption}' if caption else 'DEBUG'
            print(prefix, end=' ')
            print(event)
