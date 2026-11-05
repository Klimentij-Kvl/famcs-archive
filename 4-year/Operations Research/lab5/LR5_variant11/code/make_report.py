"""Создание PDF-отчёта в стиле предоставленного образца (ReportLab)."""
from pathlib import Path
import json, math, os
from statistics import NormalDist
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Line, Circle, String, Polygon, PolyLine
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'results/python_results.json').read_text(encoding='utf-8'))
a=json.loads((ROOT/'results/ampl_results.json').read_text(encoding='utf-8'))
font_candidates=[Path(os.environ.get('LAB_FONT_DIR','fonts')),Path('/System/Library/Fonts/Supplemental'),Path('/usr/share/fonts/truetype/dejavu'),Path('C:/Windows/Fonts')]
for directory in font_candidates:
    for regular,bold in [('Arial.ttf','Arial Bold.ttf'),('arial.ttf','arialbd.ttf'),('DejaVuSans.ttf','DejaVuSans-Bold.ttf')]:
        if (directory/regular).exists() and (directory/bold).exists():
            pdfmetrics.registerFont(TTFont('Body',str(directory/regular)))
            pdfmetrics.registerFont(TTFont('BodyBold',str(directory/bold)))
            break
    else: continue
    break
else: raise RuntimeError('Задайте LAB_FONT_DIR: папка с Arial или DejaVu Sans.')
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
W=495
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.7,leading=16.2,textColor=colors.HexColor('#333333'),spaceAfter=10),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9,leading=13,spaceAfter=8,textColor=colors.HexColor('#444444')),
 'h1':ParagraphStyle('h1',fontName='BodyBold',fontSize=23,leading=28,spaceAfter=10,textColor=colors.HexColor('#333333')),
 'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=14,leading=19,spaceBefore=8,spaceAfter=10,textColor=colors.HexColor('#333333')),
 'formula':ParagraphStyle('formula',fontName='Body',fontSize=12,leading=20,alignment=1,spaceBefore=6,spaceAfter=12),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=9.2,leading=12),
 'code':ParagraphStyle('code',fontName='Body',fontSize=8.1,leading=11,backColor=colors.HexColor('#f5f5f5'),borderPadding=8,spaceAfter=12)}
story=[]
def p(text,style='body'): story.append(Paragraph(text,styles[style]))
def formula(s):p(s,'formula')
def heading(s):
    p(s,'h1');story.append(HRFlowable(width='100%',thickness=.5,color=colors.HexColor('#dddddd'),spaceAfter=17))
