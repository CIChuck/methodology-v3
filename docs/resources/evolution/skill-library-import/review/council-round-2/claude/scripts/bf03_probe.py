"""BF-03 counterexamples against compare_refs from a given verifier file, in a disposable repo."""
import importlib.util, os, subprocess, sys, tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location("v", sys.argv[1]); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
root = Path(tempfile.mkdtemp(prefix="bf03-"))
env = {**os.environ, "GIT_AUTHOR_NAME": "T3 Code", "GIT_AUTHOR_EMAIL": "t3code@users.noreply.github.com",
       "GIT_COMMITTER_NAME": "T3 Code", "GIT_COMMITTER_EMAIL": "t3code@users.noreply.github.com"}
def g(*a, data=None, e=None): return subprocess.run(["git", *a], cwd=root, env=e or env, input=data, text=True, capture_output=True, check=True).stdout.strip()
g("init", "-q"); (root/"f").write_text("frozen\n"); g("add", "f"); T1 = g("write-tree")
(root/"f").write_text("other\n"); g("add", "f"); T2 = g("write-tree")
P = "refs/t3/orchestration-v2/checkpoints/"
def ck(name, tree, subj=None, e=None): return g("commit-tree", tree, data=(subj or f"t3 checkpoint ref={name}") + "\n", e=e)
frozen = {P+"ctxA/ordinal/0": ck(P+"ctxA/ordinal/0", T2), P+"ctxA/ordinal/1": ck(P+"ctxA/ordinal/1", T1), "refs/heads/main": ck("x", T1, "main")}
def fmt(d): return "\n".join(f"{k} {o}" for k, o in d.items())
cases = []
def case(label, added, expect_pass, *, frozen_override=None, allow=True, drop=None):
    before = dict(frozen_override if frozen_override is not None else frozen); after = dict(before)
    if drop: after.pop(drop); 
    after.update(added)
    errs, ok = v.compare_refs(root, fmt(before), fmt(after), allow_identical_t3_checkpoints=allow)
    passed = not errs
    res = "OK " if passed == expect_pass else "MISMATCH"
    print(f"{res} expect={'pass' if expect_pass else 'fail'} got={'pass' if passed else 'fail'} :: {label} :: {errs or [a['frozen_anchor'] for a in ok]}")
    cases.append(passed == expect_pass)
n = P+"ctxA/ordinal/2"; case("existing context, next ordinal, frozen tree", {n: ck(n, T1)}, True)
n = P+"ctxB/ordinal/0"; case("new context ordinal 0, frozen tree", {n: ck(n, T1)}, True)
n = P+"ctxB/ordinal/5"; case("new context any ordinal, frozen tree", {n: ck(n, T1)}, True)
n = P+"ctxB/ordinal/0"; case("new context, different tree", {n: ck(n, T2)}, False)
n = P+"ctxB/ordinal/0"; case("new context, tree of older non-latest frozen anchor only", {n: ck(n, T2)}, False)
n = P+"ctxB/ordinal/0"; case("new context, no frozen T3 checkpoint at all", {n: ck(n, T1)}, False, frozen_override={"refs/heads/main": frozen["refs/heads/main"]})
n0 = P+"ctxB/ordinal/0"; n1 = P+"ctxC/ordinal/0"
case("new contexts only chain to each other, no frozen T3", {n0: ck(n0, T1), n1: ck(n1, T1)}, False, frozen_override={"refs/heads/main": frozen["refs/heads/main"]})
n = P+"ctxB/ordinal/0"; case("new context, wrong subject", {n: ck(n, T1, "wrong")}, False)
n = P+"ctxB/ordinal/0"; case("new context, subject names other ref", {n: ck(P+"ctxB/ordinal/9", T1)}, False)
n = P+"ctxB/ordinal/0"; case("new context, wrong author", {n: ck(n, T1, e={**env, "GIT_AUTHOR_NAME": "Mallory"})}, False)
n = P+"ctxB/ordinal/0"; case("new context, wrong author email", {n: ck(n, T1, e={**env, "GIT_AUTHOR_EMAIL": "m@x"})}, False)
n = P+"ctxB/ordinal/0"; case("new context ref -> tree object (noncommit)", {n: T1}, False)
blob = g("hash-object", "-w", "f"); n = P+"ctxB/ordinal/0"; case("new context ref -> blob", {n: blob}, False)
tag = g("mktag", data=f"object {ck(P+'ctxB/ordinal/0', T1)}\ntype commit\ntag t\ntagger T3 Code <t3code@users.noreply.github.com> 0 +0000\n\nm\n")
n = P+"ctxB/ordinal/0"; case("new context ref -> annotated tag of valid commit", {n: tag}, False)
n = P+"ctxA/ordinal/1"; case("existing context same ordinal (rewritten frozen)", {n: ck(n, T1, "t3 checkpoint ref="+n+" again")}, False)
n = P+"ctxA/ordinal/01"; case("existing context nonincreasing ordinal 01", {n: ck(n, T1)}, False)
n = P+"ctxA/ordinal/0"; case("frozen ref deleted", {}, False, drop=P+"ctxA/ordinal/0")
case("frozen ref rewritten", {P+"ctxA/ordinal/0": ck(P+"ctxA/ordinal/0", T1)}, False)
case("non-T3 ref added", {"refs/heads/new": ck("refs/heads/new", T1)}, False)
n = "refs/t3/other/checkpoints/ctxB/ordinal/0"; case("other refs/t3 namespace", {n: ck(n, T1)}, False)
n = P+"ctxB/ordinal/0"; case("approval absent (allow=False)", {n: ck(n, T1)}, False, allow=False)
n = P+"ctx.B/ordinal/0"; case("context name outside regex", {n: ck(n, T1)}, False)
print("ALL_EXPECTED" if all(cases) else "SOME_MISMATCH", sum(cases), "/", len(cases))
