import numpy as np, json, csv, datetime as dt
rng=np.random.default_rng(20261111)
ACTS=['Doblar hoja','Ensobrar y cerrar','Etiquetar y apilar']
N=15
SPEC={'AS-IS':{'m':[7.4,12.6,6.3],'s':[0.55,1.05,0.50]},
      'TO-BE':{'m':[7.1,9.4,5.6],'s':[0.50,0.70,0.45]}}
rows=[]; data={}
t0={'AS-IS':dt.datetime(2026,11,11,13,0,0),'TO-BE':dt.datetime(2026,11,11,13,40,0)}
for sc in SPEC:
    true=np.array([[max(2.0,SPEC[sc]['m'][a]+SPEC[sc]['s'][a]*rng.standard_normal()) for a in range(3)] for c in range(N)])
    flat=true.flatten(); nb=len(flat)+1
    bounds=np.concatenate([[0],np.cumsum(flat)])
    # video: fronteras redondeadas a cuadros de 30 fps
    vb=np.round(bounds*30)/30
    # cámara: detección a ~15 fps + desfase de la mano al entrar/salir de la zona
    cb=bounds+rng.normal(0.04,0.11,nb); cb=np.round(cb*15)/15
    # cronómetro manual (método continuo): error de reacción en cada lectura
    mb=bounds+rng.normal(0.18,0.24,nb)
    video=np.diff(vb).reshape(N,3); cam=np.diff(cb).reshape(N,3); man=np.round(np.diff(mb),2).reshape(N,3)
    # un error de anotación/transcripción en la hoja manual por escenario (+1,8 s)
    c,a=(8,1) if sc=='AS-IS' else (5,0)
    man[c,a]=man[c,a]+1.8
    data[sc]={'video':np.round(video,2).tolist(),'camara':np.round(cam,2).tolist(),'manual':np.round(man,2).tolist(),'true':true.tolist()}
    for src in ['camara','manual','video']:
        arr=np.round({'video':video,'camara':cam,'manual':man}[src],2)
        t=t0[sc]
        for ci in range(N):
            for ai in range(3):
                t+=dt.timedelta(seconds=float(arr[ci,ai]))
                rows.append([f"sim-{sc}-{src}-{ci+1}-{ai+1}",t.isoformat()+'Z',sc,ai+1,ACTS[ai],ci+1,float(arr[ci,ai]),src])
with open('/home/claude/sim/OptiTime_datos_simulados.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['id','fecha_hora','escenario','actividad_n','actividad','ciclo','tiempo_s','fuente']); w.writerows(rows)
json.dump(data,open('/home/claude/sim/data.json','w'))
# ---- resumen (mismas fórmulas que la app) ----
V,S=1.00,0.15
def st(x):
    x=np.array(x);n=len(x);s1=x.sum();s2=(x*x).sum()
    return dict(n=n,mean=x.mean(),sd=x.std(ddof=1),cv=x.std(ddof=1)/x.mean(),nreq=(40*np.sqrt(n*s2-s1*s1)/s1)**2)
R={}
for sc in SPEC:
    cam=np.array(data[sc]['camara']); per=[]
    for a in range(3):
        d=st(cam[:,a]); d['TN']=d['mean']*V; d['TE']=d['TN']*(1+S); d['cap']=3600/d['TE']; per.append(d)
    sumTE=sum(p['TE'] for p in per); maxTE=max(p['TE'] for p in per)
    R[sc]=dict(per=per,sumTE=sumTE,cap1=3600/sumTE,capLine=3600/maxTE,prodLine=3600/maxTE/3,bal=sumTE/(3*maxTE),bn=int(np.argmax([p['TE'] for p in per])))
for sc in R:
    print(sc)
    for a,p in enumerate(R[sc]['per']): print(f"  {ACTS[a]:20s} n={p['n']} TO={p['mean']:.2f} sd={p['sd']:.2f} CV={p['cv']:.3f} nreq={p['nreq']:.1f} TE={p['TE']:.2f} cap={p['cap']:.1f}")
    print(f"  ciclo TO={sum(p['mean'] for p in R[sc]['per']):.2f} sumTE={R[sc]['sumTE']:.2f} cap1={R[sc]['cap1']:.1f} capLine={R[sc]['capLine']:.1f} prodLine={R[sc]['prodLine']:.1f} bal={R[sc]['bal']:.3f} bn={ACTS[R[sc]['bn']]}")
# precisión
for src in ['manual','camara']:
    e=[];ref=[]
    for sc in SPEC:
        e+= (np.array(data[sc][src])-np.array(data[sc]['video'])).flatten().tolist(); ref+=np.array(data[sc]['video']).flatten().tolist()
    e=np.array(e);ref=np.array(ref)
    print(src,'pares',len(e),'MAE',abs(e).mean().round(3),'MAPE%',(abs(e)/ref*100).mean().round(2),'sesgo',e.mean().round(3),'max',abs(e).max().round(2))
