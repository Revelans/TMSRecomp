"""Walk the player to map position x z (layout coordinates) with NX_CONTROL, using the "pos" command as feedback.
Run from private/tms while the game runs with NX_CONTROL=control.txt NX_LOG=live.log.  Other files: GOTO_CTL / GOTO_LOG env (rig instances).
python ../../tools/drive/goto.py X Z [--tol 6] [--step 400]
The stick is camera-relative and cameras cut between zones, so the stick->world rotation is re-learned from every
step's actual movement. Exits 0 when within tol, 1 when stuck (no movement for 3 steps)."""
import argparse, math, os, re, time
CTL, LOG = os.environ.get("GOTO_CTL", "control.txt"), os.environ.get("GOTO_LOG", "live.log")

ap = argparse.ArgumentParser()
ap.add_argument("x", type=float)
ap.add_argument("z", type=float)
ap.add_argument("--tol", type=float, default=6)
ap.add_argument("--step", type=int, default=400, help="game ms per stick hold")
ap.add_argument("--speed", type=float, default=2, help="NX_SPEED of the run (wall time = game time / speed)")
a = ap.parse_args()


def send(line):
    with open(CTL, "a") as f:
        f.write(line + "\n")


def pos():
    n = len(open(LOG, "rb").read())
    send("pos")
    for _ in range(40):
        time.sleep(0.1)
        tail = open(LOG, "rb").read()[n:].decode("latin1")
        m = re.findall(r"\[pos\] player (\S+) (\S+) (\S+)", tail)
        if m:
            return tuple(map(float, m[-1]))
        if "[pos] " in tail:
            return None
    return None


theta = 0.0  # world angle = stick angle + theta (stick (0,+1) = up on screen)
stuck = 0
for it in range(200):
    p = pos()
    if not p:
        print("no position"); time.sleep(1); continue
    dx, dz = a.x - p[0], a.z - p[2]
    dist = math.hypot(dx, dz)
    if dist < a.tol:
        print(f"arrived at {p[0]:.1f} {p[1]:.1f} {p[2]:.1f}"); raise SystemExit(0)
    want = math.atan2(-dz, dx)           # world angle of the target (north = -z = up, like the stick)
    s = want - theta                     # stick angle
    hold = a.step if dist > 25 else max(120, int(a.step * dist / 25))
    sx, sy = int(32767 * math.cos(s)), int(32767 * math.sin(s))
    send(f"ls {sx} {sy} {hold}")
    time.sleep(hold / 1000 / a.speed + 0.25)
    q = pos()
    if not q:
        continue
    mx, mz = q[0] - p[0], q[2] - p[2]
    moved = math.hypot(mx, mz)
    if moved > 1.5:
        theta = math.atan2(-mz, mx) - s
        stuck = 0
    else:
        stuck += 1
        if stuck >= 3:
            print(f"stuck at {q[0]:.1f} {q[1]:.1f} {q[2]:.1f}"); raise SystemExit(1)
    print(f"{q[0]:.1f} {q[1]:.1f} {q[2]:.1f}  dist {dist:.0f}  moved {moved:.1f}")
print("gave up"); raise SystemExit(1)
