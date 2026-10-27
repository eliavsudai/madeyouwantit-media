import json, numpy as np, soundfile as sf
SR = 48000
TL = json.load(open("/home/claude/r1/timeline2.json"))
TOTAL, TT, TP, TE, TF = TL["total"], TL["touch"], TL["pop"], TL["end"], TL["fake"]
N = int(TOTAL * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(1)


def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y


def env_rise(t0, t1):
    return np.clip((t - t0) / max(t1 - t0, 1e-3), 0, 1)


bed = np.zeros(N)
# ---- drone: low fifth, slowly rising in pitch and level ----
pre = t < TT
p = np.clip(t / TT, 0, 1)
f0 = 55 * (1 + 0.12 * p ** 2)
ph = 2 * np.pi * np.cumsum(f0) / SR
drone = 0.5 * np.sin(ph) + 0.3 * np.sin(1.5 * ph) + 0.12 * np.sin(2 * ph + 0.3 * np.sin(t * 0.7))
noise = rng.normal(0, 1, N)
wind = np.convolve(noise, np.ones(240) / 240, mode="same") * 3.0
drone_level = (0.10 + 0.32 * p ** 1.5) * env_rise(0, 1.2)
bed += (drone + 0.5 * wind) * drone_level * pre

# ---- clock ticks, slowly tightening ----
def click(freq=3200, dur=0.018, amp=0.35):
    n = int(dur * SR); k = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * freq * k) * np.exp(-k / 0.004) + amp * 0.4 * rng.normal(0, 1, n) * np.exp(-k / 0.002)

tt = 0.7; i = 0
while tt < TT - 0.1:
    if not (TF - 0.05 < tt < TF + 1.5):
        c = click(3400 if i % 2 == 0 else 2900, amp=0.22 + 0.12 * tt / TT)
        s = int(tt * SR); bed[s:s + len(c)] += c[:max(0, N - s)]
    tt += 0.5 - 0.17 * (tt / TT) ** 2; i += 1

# ---- heartbeat in the last stretch ----
def thump(amp):
    n = int(0.18 * SR); k = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * (48 + 30 * np.exp(-k / 0.03)) * k) * np.exp(-k / 0.05)

hb = 14.0
while hb < TT - 0.2:
    prog = (hb - 14) / (TT - 14)
    amp = 0.35 + 0.35 * prog
    for off, a in ((0, 1.0), (0.17, 0.7)):
        s = int((hb + off) * SR); th = thump(amp * a); bed[s:s + len(th)] += th[:max(0, N - s)]
    hb += 60 / (66 + 50 * prog)

# ---- whoosh of the pin entering ----
wn = rng.normal(0, 1, int(0.9 * SR))
k = np.arange(len(wn)) / SR
wsh = np.convolve(wn, np.ones(30) / 30, mode="same") * np.exp(-((k - 0.25) / 0.18) ** 2) * 0.35
bed[:len(wsh)] += wsh

# ---- fake-out: riser into the lunge, two hard heartbeats at the closest point, then release ----
dip = 1 - 0.85 * np.clip((t - (TF + 0.55)) / 0.05, 0, 1) * np.clip((TF + 1.6 - t) / 0.5, 0, 1)
bed *= dip
s0 = int((TF - 0.1) * SR); n = int(0.75 * SR); k = np.arange(n) / SR
ris = rng.normal(0, 1, n); ris = ris - np.convolve(ris, np.ones(12) / 12, mode="same")
ris *= (k / k[-1]) ** 2.2 * 0.5
ris += np.sin(2 * np.pi * np.cumsum(300 + 900 * (k / k[-1]) ** 2) / SR) * (k / k[-1]) ** 2 * 0.12
bed[s0:s0 + n] += ris
for off in (0.6, 0.78):
    th = thump(1.25); s = int((TF + off) * SR); bed[s:s + len(th)] += th
# hard cut at the touch (tension silence)
cut = np.ones(N); cut[int(TT * SR):] = 0
cut = np.convolve(cut, np.ones(1200) / 1200, mode="same")
bed *= cut

