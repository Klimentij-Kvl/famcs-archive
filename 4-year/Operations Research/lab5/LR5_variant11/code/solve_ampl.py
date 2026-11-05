"""Запуск AMPL/HiGHS и сравнение с независимо заданной моделью SciPy."""
from pathlib import Path
import json
from amplpy import AMPL
from solve_python import DATA, cpm
ROOT = Path(__file__).resolve().parents[1]

def capture(a):
    x = [a.get_value(f'x["{e[0]}"]') for e in DATA]
    d = [e[3]-x[k] for k,e in enumerate(DATA)]
    t = a.get_value('y[sink]')
    cost = a.get_value('TotalCost')
    assert a.get_value('solve_result') == 'solved'
    assert abs(cpm(d)['T']-t)<1e-6
    return dict(T=t,cost=cost,x=x,d=d,extra=cost-10*t,
                events=[a.get_value(f'y[{i}]') for i in range(9)])

def main():
    a = AMPL()
    a.read(str(ROOT/'code/model.mod'))
    a.read_data(str(ROOT/'code/variant11.dat'))
    a.option['solver']='highs'
    log = a.get_output('drop Fastest; objective TotalCost; solve;')
    opt=capture(a)
    log += a.get_output('objective Duration; solve; let Tmin := y[sink]; restore Fastest; objective TotalCost; solve;')
    fast=capture(a)
    py=json.loads((ROOT/'results/python_results.json').read_text(encoding='utf-8'))
    for key,sol in [('opt',opt),('fast',fast)]:
        for metric in ['T','cost','extra']:
            assert abs(sol[metric]-py[key][metric])<1e-6,(key,metric)
    # Проверка всей кривой затрат. Разные оптимальные векторы допустимы.
    a.eval('drop Fastest; objective CrashCost;')
    for row in py['frontier']:
        a.param['deadline']=row['deadline']
        log += a.get_output('solve;')
        sol=capture(a)
        assert abs(sol['cost']-row['cost'])<1e-6
    out=dict(opt=opt,fast=fast,checked_deadlines=len(py['frontier']),comparison='PASS')
    (ROOT/'results/ampl_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'results/ampl_log.txt').write_text(log,encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2))
    a.close()

if __name__=='__main__': main()
