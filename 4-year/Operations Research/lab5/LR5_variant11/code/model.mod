# ЛР 5. Непрерывная модель время-стоимость.
set V ordered;
set B ordered;
param source symbolic in V;
param sink symbolic in V;
param tail {B} symbolic in V;
param head {B} symbolic in V;
param tmax {B} >= 0;
param tmin {k in B} >= 0, <= tmax[k];
param price {B} >= 0;
param S >= 0;
param deadline default 100000;
param Tmin default 0;
var x {k in B} >= 0, <= tmax[k]-tmin[k];
var y {V} >= 0;
s.t. Start: y[source] = 0;
s.t. Precedence {k in B}: y[head[k]] >= y[tail[k]]+tmax[k]-x[k];
s.t. Deadline: y[sink] <= deadline;
s.t. Fastest: y[sink] <= Tmin;
minimize TotalCost: S*y[sink]+sum{k in B} price[k]*x[k];
minimize Duration: y[sink];

minimize CrashCost: sum{k in B} price[k]*x[k];
