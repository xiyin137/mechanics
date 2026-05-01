(* Restricted Sun-Jupiter asteroid ejection probability demo.

   Authors: GPT 5.5 and Xi Yin.

   This is a compact Mathematica companion to the Python ensemble simulation.
   It favors readability over speed. For large ensembles use the Python script.
   Unlike the Python demo, this notebook companion detects ejection only: it
   does not classify solar collisions, close Jupiter encounters, or write CSV.

   Run with:
     wolframscript -file demos/mathematica/AsteroidEjectionProbability.wl
*)

ClearAll["Global`*"];

g = 4 Pi^2;
mSun = 1.0;
mJupiter = 9.543*10^-4;
aJupiter = 5.2044;
nJupiter = Sqrt[g (mSun + mJupiter)/aJupiter^3];
ejectionRadius = 20.0;
tmax = 50.0;
particles = 32;

rJ[t_] := aJupiter {Cos[nJupiter t], Sin[nJupiter t]};

acceleration[t_, r_] := Module[{sun, diff, direct, indirect},
  sun = -g mSun r/Norm[r]^3;
  diff = r - rJ[t];
  direct = -g mJupiter diff/Norm[diff]^3;
  indirect = -g mJupiter rJ[t]/Norm[rJ[t]]^3;
  sun + direct + indirect
];

SeedRandom[7];

sampleInitialCondition[] := Module[
  {a, e, mean, peri, ecc, f, p, rr, root, xOrb, yOrb, vxOrb, vyOrb,
   c, s, pos, vel},
  a = RandomReal[{2.05, 3.75}];
  e = RandomReal[{0.0, 0.08}];
  mean = RandomReal[{0.0, 2 Pi}];
  peri = RandomReal[{0.0, 2 Pi}];
  ecc = FixedPoint[# - (# - e Sin[#] - mean)/(1 - e Cos[#]) &, mean, 8];
  f = 2 ArcTan[Sqrt[1 + e] Sin[ecc/2], Sqrt[1 - e] Cos[ecc/2]];
  p = a (1 - e^2);
  rr = p/(1 + e Cos[f]);
  root = Sqrt[g mSun/p];
  xOrb = rr Cos[f];
  yOrb = rr Sin[f];
  vxOrb = -root Sin[f];
  vyOrb = root (e + Cos[f]);
  c = Cos[peri];
  s = Sin[peri];
  pos = {c xOrb - s yOrb, s xOrb + c yOrb};
  vel = {c vxOrb - s vyOrb, s vxOrb + c vyOrb};
  <|"a0" -> a, "pos" -> pos, "vel" -> vel|>
];

runParticle[ic_] := Module[{x, y, status = "survived", sol},
  sol = Quiet@NDSolveValue[
     {
       x''[t] == acceleration[t, {x[t], y[t]}][[1]],
       y''[t] == acceleration[t, {x[t], y[t]}][[2]],
       x[0] == ic["pos"][[1]],
       y[0] == ic["pos"][[2]],
       x'[0] == ic["vel"][[1]],
       y'[0] == ic["vel"][[2]],
       WhenEvent[Norm[{x[t], y[t]}] > ejectionRadius,
         status = "ejected"; "StopIntegration"]
     },
     {x, y},
     {t, 0, tmax},
     MaxStepFraction -> 1/2000
   ];
  <|"a0" -> ic["a0"], "status" -> status|>
];

ensemble = Table[runParticle[sampleInitialCondition[]], {particles}];
ejected = Count[ensemble[[All, "status"]], "ejected"];
probability = N[ejected/particles];

Print["particles=", particles];
Print["tmax=", tmax];
Print["ejected=", ejected];
Print["ejection_probability=", probability];

ejectionHistogram = Histogram[
  Pick[ensemble[[All, "a0"]], ensemble[[All, "status"]], "ejected"],
  {2.05, 3.75, 0.1},
  AxesLabel -> {"initial semimajor axis", "ejected count"},
  PlotLabel -> "Ejected particles by initial semimajor axis"
];

Print[ejectionHistogram];
If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
Export["figures/asteroid_ejection_probability_mathematica.png", ejectionHistogram];
Print["wrote_plot=figures/asteroid_ejection_probability_mathematica.png"];
