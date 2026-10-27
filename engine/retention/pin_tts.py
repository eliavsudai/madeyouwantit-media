import soundfile as sf, numpy as np, json, sys
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
V, SP = sys.argv[1], float(sys.argv[2])
L = [
 "You've been staring at a pin for four seconds.",
 "You don't care about balloons.",
 "You just need to see what happens.",
 "That feeling is tension. It's why you're still here.",
 "Most ads show everything in the first second. So people scroll.",
 "We build Reels for your product like this one.",
 "People stay to the end, and remember who made it.",
 "DM us DAILY. Your first one is free.",
 "See? You stayed.",
]
meta=[]
for i,t in enumerate(L):
    s,sr=k.create(t,voice=V,speed=SP,lang="en-us")
    a=np.abs(s); nz=np.where(a>0.01)[0]; s=s[max(0,nz[0]-240):nz[-1]+480]
    sf.write(f"/home/claude/r1/vo2/{V}_{i:02d}.wav",s,sr); meta.append({"i":i,"text":t,"dur":round(len(s)/sr,3)})
json.dump(meta,open(f"/home/claude/r1/vo2/{V}.json","w"),indent=1)
print(V, "total", round(sum(m["dur"] for m in meta),2), [m["dur"] for m in meta])
