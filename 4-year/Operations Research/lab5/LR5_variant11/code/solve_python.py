"""ЛР 5, вариант 11. CPM, PERT и линейная оптимизация (SciPy/HiGHS)."""
from pathlib import Path
import json
from math import sqrt, floor
from statistics import NormalDist
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
# k, начальное событие, конечное событие, tmax, tmode, tmin, цена сокращения
DATA = [
 ('b1',0,1,10,7,3,5), ('b2',1,2,9,6,4,3),
 ('b3',1,3,8,5,2,8), ('b4',1,4,12,7,1,6),
 ('b5',2,5,6,3,2,2), ('b6',3,5,9,6,1,6),
 ('b7',4,6,10,4,3,9), ('b8',5,7,13,8,3,1),
 ('b9',6,7,7,5,1,4), ('b10',7,8,9,4,2,3),
 ('b11',6,8,10,9,4,8), ('f',5,6,0,0,0,0)]
N = 9
S = 10

def all_paths(start=0, finish=8):
    if start == finish:
        return [[]]
    return [[k] + p for k,e in enumerate(DATA) if e[1] == start
            for p in all_paths(e[2], finish)]

PATHS = all_paths()

def cpm(d):
    early = [0.0]*N
    for j in range(1,N):
        early[j] = max(early[e[1]]+d[k] for k,e in enumerate(DATA) if e[2]==j)
    late = [early[-1]]*N
    for i in reversed(range(N-1)):
        late[i] = min(late[e[2]]-d[k] for k,e in enumerate(DATA) if e[1]==i)
    total = [late[e[2]]-early[e[1]]-d[k] for k,e in enumerate(DATA)]
    independent = [early[e[2]]-late[e[1]]-d[k] for k,e in enumerate(DATA)]
    critical = [p for p in PATHS if abs(sum(d[k] for k in p)-early[-1])<1e-7]
    return dict(T=early[-1], early=early, late=late, total=total,
                independent=independent, critical=critical)

def pert(two=False, rounded=False):
    d = [(3*e[3]+2*e[5])/5 if two else (e[3]+4*e[4]+e[5])/6 for e in DATA]
    if rounded:
        d = [floor(x+0.5) for x in d]  # округление .5 вверх, как в пособии
    var = [((e[3]-e[5])/6)**2 for e in DATA]
    cp = cpm(d)
    p = max(cp['critical'], key=lambda p:sum(var[k] for k in p))
    variance = sum(var[k] for k in p)
    sigma = sqrt(variance)
    mu = cp['T']
    normal = NormalDist()
    return dict(d=d,var=var,path=p,mu=mu,variance=variance,sigma=sigma,
                probability=normal.cdf((28-mu)/sigma),
                interval=[mu-3*sigma,mu+3*sigma],
                deadline90=mu+normal.inv_cdf(0.9)*sigma,
                central90=[mu-normal.inv_cdf(.95)*sigma,mu+normal.inv_cdf(.95)*sigma])

def optimize(deadline=None, objective='cost'):
    # Переменные: x[0:11] - сокращения работ, y[11:20] - сроки событий.
    c = np.zeros(20)
    if objective=='time':
        c[-1] = 1
    else:
        c[:11] = [e[6] for e in DATA[:11]]
        c[-1] = 0 if objective=='extra' else S
    rows, rhs = [], []
    for k,e in enumerate(DATA):
        row = np.zeros(20)
        row[11+e[1]],row[11+e[2]] = 1,-1
        if k<11: row[k] = -1
        rows.append(row); rhs.append(-e[3])
    if deadline is not None:
        row = np.zeros(20); row[-1]=1
        rows.append(row); rhs.append(deadline)
    bounds = [(0,e[3]-e[5]) for e in DATA[:11]]+[(0,0)]+[(0,None)]*8
    result = linprog(c,A_ub=rows,b_ub=rhs,bounds=bounds,method='highs')
    if not result.success: raise RuntimeError(result.message)
    x = result.x[:11]
    d = [e[3]-x[k] for k,e in enumerate(DATA[:11])]+[0]
    cp = cpm(d)
    extra = sum(e[6]*x[k] for k,e in enumerate(DATA[:11]))
    assert np.min(np.array(rhs)-np.array(rows)@result.x)>-1e-7
    assert abs(cp['T']-result.x[-1])<1e-7
    return dict(T=cp['T'],extra=float(extra),cost=float(S*cp['T']+extra),
                x=x.tolist(),d=d,events=cp['early'],critical=cp['critical'],
                status=result.message)

def main():
    baseline = cpm([e[3] for e in DATA])
    opt = optimize()
    fast_time = optimize(objective='time')['T']
    fast = optimize(deadline=fast_time)
    frontier = [dict(deadline=t, **optimize(deadline=t, objective='extra')) for t in range(int(fast_time),int(baseline['T'])+1)]
    # Независимая проверка через все полные пути.
    for sol in [opt,fast]+frontier:
        assert all(sum(sol['d'][k] for k in p)<=sol['T']+1e-7 for p in PATHS)
    assert abs(min(r['cost'] for r in frontier)-opt['cost'])<1e-7
    detours=[]
    critical=baseline['critical'][0]
    vertices=[0]+[DATA[k][2] for k in critical]
    for i in vertices:
        for j in vertices:
            if j<=i: continue
            for p in all_paths(i,j):
                inside=[DATA[k][2] for k in p[:-1]]
                if any(v in vertices for v in inside): continue
                if all(k in critical for k in p): continue
                a=baseline['early'][j]-baseline['early'][i]
                b=sum(DATA[k][3] for k in p)
                detours.append(dict(vertices=[i]+[DATA[k][2] for k in p],a=a,b=b,reserve=a-b,N=b/a))
    # Проверка всех альтернативных путей по вероятности и квантилю.
    alternatives = []
    for model in [pert(), pert(True)]:
        stats = []
        for p in PATHS:
            mu = sum(model['d'][k] for k in p)
            sigma = sqrt(sum(model['var'][k] for k in p))
            stats.append(dict(path=p, mu=mu, sigma=sigma, probability=NormalDist().cdf((28-mu)/sigma), deadline90=mu+NormalDist().inv_cdf(.9)*sigma))
            assert mu+NormalDist().inv_cdf(.9)*sigma <= model['deadline90']+1e-9
        alternatives.append(stats)
    out=dict(alternatives=alternatives, data=DATA,paths=PATHS,baseline=baseline,detours=detours,
             pert3=pert(),pert2=pert(True),pert3_rounded=pert(rounded=True),
             pert2_rounded=pert(True,True),opt=opt,fast=fast,frontier=frontier)
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/python_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:out[k] for k in ['baseline','pert3','pert2','opt','fast','detours']},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