# ---- rubber squeak during the dent ----
s0, s1 = int(TT * SR), int(TP * SR)
k = np.arange(s1 - s0) / SR
fq = 520 + 380 * (k / k[-1]) + 60 * np.sin(2 * np.pi * 23 * k)
sq = np.sin(2 * np.pi * np.cumsum(fq) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 37 * k)) ** 2
sq += 0.3 * np.sin(2 * np.pi * np.cumsum(fq * 2.01) / SR)
sq *= np.clip(k / 0.08, 0, 1) * 0.4 * (0.6 + 0.4 * k / k[-1])
bed[s0:s1] += sq

# ---- POP ----
s = int(TP * SR)
n = int(1.6 * SR); k = np.arange(n) / SR
bang = rng.normal(0, 1, n) * np.exp(-k / 0.035) * 1.0
bang += np.sin(2 * np.pi * (70 + 120 * np.exp(-k / 0.02)) * k) * np.exp(-k / 0.12) * 0.9
tail = np.convolve(rng.normal(0, 1, n) * np.exp(-k / 0.5), np.ones(60) / 60, mode="same") * 0.18 * np.clip(k / 0.02, 0, 1)
pop = np.tanh((bang + tail) * 1.4) * 0.95
popsig = np.zeros(N); popsig[s:s + n] += pop[:max(0, N - s)]

# ---- soft resolve pad after the pop ----
ps = TP + 0.35
pad = np.zeros(N)
for f in (261.63, 392.0, 493.88, 587.33, 659.25):
    pad += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * (1 + 0.004 * np.sin(t * 5))
padenv = np.clip((t - ps) / 0.8, 0, 1) * np.clip((TE + 0.3 - t) / 0.5, 0, 1)
bed += pad * padenv * 0.035

# ---- end-card sting: two bell plucks ----
def bell(f, amp, dur=1.8):
    n = int(dur * SR); k = np.arange(n) / SR
    return amp * (np.sin(2 * np.pi * f * k) + 0.4 * np.sin(2 * np.pi * f * 2.76 * k) * np.exp(-k / 0.2)) * np.exp(-k / 0.6)

for off, f in ((0.0, 659.25), (0.45, 987.77)):
    b = bell(f, 0.22); s = int((TE + off) * SR); bed[s:s + len(b)] += b[:max(0, N - s)]
# low warm chord under the end card
endpad = sum(np.sin(2 * np.pi * f * t) for f in (130.81, 196.0, 329.63))
bed += endpad * np.clip((t - TE) / 0.3, 0, 1) * np.clip((TOTAL - t) / 0.8, 0, 1) * 0.06

# ---- voice ----
voice = np.zeros(N)
for i, st in enumerate(TL["starts"]):
    w, sr = sf.read(TL["files"][i])
    if w.ndim > 1: w = w.mean(1)
    x = np.interp(np.arange(int(len(w) * SR / sr)) / SR, np.arange(len(w)) / sr, w)
    s = int(st * SR); voice[s:s + len(x)] += x[:max(0, N - s)]
voice = voice / np.abs(voice).max()
voice = np.tanh(voice * 2.4) / np.tanh(2.4) * 0.9

# duck the bed under the voice
venv = np.convolve(np.abs(voice), np.ones(4800) / 4800, mode="same")
venv = np.clip(venv / (venv.max() * 0.25), 0, 1)
duck = 1 - 0.6 * venv
bed *= 1 + 2.2 * np.clip((4.0 - t) / 0.5, 0, 1)
bed = np.tanh(bed * 0.9)
mix = voice + bed * 0.5 * duck + popsig * 1.0
mix = np.tanh(mix * 1.05) / np.tanh(1.05)
def rms(a, b, x): return float(np.sqrt(np.mean(x[int(a*SR):int(b*SR)] ** 2)))
print("intro bed rms", round(rms(0.5, 4.8, mix), 3), "voice section rms", round(rms(5, 29, voice), 3), "bed under voice", round(rms(5, 29, bed * 0.5 * duck), 3), "peak", round(np.abs(mix).max(), 3))
mix = mix / np.abs(mix).max() * 0.92
fade = np.clip((TOTAL - t) / 0.4, 0, 1)
mix *= fade
sf.write("/home/claude/r1/mix2.wav", np.stack([mix, mix], 1).astype(np.float32), SR)
print("ok", round(TOTAL, 2), "peak bed/voice", round(np.abs(bed * 0.55).max(), 2))
