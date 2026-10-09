#!/usr/bin/env python3
"""Patch kernel 3.18 for Python3 + GCC>=10. Rewrites gcc-wrapper.py directly."""
import os, re

# ── Patch 1: Rewrite scripts/gcc-wrapper.py as clean Python 3 ────────────────
path = 'scripts/gcc-wrapper.py'
if os.path.exists(path):
    content = open(path).read()
    # Fix: print "str", var  ->  print("str", var)
    content = content.replace(
        'print "error, forbidden warning:", m.group(2)',
        'print("error, forbidden warning:", m.group(2))'
    )
    # Fix: print line,  ->  print(line, end="")
    content = content.replace(
        'print line,',
        'print(line, end="")'
    )
    # Fix: print args[0] + ':',e.strerror  ->  print(args[0]+':',e.strerror)
    content = content.replace(
        "print args[0] + ':',e.strerror",
        "print(args[0] + ':', e.strerror)"
    )
    # Fix: print 'Is your PATH...'  ->  print('Is your PATH...')
    content = content.replace(
        "print 'Is your PATH set correctly?'",
        "print('Is your PATH set correctly?')"
    )
    # Fix: print ' '.join(args), str(e)  ->  print(...)
    content = content.replace(
        "print ' '.join(args), str(e)",
        "print(' '.join(args), str(e))"
    )
    # Fix bytes from subprocess stderr
    content = content.replace(
        'for line in proc.stderr:',
        'for line in proc.stderr:\n            if isinstance(line, bytes): line = line.decode("utf-8", errors="replace")'
    )
    # Fix shebang
    content = content.replace('#! /usr/bin/env python2', '#! /usr/bin/env python3')
    open(path, 'w').write(content)
    print("[OK] gcc-wrapper.py patched")
else:
    print("[SKIP] gcc-wrapper.py not found")

# ── Patch 2: dtc yylloc (GCC>=10 strict no-common) ───────────────────────────
for p in ['scripts/dtc/dtc-lexer.lex.c_shipped', 'scripts/dtc/dtc-lexer.l']:
    if os.path.exists(p):
        src = open(p).read()
        new = re.sub(r'^YYLTYPE yylloc;', 'extern YYLTYPE yylloc;', src, flags=re.MULTILINE)
        if new != src:
            open(p, 'w').write(new)
            print(f"[OK] {p} yylloc patched")
        else:
            print(f"[SKIP] {p} already ok")
    else:
        print(f"[SKIP] {p} not found")

print("Done.")
