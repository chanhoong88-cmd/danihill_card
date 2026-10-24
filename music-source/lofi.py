# Original soft lofi wedding loop for the Dani Hill e-card (composed procedurally, royalty-free).
import numpy as np
from scipy.signal import butter, sosfilt
SR=44100; BPM=72; BEAT=60/BPM; BAR=4*BEAT; BARS=16
L=int(round(BARS*BAR*SR))
mix=np.zeros((L,2))
rng=np.random.default_rng(7)
mf=lambda m: 440*2**((m-69)/12)

def add(sig,start,pan=0.0,gain=1.0):
    i0=int(round(start*SR))%L
    n=len(sig); idx=(np.arange(n)+i0)%L
    l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    np.add.at(mix[:,0],idx,sig*gain*l*1.414); np.add.at(mix[:,1],idx,sig*gain*r*1.414)

def ep(m,dur,vel=1.0,cents=0.0):            # warm electric piano (Rhodes-like FM)
    f=mf(m)*2**(cents/1200); n=int((dur+2.2)*SR); t=np.arange(n)/SR
    idx=2.2*np.exp(-t*7)
    car=np.sin(2*np.pi*f*t+idx*np.sin(2*np.pi*f*t))+0.18*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)
    env=np.minimum(t/0.006,1)*np.exp(-t/1.7)
    rel=np.clip(1-(t-dur)/0.6,0,1); env*=np.where(t>dur,rel,1)
    return car*env*vel
def bell(m,dur,vel=1.0):                    # soft music-box melody
    f=mf(m); n=int((dur+1.8)*SR); t=np.arange(n)/SR
    s=np.sin(2*np.pi*f*t)+0.22*np.sin(2*np.pi*3*f*t)*np.exp(-t*4)+0.08*np.sin(2*np.pi*4.01*f*t)*np.exp(-t*6)
    env=np.minimum(t/0.004,1)*np.exp(-t/1.1)
    return s*env*vel
def pad(m,dur,vel=1.0):                     # airy sustained pad
    f=mf(m); n=int((dur+1.5)*SR); t=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*(1+d)*t+ph) for d,ph in [(-.003,0),(0,1.1),(.003,2.3)])/3
    s+=0.2*np.sin(2*np.pi*2*f*t)
    env=np.clip(t/1.2,0,1)*np.where(t>dur,np.clip(1-(t-dur)/1.5,0,1),1)
    return s*env*vel
def bass(m,dur,vel=1.0):
    f=mf(m); n=int((dur+0.4)*SR); t=np.arange(n)/SR
    s=np.tanh(1.6*np.sin(2*np.pi*f*t))/np.tanh(1.6)
    env=np.minimum(t/0.012,1)*np.exp(-t/2.4)*np.where(t>dur,np.clip(1-(t-dur)/0.3,0,1),1)
    return s*env*vel
def kick():
    n=int(.45*SR); t=np.arange(n)/SR; f=45+65*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/0.16)
def noise_hit(lo,hi,decay,n_s=.4):
    n=int(n_s*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
    x=sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
    return x*np.exp(-t/decay)*np.minimum(t/0.003,1)

# chords: (bass root, voicing)
CH=[(41,[57,60,64,67]),(40,[55,59,62,64]),(38,[53,57,60,64]),(36,[52,55,59,62])]   # Fmaj9 Em7 Dm9 Cmaj9
for bar in range(BARS):
    root,voi=CH[(bar//2)%4]; b0=bar*BAR; first=(bar%2==0)
    hits=[(0,1.7,1.0),(2.5,1.3,.62)] if first else [(0,1.2,.78),(1.5,.5,.45),(3.5,.5,.5)]
    for beat,d,v in hits:
        for k,m in enumerate(voi):
            st=b0+beat*BEAT+k*0.016+rng.uniform(0,.008)
            add(ep(m,d*BEAT,v*.16,cents=-5),st,-.35); add(ep(m,d*BEAT,v*.16,cents=5),st,.35)
    if first:
        for m in voi[1:]: add(pad(m+12,2*BAR-.3,.035),b0,rng.uniform(-.5,.5))
    add(bass(root,1.8*BEAT,.42),b0); add(bass(root+7 if not first else root,.9*BEAT,.26),b0+2.5*BEAT)
    # soft swung drums (start gently, fuller in bars 2+)
    dg=.55 if bar<2 else 1.0
    for beat in (0,2.5): add(kick(),b0+beat*BEAT,0,.5*dg)
    for beat in (1,3): add(noise_hit(1200,5200,.11),b0+beat*BEAT,.1,.09*dg)
    for e in range(8):
        sw=.09 if e%2 else 0; v=(.05 if e%2 else .075)*rng.uniform(.75,1.1)
        add(noise_hit(6000,11000,.035,.12),b0+(e*.5+sw)*BEAT,.3,v*dg)

MEL=[(8,0,76,1.5),(8,1.5,74,.5),(8,2,72,1),(8,3,69,1),(9,0,72,2),(9,2.5,74,.5),(9,3,76,1),
     (10,0,74,1.5),(10,1.5,71,.5),(10,2,67,2),(11,0,71,1),(11,1,72,1),(11,2,74,2),
     (12,0,72,1.5),(12,1.5,69,.5),(12,2,65,1),(12,3,69,1),(13,0,72,3),
     (14,0,71,1),(14,1,67,1),(14,2,64,2),(15,0,67,1),(15,1,71,1),(15,2,72,2),
     (2,0,79,2),(3,2,76,2),(4,0,74,2),(5,2,71,2),(6,0,72,2),(7,2,67,2)]   # sparse first-half echoes
for bar,beat,m,d in MEL:
    v=.11 if bar>=8 else .055
    add(bell(m,d*BEAT,v),bar*BAR+beat*BEAT+rng.uniform(0,.01),.15)
    add(bell(m,d*BEAT,v*.28),bar*BAR+beat*BEAT+.375*BEAT,-.4)   # soft echo

# ---- lofi master (circular processing keeps the loop seamless) ----
def circ(x,sos):
    y=sosfilt(sos,np.concatenate([x,x,x],axis=0),axis=0); return y[L:2*L]
mix=circ(mix,butter(2,[45,4800],'band',fs=SR,output='sos'))
# tape wow: integer cycles across the loop
t=np.arange(L)/SR; cyc=round((L/SR)*0.45)
d=0.0016*SR*(1+np.sin(2*np.pi*cyc*np.arange(L)/L))/2
src=(np.arange(L)-d)%L; i0=np.floor(src).astype(int); fr=src-i0
mix=mix[i0]*(1-fr)[:,None]+mix[(i0+1)%L]*fr[:,None]
# vinyl: gentle hiss + sparse crackle
hiss=circ(rng.standard_normal((L,2))*.004,butter(2,[800,6000],'band',fs=SR,output='sos'))
cr=np.zeros((L,2)); pos=rng.choice(L,int(L/SR*9),replace=False)
cr[pos]=rng.uniform(-.25,.25,(len(pos),2))*rng.uniform(.2,1,(len(pos),1))
cr=circ(cr,butter(2,[1500,7000],'band',fs=SR,output='sos'))*.35
mix=mix+hiss+cr
mix=np.tanh(mix*1.4)/1.4
mix=mix/np.max(np.abs(mix))*0.82
import soundfile as sf
sf.write('/home/claude/music/lofi.wav',mix.astype(np.float32),SR)
print('seconds',L/SR)
