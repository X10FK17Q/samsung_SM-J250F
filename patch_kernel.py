#!/usr/bin/env python3
"""Patch kernel 3.18 scripts for Python3 + GCC>=10 compatibility."""
import re, os, sys

# --- Patch 1: gcc-wrapper.py ---
path = 'scripts/gcc-wrapper.py'
if os.path.exists(path):
    with open(path, 'r') as f:
        src = f.read()
    # print "str", var  ->  print("str", var)
    src = re.sub(r'print (".*?"),\s*(.+)', r'print(\1, \2)', src)
    # print "str" % var  ->  print("str" % var)
    src = re.sub(r'print (".*?" % \S+)', r'print(\1)', src)
    # print line,  ->  print(line, end="")
    src = src.replace('print line,', 'print(line, end="")')
    # print line  ->  print(line)
    src = re.sub(r'^(\s*)print line\s*$', r'\1print(line)', src, flags=re.MULTILINE)
    with open(path, 'w') as f:
        f.write(src)
    print(f"[OK] {path} patched")
else:
    print(f"[SKIP] {path} not found")

# --- Patch 2: dtc-lexer yylloc multiple definition ---
for path in ['scripts/dtc/dtc-lexer.lex.c_shipped', 'scripts/dtc/dtc-lexer.l']:
    if os.path.exists(path):
        with open(path, 'r') as f:
            src = f.read()
        patched = re.sub(r'^YYLTYPE yylloc;', 'extern YYLTYPE yylloc;', src, flags=re.MULTILINE)
        if patched != src:
            with open(path, 'w') as f:
                f.write(patched)
            print(f"[OK] {path} yylloc patched")
        else:
            print(f"[SKIP] {path} yylloc already ok or not found")
    else:
        print(f"[SKIP] {path} not found")

print("All patches done.")
