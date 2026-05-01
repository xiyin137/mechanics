(* Standard-map invariant-curve breakdown companion demo.

   This script mirrors demos/python/standard_map_torus_breakdown.py. It follows
   an ensemble near the golden-mean unperturbed rotation number and leaves the
   momentum unwrapped so finite-time transport is visible.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/StandardMapTorusBreakdown.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/StandardMapTorusBreakdown.wl --plot

   Authors: GPT 5.5 and Xi Yin.
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

twoPi = 2 Pi;
goldenRotation = (Sqrt[5] - 1)/2;
goldenP = twoPi goldenRotation;
kick = 1.1;
orbitCount = 96;
stepCount = 900;
width = 10^-3;
seed = 20260501;

standardStep[{q_, p_}, k_] := Module[
  {pNext, qNext},
  pNext = p + k Sin[Mod[q, twoPi]];
  qNext = q + pNext;
  {qNext, pNext}
];

iterateOrbit[q0_, p0_, k_, steps_] := NestList[standardStep[#, k] &, {q0, p0}, steps];

SeedRandom[seed];
qInitial = RandomReal[{0, twoPi}, orbitCount];
pInitial = goldenP + RandomReal[{-width, width}, orbitCount];
trajectories = MapThread[iterateOrbit[#1, #2, kick, stepCount] &, {qInitial, pInitial}];

qMod = Mod[trajectories[[All, All, 1]], twoPi];
pValues = trajectories[[All, All, 2]];
pFinal = pValues[[All, -1]];
pSpanByTime = Table[
  Max[pValues[[All, n]]] - Min[pValues[[All, n]]],
  {n, 1, stepCount + 1}
];
pStdByTime = Table[StandardDeviation[pValues[[All, n]]], {n, 1, stepCount + 1}];
deltaP = pFinal - pInitial;

Print["Standard-map invariant-curve breakdown diagnostic"];
Print["This is a finite-time transport probe, not a proof of torus destruction."];
Print["K=", N[kick, 12]];
Print["orbits=", orbitCount];
Print["steps=", stepCount];
Print["seed=", seed];
Print["p_span_initial=", N[First[pSpanByTime], 12]];
Print["p_span_final=", N[Last[pSpanByTime], 12]];
Print["p_span_max=", N[Max[pSpanByTime], 12]];
Print["p_std_initial=", N[First[pStdByTime], 12]];
Print["p_std_final=", N[Last[pStdByTime], 12]];
Print["mean_abs_delta_p=", N[Mean[Abs[deltaP]], 12]];
Print["max_abs_delta_p=", N[Max[Abs[deltaP]], 12]];

If[makeFigures,
  stride = Max[1, Floor[(stepCount + 1)/300]];
  scatterData = Flatten[
    Table[
      Transpose[{qMod[[All, n]], pValues[[All, n]]}],
      {n, 1, stepCount + 1, stride}
    ],
    1
  ];
  phasePlot = ListPlot[
    scatterData,
    PlotStyle -> Directive[Blue, Opacity[0.45], PointSize[0.0018]],
    Frame -> True,
    FrameLabel -> {"q mod 2 pi", "unwrapped p"},
    PlotLabel -> "Standard-map ensemble near golden rotation"
  ];
  spreadPlot = ListLinePlot[
    {pSpanByTime, pStdByTime},
    DataRange -> {0, stepCount},
    Frame -> True,
    FrameLabel -> {"iteration", "momentum spread"},
    PlotLegends -> {"p span", "p standard deviation"},
    PlotLabel -> "Finite-time transport diagnostic"
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export[
    "figures/standard_map_torus_breakdown_mathematica.png",
    GraphicsGrid[{{phasePlot, spreadPlot}}]
  ];
  Print["wrote_plot=figures/standard_map_torus_breakdown_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/standard_map_torus_breakdown_mathematica.png"]
];