def page(s): story.append(PageBreak());heading(s)
def table(rows,widths=None):
    rows=[[Paragraph(str(v),styles['cell']) for v in row] for row in rows]
    t=Table(rows,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#444444')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#bbbbbb')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),7)]))
    story.append(t);story.append(Spacer(1,12))
def f(x,n=3):
    if abs(x-round(x))<1e-9:return str(round(x))
    return f'{x:.{n}f}'.replace('.',',')
def path(q):return ' - '.join(r['data'][k][0] for k in q if k!=11)
def graph():
    d=Drawing(W,245)
    pos={0:(15,125),1:(78,125),2:(155,218),3:(155,125),4:(155,28),5:(250,170),6:(290,28),7:(385,170),8:(477,85)}
    critical=r['baseline']['critical'][0]
    shifts={0:(0,14),1:(-20,3),2:(0,15),3:(-20,-5),4:(0,15),5:(0,-18),6:(0,-16),7:(0,14),8:(15,-2),9:(10,12),10:(5,-16),11:(-23,0)}
    for k,e in enumerate(r['data']):
        x,y=pos[e[1]];xx,yy=pos[e[2]];dx=xx-x;dy=yy-y;length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
        x+=12*ux;y+=12*uy;xx-=14*ux;yy-=14*uy
        col=colors.HexColor('#333333')
        d.add(Line(x,y,xx,yy,strokeColor=col,strokeWidth=2.5 if k in critical else 1,strokeDashArray=[4,3] if k==11 else None))
        d.add(Polygon([xx,yy,xx-7*ux+3*uy,yy-7*uy-3*ux,xx-7*ux-3*uy,yy-7*uy+3*ux],fillColor=col,strokeColor=col))
        sx,sy=shifts[k];label=f'{e[0]} ({e[3]})'
        d.add(String((x+xx)/2+sx,(y+yy)/2+sy,label,fontName='Body',fontSize=9,textAnchor='middle'))
    for i,(x,y) in pos.items():
        d.add(Circle(x,y,12,fillColor=colors.white,strokeColor=colors.HexColor('#333333'),strokeWidth=1.3))
        d.add(String(x,y-3.5,str(i),fontName='BodyBold',fontSize=10,textAnchor='middle'))
    return d

heading('Лабораторная работа 5')
p('Ковалевский Климентий Евгеньевич, 4 курс 7 группа')
story.append(HRFlowable(width='100%',thickness=1,color=colors.gray,spaceBefore=8,spaceAfter=18))
p('Вариант 11. Задачи сетевого планирования','h2')
p('1. Постановка задачи','h1')
p('Дан проект из 11 работ с отношениями предшествования. Для каждой работы известны пессимистическая, наиболее вероятная и оптимистическая длительности, а также стоимость сокращения работы на один день.')
p('Требуется построить сетевой график и рассчитать его временные характеристики; исследовать трёхпараметрическую и двухпараметрическую вероятностные модели; найти наиболее дешёвый план и наиболее дешёвый план при минимальном сроке.')
p('Исходные данные','h2')
preds=['-','b1','b1','b1','b2','b3','b4','b5, b6','b5, b6, b7','b8, b9','b5, b6, b7']
table([['Работа','Предшественники','t<sub>пес</sub>','t<sub>вер</sub>','t<sub>опт</sub>','s<sub>k</sub>']]+[[e[0],preds[k],e[3],e[4],e[5],e[6]] for k,e in enumerate(r['data'][:11])],[58,167,65,65,65,65])
p('Директивный срок T<sub>дир</sub> = 28 дней. Надёжность γ = 0,90. Стоимость одного дня проекта S = 10 ден. ед. Все длительности и резервы далее приведены в днях.')
p('Источник задания: Плескунов М. А. Задачи сетевого планирования. Екатеринбург: Изд-во Урал. ун-та, 2014. Вариант 11, с. 56 (страница 57 PDF).','small')

page('2. Сетевой график')
p('Вершины обозначают события, стрелки - работы. В скобках указаны максимальные длительности. Критические работы выделены толстой линией, фиктивная работа f = (5, 6) - пунктиром.')
story.append(graph())
p('Фиктивная работа имеет нулевую длительность и передаёт зависимость от b5 и b6 работам b9 и b11. Работа b8 зависит от b5 и b6, но не зависит от b7. Событие 8 означает окончание b10 и b11.','small')
formula('T<sub>р</sub>(j) = max<sub>(i,j)</sub> {T<sub>р</sub>(i) + t<sub>ij</sub>},   T<sub>р</sub>(0) = 0')
formula('T<sub>п</sub>(i) = min<sub>(i,j)</sub> {T<sub>п</sub>(j) - t<sub>ij</sub>},   T<sub>п</sub>(8) = T<sub>р</sub>(8)')
b=r['baseline']
table([['Событие i','Ранний срок Tр','Поздний срок Tп','Резерв Tп - Tр']]+[[i,f(b['early'][i]),f(b['late'][i]),f(b['late'][i]-b['early'][i])] for i in range(9)],[100,130,135,130])
p('<b>Критический путь:</b> 0 - 1 - 3 - 5 - 7 - 8, то есть b1 - b3 - b6 - b8 - b10. Его длительность: 10 + 8 + 9 + 13 + 9 = <b>49 дней</b>.')

page('3. Резервы и напряжённость')
formula('r<sub>п</sub>(i,j) = T<sub>п</sub>(j) - T<sub>р</sub>(i) - t<sub>ij</sub>')
formula('r<sub>н</sub>(i,j) = T<sub>р</sub>(j) - T<sub>п</sub>(i) - t<sub>ij</sub>')
table([['Работа','Дуга','t','Tр(i)','Tп(j)','rп','rн']]+[[e[0],f'{e[1]} - {e[2]}',e[3],f(b['early'][e[1]]),f(b['late'][e[2]]),f(b['total'][k]),f(b['independent'][k])] for k,e in enumerate(r['data'])],[63,72,60,75,75,75,65])
p('По определению пособия независимый резерв не ограничивается снизу нулём. Для b7 он равен 32 - 23 - 10 = -1. Это означает, что при позднем наступлении события 4 невозможно завершить b7 к раннему сроку события 6.','small')
p('Коэффициенты напряжённости','h2')
p('Как в пособии (с. 9-10), некритическая дуга здесь означает обходной путь между событиями критического пути без его внутренних событий. Пусть a - длина замыкающего критического участка, b - длина обхода. Тогда R = a - b, N = b/a.')
table([['Обходной путь','a','b','R','N']]+[[' - '.join(map(str,v['vertices'])),f(v['a']),v['b'],f(v['reserve']),f(v['N'])] for v in r['detours']],[195,65,65,65,105])
p('Критическая зона (N &gt; 0,8): первые три обхода; резервная (N &lt; 0,6): последние два. Подкритическая зона пуста. Наиболее напряжённый обход 1 - 4 - 6 - 7: N = 0,967, резерв всего 1 день.','small')

page('4. Вероятностные модели')
p('Используем формулы пособия (с. 11-20). Обозначим a = t<sub>опт</sub>, m = t<sub>вер</sub>, b = t<sub>пес</sub>. Для обеих моделей применяется одна и та же оценка дисперсии:')
formula('μ<sub>3</sub> = (a + 4m + b)/6;   μ<sub>2</sub> = (2a + 3b)/5;   σ² = ((b - a)/6)²')
p('В основных расчётах промежуточные значения не округляем. Округление до целых дней, использованное в примере пособия для упрощения, отдельно рассмотрено в разделе 5.')
table([['Работа','μ<sub>3</sub>','μ<sub>2</sub>','σ²']]+[[e[0],f(r['pert3']['d'][k]),f(r['pert2']['d'][k]),f(r['pert3']['var'][k])] for k,e in enumerate(r['data'][:11])],[90,135,135,135])
p('Критические пути по средним длительностям','h2')
p('В трёхпараметрической модели критический путь b1 - b3 - b6 - b8 - b10 имеет длину 30 дней. В двухпараметрической модели два критических пути длиной 33,8 дня: b1 - b3 - b6 - b8 - b10 и b1 - b2 - b5 - b8 - b10.')
p('Согласно пособию, при нескольких критических путях выбираем путь с наибольшей дисперсией. Их дисперсии в двухпараметрической модели равны 8,277778 и 6,638889. Поэтому для обеих моделей используем первый путь.')
formula('σ²<sub>кр</sub> = (49 + 36 + 64 + 100 + 49)/36 = 149/18 ≈ 8,277778')
formula('σ<sub>кр</sub> = √(149/18) ≈ 2,877113 дня')
p('Предполагаются независимость длительностей работ и нормальная аппроксимация длительности выбранного критического пути. Это расчётные оценки PERT: математическое ожидание максимума случайных путей в общем случае не равно максимуму их средних.','small')

page('5. Вероятность и сроки')
p('Обозначим Φ стандартную нормальную функцию распределения. В отличие от функции Лапласа в пособии, Φ здесь уже включает слагаемое 0,5.')
formula('P(T ≤ 28) ≈ Φ((28 - μ<sub>кр</sub>)/σ<sub>кр</sub>)')
formula('I<sub>0,9973</sub> ≈ [μ<sub>кр</sub> - 3σ<sub>кр</sub>; μ<sub>кр</sub> + 3σ<sub>кр</sub>]')
formula('T<sub>0,90</sub> ≈ μ<sub>кр</sub> + Φ<sup>-1</sup>(0,90)σ<sub>кр</sub>,   Φ<sup>-1</sup>(0,90) ≈ 1,281552')
p('Здесь T<sub>0,90</sub> - односторонний 90%-й квантиль, а не абсолютный верхний предел. Центральному интервалу вероятности 0,90 соответствует другой коэффициент: 1,644854. Для требуемого срока завершения используем одностороннюю оценку.')
p3,p2=r['pert3'],r['pert2']
table([['Показатель','Три параметра','Два параметра'],['μкр',f(p3['mu']),f(p2['mu'])],['(28 - μкр)/σкр',f((28-p3['mu'])/p3['sigma']),f((28-p2['mu'])/p2['sigma'])],['P(T ≤ 28)',f(100*p3['probability'])+' %',f(100*p2['probability'])+' %'],['Интервал μкр ± 3σкр','; '.join(f(v) for v in p3['interval']),'; '.join(f(v) for v in p2['interval'])],['T<sub>0,90</sub>',f(p3['deadline90']),f(p2['deadline90'])],['Срок в целых днях','34','38']],[205,145,145])
p('Проверка альтернативных путей','h2')
rows=[['Полный путь (работы)','μ<sub>3</sub>','μ<sub>2</sub>','σ','P<sub>3</sub>, %','P<sub>2</sub>, %']]
for q in r['paths']:
    rows.append([path(q),f(sum(p3['d'][k] for k in q)),f(sum(p2['d'][k] for k in q)),f(math.sqrt(sum(p3['var'][k] for k in q))), f(100*NormalDist().cdf((28-sum(p3['d'][k] for k in q))/math.sqrt(sum(p3['var'][k] for k in q))),2), f(100*NormalDist().cdf((28-sum(p2['d'][k] for k in q))/math.sqrt(sum(p2['var'][k] for k in q))),2)])
table(rows,[220,55,55,55,55,55])
p('P<sub>3</sub> и P<sub>2</sub> - вероятности завершения отдельного пути к 28-му дню. Наибольший 90%-й квантиль в обеих моделях имеет путь b1 - b3 - b6 - b8 - b10. Для двухпараметрической модели минимум вероятности равен 1,219 % на другом критическом пути; это уточнение рассмотрено далее.','small')

page('5.1. Сравнение моделей')
p('Двухпараметрическая модель оценивает срок на 3,8 дня больше: 33,8 вместо 30 дней. Вероятность уложиться в 28 дней снижается с 24,348 % до 2,190 %. Для надёжности 0,90 требуется соответственно около 34 и 38 полных дней.')
p('Трёхпараметрическая модель использует наиболее вероятную длительность каждой работы. Двухпараметрическая модель учитывает только крайние оценки, причём пессимистической длительности придаёт вес 3/5. Поэтому для данного варианта она даёт более осторожный прогноз.')
p('При сроке 28 дней, меньшем среднего 33,8, выбор максимальной дисперсии по правилу пособия не даёт наихудшую вероятность. Второй критический путь b1 - b2 - b5 - b8 - b10 даёт 1,219 %. В рамках нормальных оценок вероятность завершения всей сети не больше этой величины, поскольку должны завершиться оба пути. Значение 2,190 % в основной таблице - оценка по выбранному в пособии правилу, а не точная совместная вероятность.','small')
p('Расчёт с округлением, как в примере пособия','h2')
p('На с. 12 пособия средние длительности округляются до целых чисел. Ниже приведён результат при таком соглашении: округляется каждая работа, значения вида n + 0,5 округляются вверх; дисперсии сохраняются без промежуточного округления.')
r3,r2=r['pert3_rounded'],r['pert2_rounded']
table([['Показатель','Три параметра','Два параметра'],['μкр после округления',f(r3['mu']),f(r2['mu'])],['P(T ≤ 28)',f(100*r3['probability'])+' %',f(100*r2['probability'])+' %'],['Интервал ±3σ','; '.join(f(v) for v in r3['interval']),'; '.join(f(v) for v in r2['interval'])],['T<sub>0,90</sub>',f(r3['deadline90']),f(r2['deadline90'])],['Срок в целых днях','35','38']],[205,145,145])
p('Разница вызвана исключительно округлением исходных средних. Для основной оценки используются дробные длительности: Python и AMPL не требуют округления до целых дней.')
p('Интерпретация интервала «трёх сигм»','h2')
p('В терминологии задания это интервал гарантированного времени с вероятностью 0,9973. Строго говоря, указанная вероятность относится к нормальной аппроксимации выбранного пути; она не является безусловной гарантией для всей случайной сети. Конкурирующие пути используют общие работы и потому зависимы.')
p('Для сравнения детерминированные границы длительности проекта, полученные при всех t<sub>опт</sub> и всех t<sub>пес</sub>, составляют 14 и 49 дней. Вероятностные оценки в основных расчётах лежат внутри этих границ.')

page('6. Оптимизация стоимости')
p('Пусть x<sub>k</sub> - сокращение работы b<sub>k</sub> в днях, y<sub>i</sub> - время наступления события i. Тогда фактическая длительность работы t<sub>k</sub> = t<sub>max,k</sub> - x<sub>k</sub>, а T = y<sub>8</sub>.')
formula('0 ≤ x<sub>k</sub> ≤ t<sub>max,k</sub> - t<sub>min,k</sub>;   y<sub>0</sub> = 0;   y<sub>i</sub> ≥ 0')
formula('y<sub>j</sub> - y<sub>i</sub> ≥ t<sub>max,k</sub> - x<sub>k</sub>   для каждой работы k = (i,j)')
formula('y<sub>6</sub> ≥ y<sub>5</sub>   для фиктивной работы f')
formula('min C = 10T + Σ<sub>k=1..11</sub> s<sub>k</sub>x<sub>k</sub>')
p('Стоимость состоит из затрат на длительность проекта и дополнительных затрат на ускорение. Постоянная базовая стоимость работ в задании не указана и в модель не добавляется. Переменные непрерывны; найденные оптимальные планы имеют целочисленные длительности.')
p('Первый результат: наиболее дешёвый план','h2')
o=r['opt'];fast=r['fast']
table([['Работа','tmax','Сокращение x','Длительность t','Затраты s·x']]+[[e[0],e[3],f(o['x'][k]),f(o['d'][k]),f(e[6]*o['x'][k])] for k,e in enumerate(r['data'][:11])],[70,85,115,115,110])
formula('C* = 10 · 30 + 5 · 7 + 6 · 5 + 1 · 6 + 3 · 6 = 389')
p('<b>Оптимальный срок T* = 30 дней.</b> Ускорение стоит 89 ден. ед. По сравнению с исходным планом стоимость снижается с 490 до 389 ден. ед., то есть на 101 ден. ед. (20,61 %).')
p('Ранние сроки событий оптимального плана: (0; 3; 12; 11; 10; 20; 20; 27; 30). В AMPL допустим иной момент некритического события 2; это не меняет длительности работ и стоимость.','small')

page('7. Минимально возможный срок')
p('Задачу решаем лексикографически: сначала минимизируем T, затем при T ≤ T<sub>min</sub> минимизируем стоимость. Сокращать абсолютно все работы до t<sub>min</sub> не требуется: часть затрат была бы лишней.')
p('Нижнюю границу задаёт путь b1 - b2 - b5 - b8 - b10: сумма его минимальных длительностей равна 3 + 4 + 2 + 3 + 2 = 14. Следующий допустимый план достигает этой границы, поэтому <b>T<sub>min</sub> = 14 дней</b>.')
table([['Работа','Сокращение x','Длительность t','Затраты s·x']]+[[e[0],f(fast['x'][k]),f(fast['d'][k]),f(e[6]*fast['x'][k])] for k,e in enumerate(r['data'][:11])],[95,135,135,130])
formula('C(T<sub>min</sub>) = 10 · 14 + 328 = 468 ден. ед.')
p('Ранние сроки событий: (0; 3; 7; 8; 4; 9; 9; 12; 14). Все восемь полных путей имеют длину 14 дней. Работы b3, b7, b9 и b11 при этом остаются длиннее своих минимальных длительностей.')
all_extra=sum(e[6]*(e[3]-e[5]) for e in r['data'][:11])
p(f'Если сократить все работы до минимума, затраты на ускорение составят {all_extra} ден. ед., общая стоимость - {140+all_extra}. Найденный план сохраняет срок 14 дней и экономит {all_extra-328} ден. ед.')
p('Дополнительно: выполнение директивного срока','h2')
v28=next(v for v in r['frontier'] if v['deadline']==28)
p('В пункте 2 задания срок 28 дней используется для вероятностной оценки. В основную задачу минимизации стоимости он не включён как обязательное ограничение. Если потребовать T ≤ 28, получаем отдельный результат:')
formula(f'T = 28;   C<sub>уск</sub> = {f(v28["extra"])};   C = {f(v28["cost"])} ден. ед.')
p('Один соответствующий вектор длительностей (b1, …, b11): '+', '.join(f(v) for v in v28['d'][:11])+'.')

page('8. Проверка оптимальности')
p('Модели независимо заданы в Python (SciPy/HiGHS) и в AMPL/HiGHS. Оба запуска завершились со статусом optimal. Совпали длительности проектов, общие затраты и затраты на ускорение. Дополнительно сопоставлены решения для всех 36 целых сроков от 14 до 49 дней.')
table([['Режим','Python: T / C','AMPL: T / C'],['Минимальная стоимость','30 / 389','30 / 389'],['Минимальный срок','14 / 468','14 / 468'],['Срок не более 28 дней','28 / 392','28 / 392']],[215,140,140])
p('Минимальная стоимость при фиксированном сроке','h2')
p('Для каждого срока τ сначала минимизированы затраты на ускорение при T ≤ τ. В данном варианте полученные планы достигают τ. К затратам на ускорение затем добавлено 10τ.','small')
front=r['frontier']
rows=[['T','Cуск','Cобщ','T','Cуск','Cобщ','T','Cуск','Cобщ']]
for j in range(12):
    row=[]
    for index in [j,j+12,j+24]:
        v=front[index];row += [v['deadline'],f(v['extra']),f(v['cost'])]
    rows.append(row)
table(rows,[44,55,66]*3)
p('Проверка ограничений','h2')
p('Программа проверяет границы длительностей и все ограничения предшествования; перечисляет восемь полных путей и проверяет, что ни один из них не превышает найденный срок. Для самого быстрого плана нижняя граница 14 дней доказана суммой минимальных длительностей одного пути.')
p('Оптимальность непрерывной модели устанавливается решателем линейного программирования; перебор целых сроков служит дополнительной проверкой. Файлы результатов содержат исходные значения полной точности и журналы запусков.','small')

page('9. Программная реализация')
p('Python: прямой и обратный проход по событиям','h2')
code='''def cpm(d):
    early = [0.0] * N
    for j in range(1, N):
        early[j] = max(early[e[1]] + d[k]
            for k, e in enumerate(DATA) if e[2] == j)
    late = [early[-1]] * N
    for i in reversed(range(N - 1)):
        late[i] = min(late[e[2]] - d[k]
            for k, e in enumerate(DATA) if e[1] == i)
    # Резервы, критические пути и полная проверка:
    # см. solve_python.py в архиве.
'''
story.append(Preformatted(code,styles['code']))
p('AMPL: основные ограничения и целевая функция','h2')
code='''var x {k in B} >= 0, <= tmax[k] - tmin[k];
var y {V} >= 0;
s.t. Start: y[source] = 0;
s.t. Precedence {k in B}:
    y[head[k]] >= y[tail[k]] + tmax[k] - x[k];
minimize TotalCost:
    S*y[sink] + sum{k in B} price[k]*x[k];
minimize Duration: y[sink];
'''
story.append(Preformatted(code,styles['code']))
p('Для минимального срока сначала выбирается цель Duration, сохраняется T<sub>min</sub>, затем добавляется ограничение y[sink] ≤ T<sub>min</sub> и выбирается цель TotalCost.')
p('Файлы в архиве','h2')
table([['Файл','Назначение'],['code/solve_python.py','CPM, PERT, оптимизация и проверки'],['code/model.mod; variant11.dat','Модель AMPL и данные варианта 11'],['code/solve.run','Самостоятельный запуск в AMPL'],['code/solve_ampl.py','Запуск AMPL из Python и сравнение'],['code/make_report.py','Воспроизводимое создание отчёта'],['results/; README.md','Результаты, журналы и инструкция']],[225,270])

page('10. Выводы')
p('Для исходного проекта критический путь b1 - b3 - b6 - b8 - b10 имеет длительность <b>49 дней</b>. Наиболее напряжённый некритический обход проходит через работы b4, b7 и b9; его резерв составляет один день.')
p('Без промежуточного округления трёхпараметрическая модель даёт ожидаемый критический срок <b>30 дней</b> и вероятность выполнения за 28 дней около <b>24,35 %</b>. Двухпараметрическая модель даёт <b>33,8 дня</b> и оценку по пути максимальной дисперсии около <b>2,19 %</b>; другой критический путь даёт <b>1,219 %</b>, что ограничивает сверху вероятность завершения всей сети в рамках нормальной модели. Односторонние сроки надёжности 0,90 составляют 33,687 и 37,487 дня, или 34 и 38 полных дней.')
p('Минимальная стоимость проекта равна <b>389 ден. ед.</b> при сроке <b>30 дней</b>. Минимально возможный срок равен <b>14 дням</b>; наименьшая стоимость при таком сроке составляет <b>468 ден. ед.</b>. При дополнительном ограничении T ≤ 28 дней минимальная стоимость равна <b>392 ден. ед.</b>')
p('Результаты Python и AMPL совпали. Таким образом, минимальный срок и минимальная стоимость достигаются разными планами: ускорение с 30 до 14 дней увеличивает общую стоимость на 79 ден. ед.')
p('Источники','h2')
p('1. Плескунов М. А. Задачи сетевого планирования: учебное пособие / науч. ред. А. И. Короткий. Екатеринбург: Изд-во Урал. ун-та, 2014. 92 с. ISBN 978-5-7996-1167-5. Метод критического пути: с. 6-10; вероятностные модели: с. 11-20; оптимизация: с. 21-45; вариант 11: с. 56.','small')
p('2. AMPL. Initial Setup: установка Python API и решателя HiGHS. <link href="https://amplpy.ampl.com/en/stable/getting-started.html" color="#333333">https://amplpy.ampl.com/en/stable/getting-started.html</link>.','small')
p('3. Образец оформления: предоставленный отчёт «Лабораторная работа 4», файл 7b_Kovalevskij_4_16.pdf.','small')

def footer(c,doc):
    c.setFont('Body',8);c.setFillColor(colors.gray)
    c.drawRightString(545,25,str(doc.page))
doc=SimpleDocTemplate(str(ROOT/'LR5_variant11_report.pdf'),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=42,bottomMargin=40,title='Лабораторная работа 5. Вариант 11',author='Ковалевский Климентий Евгеньевич')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(ROOT/'LR5_variant11_report.pdf')
