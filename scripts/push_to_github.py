#!/usr/bin/env python3
"""Push to GitHub via REST API (handles file deletions)"""
import subprocess, json, os, sys
from pathlib import Path

REPO = "fclwtt/agent-component-library"
BRANCH = "master"
CHUNK = 50

def gh(method, endpoint, data=None):
    cmd = ['gh', 'api', '--method', method, endpoint, '--input', '-']
    r = subprocess.run(cmd, input=json.dumps(data) if data else None,
                       capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        err = (r.stdout or r.stderr)[:200]
        print(f"  API err: {err}", flush=True); return None
    try: return json.loads(r.stdout) if r.stdout.strip() else None
    except: return None

def main():
    # 1. Get remote state
    ref = gh('GET', f'repos/{REPO}/git/ref/heads/{BRANCH}')
    if not ref: ref = gh('GET', f'repos/{REPO}/git/refs/heads/main')
    if not ref: print("No remote ref"); sys.exit(1)
    
    parent = ref['object']['sha']
    parent_info = gh('GET', f'repos/{REPO}/git/commits/{parent}')
    base_tree = parent_info['tree']['sha']
    print(f"Remote: {parent[:12]}, tree: {base_tree[:12]}", flush=True)

    # 2. Get root tree entries (to know what needs deletion)
    root_tree = gh('GET', f'repos/{REPO}/git/trees/{base_tree}?recursive=1')
    if not root_tree: print("Cannot fetch root tree"); sys.exit(1)
    
    existing_paths = {e['path'] for e in root_tree['tree'] if e['type'] == 'blob'}
    
    # 3. Collect local files
    root = Path.cwd()
    local_paths = set()
    tree_entries = []
    
    for p in sorted(root.rglob('*'), key=lambda x: str(x)):
        if p.is_dir(): continue
        if any(x in p.parts for x in ('.git', '__pycache__', '.pytest_cache', 'node_modules')): continue
        if p.name == '.DS_Store': continue
        rel = str(p.relative_to(root))
        sz = p.stat().st_size
        if sz > 100000 or sz == 0: continue
        try: c = p.read_text(encoding='utf-8', errors='replace')
        except: continue
        if not c.strip(): continue
        mode = '100755' if os.access(p, os.X_OK) else '100644'
        tree_entries.append({'path': rel, 'mode': mode, 'content': c})
        local_paths.add(rel)
    
    # 4. Find files that need deletion (exist remotely but not locally)
    to_delete = existing_paths - local_paths
    for d in sorted(to_delete):
        tree_entries.append({'path': d, 'mode': '100644', 'sha': None})
    
    total_add = len(tree_entries) - len(to_delete)
    print(f"Local: {total_add} files, Delete: {len(to_delete)} files, Total: {len(tree_entries)}", flush=True)

    # 5. Create tree
    current = base_tree
    for i in range(0, len(tree_entries), CHUNK):
        r = gh('POST', f'repos/{REPO}/git/trees',
               {'tree': tree_entries[i:i+CHUNK], 'base_tree': current})
        if not r: print(f"Tree {i//CHUNK+1} FAILED"); sys.exit(1)
        current = r['sha']
        print(f"  Tree {i//CHUNK+1}: {current[:12]}", flush=True)

    # 6. Commit
    msg = sys.argv[1] if len(sys.argv) > 1 else "update"
    r = gh('POST', f'repos/{REPO}/git/commits', {
        'message': msg, 'tree': current, 'parents': [parent],
    })
    if not r: print("Commit FAILED"); sys.exit(1)
    print(f"Commit: {r['sha'][:12]}", flush=True)

    # 7. Push
    r = gh('PATCH', f'repos/{REPO}/git/refs/heads/{BRANCH}', {'sha': r['sha'], 'force': True})
    if r: print(f"\nPUSHED! {r['ref']} -> {r['object']['sha'][:12]}")
    else: print("Push FAILED"); sys.exit(1)

if __name__ == '__main__':
    main()
