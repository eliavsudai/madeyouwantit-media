"""Quiet, warm music bed + voice mix for lesson Reels. python3 audio.py <build_dir>"""
import json, sys, numpy as np, soundfile as sf
ROOT = sys.argv[1]
SR = 48000
TL = json.load(open(f"{ROOT}/timeline.json"))
TOTAL, TE = TL["total"], TL["end"]
N = int(TOTAL * SR); t = np.arange(N) / SR
rng = np.random.default_rng(int(sum(TL["starts"]) * 100) % 1000)


def add(buf, x, at, gain=1.0):
    s = int(at * SR); e = min(N, s + len(x))
    if 0 <= s < N:
        buf[s:e] += x[:e - s] * gain


mid = lambda m: 440 * 2 ** ((m - 69) / 12)
bpm = 86; beat = 60 / bpm; bar = beat * 4
# warm, unobtrusive progression (Fmaj7 - Am7 - Dm7 - Bbmaj7), keys rotate per reel
shift = int(rng.integers(-2, 3))
prog = [[53, 57, 60, 64], [57, 60, 64, 67], [50, 53, 57, 60], [46, 50, 53, 57]]
bed = np.zeros(N)
for b in range(int(TE / bar) + 2):
    ch = prog[b % 4]
    for m in ch:
        f = mid(m + shift)
        n = int((bar + 0.6) * SR); k = np.arange(n) / SR
        # soft electric-piano tone: sine + slight 2nd harmonic, gentle tremolo, slow attack
        w = (np.sin(2 * np.pi * f * k) + 0.18 * np.sin(2 * np.pi * 2 * f * k) * np.exp(-k / 0.6))
        w *= (1 + 0.12 * np.sin(2 * np.pi * 4.5 * k)) * np.clip(k / 0.04, 0, 1) * np.exp(-k / 2.2)
        add(bed, w, b * bar, 0.05)
    # bass root
    f = mid(prog[b % 4][0] + shift - 12)
    n = int(bar * SR); k = np.arange(n) / SR
    add(bed, np.sin(2 * np.pi * f * k) * np.clip(k / 0.02, 0, 1) * np.exp(-k / 1.4), b * bar, 0.09)
    for q in range(4):  # soft kick on 1 and 3, shaker on off-beats
        at = b * bar + q * beat
        if q in (0, 2):
            n = int(0.22 * SR); k = np.arange(n) / SR
            add(bed, np.sin(2 * np.pi * (48 + 40 * np.exp(-k / 0.02)) * k) * np.exp(-k / 0.09), at, 0.22)
        n = int(0.06 * SR); k = np.arange(n) / SR
        sh = rng.normal(0, 1, n); sh = sh - np.convolve(sh, np.ones(6) / 6, "same")
        add(bed, sh * np.exp(-k / 0.018), at + beat / 2, 0.035)
bed *= np.clip(t / 0.4, 0, 1) * np.clip((TE + 0.2 - t) / 0.4, 0, 1)

# end-card sting
def bell(f, dur=1.8):
    n = int(dur * SR); k = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * k) + 0.35 * np.sin(2 * np.pi * f * 2.76 * k) * np.exp(-k / 0.2)) * np.exp(-k / 0.7)
add(bed, bell(mid(76 + shift)), TE, 0.16); add(bed, bell(mid(81 + shift)), TE + 0.35, 0.16)
endpad = sum(np.sin(2 * np.pi * mid(m + shift) * t) for m in (53, 60, 64)) * np.clip((t - TE) / 0.3, 0, 1) * np.clip((TOTAL - t) / 0.8, 0, 1)
bed += endpad * 0.04

voice = np.zeros(N)
for st, fp in zip(TL["starts"], TL["files"]):
    w, sr = sf.read(fp)
    if w.ndim > 1: w = w.mean(1)
    x = np.interp(np.arange(int(len(w) * SR / sr)) / SR, np.arange(len(w)) / sr, w)
    add(voice, x, st)
voice /= np.abs(voice).max()
voice = np.tanh(voice * 2.0) / np.tanh(2.0) * 0.9
venv = np.convolve(np.abs(voice), np.ones(4800) / 4800, "same"); venv = np.clip(venv / (venv.max() * 0.25), 0, 1)
mix = voice + bed * (1 - 0.55 * venv) * 0.75
mix = np.tanh(mix * 1.05) / np.tanh(1.05)
def rms(a, b, x): return float(np.sqrt(np.mean(x[int(a * SR):int(b * SR)] ** 2)))
print("voice rms", round(rms(0.3, TE, voice), 3), "bed under voice", round(rms(0.3, TE, bed * (1 - 0.55 * venv) * 0.9), 3))
mix = mix / np.abs(mix).max() * 0.92 * np.clip((TOTAL - t) / 0.4, 0, 1)
sf.write(f"{ROOT}/mix.wav", np.stack([mix, mix], 1).astype(np.float32), SR)
