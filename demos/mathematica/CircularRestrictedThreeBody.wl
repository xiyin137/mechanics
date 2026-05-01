(* Circular restricted three-body problem companion demo.

   Units: total primary mass = 1, primary separation = 1, angular velocity = 1.
   The smaller primary has mass fraction mu.

   Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/CircularRestrictedThreeBody.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/CircularRestrictedThreeBody.wl --plot
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

mu = 9.543*10^-4/(1 + 9.543*10^-4);

r1[x_, y_] := Sqrt[(x + mu)^2 + y^2];
r2[x_, y_] := Sqrt[(x - 1 + mu)^2 + y^2];
omegaEff[x_, y_] := 1/2 (x^2 + y^2) + (1 - mu)/r1[x, y] + mu/r2[x, y];

eqx[x_, y_] := D[omegaEff[xx, yy], xx] /. {xx -> x, yy -> y};
eqy[x_, y_] := D[omegaEff[xx, yy], yy] /. {xx -> x, yy -> y};

l1 = x /. FindRoot[eqx[x, 0] == 0, {x, 0.93}];
l2 = x /. FindRoot[eqx[x, 0] == 0, {x, 1.07}];
l3 = x /. FindRoot[eqx[x, 0] == 0, {x, -1.0}];
l4 = {1/2 - mu, Sqrt[3]/2};
l5 = {1/2 - mu, -Sqrt[3]/2};

Print["mu=", N[mu, 12]];
Print["L1=", N[{l1, 0}, 12]];
Print["L2=", N[{l2, 0}, 12]];
Print["L3=", N[{l3, 0}, 12]];
Print["L4=", N[l4, 12]];
Print["L5=", N[l5, 12]];

eqns = {
   x''[t] - 2 y'[t] == eqx[x[t], y[t]],
   y''[t] + 2 x'[t] == eqy[x[t], y[t]],
   x[0] == l4[[1]] + 0.02,
   y[0] == l4[[2]],
   x'[0] == 0,
   y'[0] == 0
};

tmax = 6 Pi;
sol = NDSolveValue[eqns, {x, y, x', y'}, {t, 0, tmax},
   MaxStepFraction -> 1/2000
];

jacobi[t_] := 2 omegaEff[sol[[1]][t], sol[[2]][t]] -
   sol[[3]][t]^2 - sol[[4]][t]^2;

samples = Subdivide[0, tmax, 400];
drift = Max[Abs[jacobi /@ samples - jacobi[0]]];

Print["jacobi_initial=", N[jacobi[0], 12]];
Print["jacobi_max_abs_drift=", ScientificForm[drift, 4]];

If[makeFigures,
  trajPlot = ParametricPlot[
     Evaluate[{sol[[1]][t], sol[[2]][t]}],
     {t, 0, tmax},
     PlotRange -> {{-1.5, 1.5}, {-1.2, 1.2}},
     AspectRatio -> Automatic,
     Frame -> True,
     FrameLabel -> {"rotating-frame x", "rotating-frame y"},
     PlotLabel -> "CR3BP trajectory near L4"
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export["figures/cr3bp_mathematica.png", trajPlot];
  Print["wrote_plot=figures/cr3bp_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/cr3bp_mathematica.png"]
];
