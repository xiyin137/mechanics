(* Jovian resonance normal-form companion demo.

   Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

   This script mirrors demos/python/asteroid_resonance_normal_form.py. It
   computes nominal interior resonance locations, the illustrative pendulum
   half-width scaling Delta J = 2 Sqrt[epsilon eta e^r/Abs[A]], and the actual
   first-order 2:1 disturbing-function coefficient in the planar circular
   restricted model.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/AsteroidResonanceNormalForm.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/AsteroidResonanceNormalForm.wl --plot
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

aJupiter = 5.2044;
epsilon = 9.543*10^-4;
eta = 1.0;
curvature = 1.0;
resonances = <|"3:1" -> {3, 1}, "5:2" -> {5, 2}, "7:3" -> {7, 3}, "2:1" -> {2, 1}|>;

location[{p_, q_}] := aJupiter (q/p)^(2/3);
order[{p_, q_}] := p - q;
halfWidth[e_, {p_, q_}] := 2 Sqrt[epsilon eta e^(p - q)/Abs[curvature]];
csvNumber[x_] := ToString[NumberForm[N[x], {Infinity, 6}], OutputForm];

alpha21 = (1/2)^(2/3);
qDen[psi_] := 1 - 2 alpha21 Cos[psi] + alpha21^2;
dDirectRho[psi_] := (alpha21 Cos[psi] - alpha21^2)/qDen[psi]^(3/2);
dDirectPsi[psi_] := -alpha21 Sin[psi]/qDen[psi]^(3/2);
dRRho[psi_] := dDirectRho[psi] - alpha21 Cos[psi];
dRPsi[psi_] := dDirectPsi[psi] + alpha21 Sin[psi];
coefficient21 = N[
  NIntegrate[
    -Cos[2 psi] dRRho[psi] + 2 Sin[2 psi] dRPsi[psi],
    {psi, 0, 2 Pi},
    WorkingPrecision -> 30,
    AccuracyGoal -> 18,
    PrecisionGoal -> 18
  ]/(2 Pi),
  15
];
halfWidth21[e_] := 4 aJupiter Sqrt[epsilon Abs[coefficient21] e alpha21^3/3];

Print["resonance,p,q,order,a_au"];
KeyValueMap[
  Function[{label, ratio},
    Print[
      label, ",", ratio[[1]], ",", ratio[[2]], ",", order[ratio], ",",
      csvNumber[location[ratio]]
    ]
  ],
  resonances
];

Print["width_scaling_note=B_r(e)=eta e^r is illustrative unless eta comes from a disturbing-function calculation"];
Print["epsilon=", N[epsilon, 12]];
Print["eta=", eta];
Print["curvature=", curvature];
Print["coefficient_2to1_units_gmj_over_aj=", N[coefficient21, 12]];
Print["half_width_2to1_au_at_e_0p1=", N[halfWidth21[0.1], 12]];

If[makeFigures,
  eccGrid = Range[0.02, 0.30, 0.02];
  widthCurves = KeyValueMap[
    Function[{label, ratio},
      Transpose[{eccGrid, halfWidth[#, ratio] & /@ eccGrid}]
    ],
    resonances
  ];
  widthPlot = ListLinePlot[
    Append[Values[widthCurves], Transpose[{eccGrid, halfWidth21 /@ eccGrid}]],
    PlotLegends -> Append[Keys[resonances], "2:1 actual [AU]"],
    Frame -> True,
    FrameLabel -> {"eccentricity", "half-width: model units or AU"},
    PlotLabel -> "Illustrative resonant width scaling"
  ];
  locationPlot = ListPlot[
    KeyValueMap[{location[#2], 0} &, resonances],
    PlotMarkers -> Automatic,
    Frame -> True,
    FrameLabel -> {"semimajor axis [AU]", ""},
    PlotLabel -> "Nominal interior Jovian resonances",
    Epilog -> KeyValueMap[
      Text[Style[#1, 11], {location[#2], 0.08}, {0, 0}] &,
      resonances
    ]
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export[
    "figures/asteroid_resonance_normal_form_mathematica.png",
    GraphicsGrid[{{locationPlot, widthPlot}}]
  ];
  Print["wrote_plot=figures/asteroid_resonance_normal_form_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/asteroid_resonance_normal_form_mathematica.png"]
];
