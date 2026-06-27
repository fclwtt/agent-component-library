#!/usr/bin/env python3
"""Push via GitHub REST API (avoid git push network issues)"""
import subprocess, json, os, sys; from pathlib import Path
REPO="fclwtt/agent-component-library"; BRANCH="master"

def gh(method,endpoint,data=None):
    cmd=['gh','api','--method',method,endpoint,'--input','-']
    r=subprocess.run(cmd,input=json.dumps(data)if data else None,capture_output=True,text=True,timeout=30)
    if r.returncode!=0:print(f"API err:{(r.stdout or r.stderr)[:200]}",flush=True);return None
    return json.loads(r.stdout)if r.stdout.strip()else None

ref=gh('GET',f'repos/{REPO}/git/ref/heads/{BRANCH}')or gh('GET',f'repos/{REPO}/git/refs/heads/main')
if not ref:print("No remote ref");sys.exit(1)
parent=ref['object']['sha']
bt=gh('GET',f'repos/{REPO}/git/commits/{parent}')['tree']['sha']
print(f"Remote:{parent[:12]},tree:{bt[:12]}")

files=[];root=Path.cwd()
for p in root.rglob('*'):
 if p.is_dir():continue
 if any(x in p.parts for x in('.git','__pycache__','.pytest_cache','node_modules')):continue
 if p.name=='.DS_Store':continue
 rl=str(p.relative_to(root));sz=p.stat().st_size
 if sz>100000 or sz==0:continue
 try:c=p.read_text(encoding='utf-8',errors='replace')
 except:continue
 if not c.strip():continue
 files.append({'path':rl,'mode':'100755'if os.access(p,os.X_OK)else'100644','content':c})

print(f"Files:{len(files)},{sum(len(f['content'])for f in files)/1024:.0f}KB",flush=True)
cur=bt
for i in range(0,len(files),50):
 r=gh('POST',f'repos/{REPO}/git/trees',{'tree':files[i:i+50],'base_tree':cur})
 if not r:print(f"Tree {i//50+1} FAILED");sys.exit(1)
 cur=r['sha'];print(f"Tree {i//50+1}:{cur[:12]}",flush=True)

msg=sys.argv[1]if len(sys.argv)>1 else"update"
r=gh('POST',f'repos/{REPO}/git/commits',{'message':msg,'tree':cur,'parents':[parent]})
if not r:print("Commit FAILED");sys.exit(1)
print(f"Commit:{r['sha'][:12]}",flush=True)

r=gh('PATCH',f'repos/{REPO}/git/refs/heads/{BRANCH}',{'sha':r['sha'],'force':True})
if r:print(f"\nPUSHED!{r['ref']}->{r['object']['sha'][:12]}")
else:print("Push FAILED");sys.exit(1)
