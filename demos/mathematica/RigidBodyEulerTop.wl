(* Euler top companion demo.

   Authors: GPT 5.5 and Xi Yin.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/RigidBodyEulerTop.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/RigidBodyEulerTop.wl --plot

   The script integrates Euler's equations for a free rigid body and reports
   invariant drift. It is designed to be pasted into a Mathematica notebook as
   well.

   Unlike the Python demo, this uses Mathematica's adaptive NDSolveValue
   integrator; long-time drift behavior depends on the selected tolerances.
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

inertia = {1.0, 2.0, 3.0};
omega0 = {0.05, 1.0, 0.05};
tmax = 50.0;

rhs[{w1_, w2_, w3_}] := {
  ((inertia[[2]] - inertia[[3]])/inertia[[1]]) w2 w3,
  ((inertia[[3]] - inertia[[1]])/inertia[[2]]) w3 w1,
  ((inertia[[1]] - inertia[[2]])/inertia[[3]]) w1 w2
};

sol = NDSolveValue[
  {
    w1'[t] == rhs[{w1[t], w2[t], w3[t]}][[1]],
    w2'[t] == rhs[{w1[t], w2[t], w3[t]}][[2]],
    w3'[t] == rhs[{w1[t], w2[t], w3[t]}][[3]],
    w1[0] == omega0[[1]],
    w2[0] == omega0[[2]],
    w3[0] == omega0[[3]]
  },
  {w1, w2, w3},
  {t, 0, tmax}
];

omegaAt[time_] := Through[sol[time]];

energy[w_] := 1/2 Total[inertia w^2];
momentumSquared[w_] := Total[(inertia w)^2];

initialEnergy = energy[omega0];
finalEnergy = energy[omegaAt[tmax]];
initialMomentumSquared = momentumSquared[omega0];
finalMomentumSquared = momentumSquared[omegaAt[tmax]];

Print["energy_initial=", N[initialEnergy, 16]];
Print["energy_final=", N[finalEnergy, 16]];
Print["energy_drift=", N[finalEnergy - initialEnergy, 16]];
Print["momentum_sq_initial=", N[initialMomentumSquared, 16]];
Print["momentum_sq_final=", N[finalMomentumSquared, 16]];
Print["momentum_sq_drift=", N[finalMomentumSquared - initialMomentumSquared, 16]];

If[makeFigures,
  omegaPlot = Plot[
    Evaluate[omegaAt[t]],
    {t, 0, tmax},
    PlotLegends -> {"omega1", "omega2", "omega3"},
    AxesLabel -> {"t", "body angular velocity"},
    PlotLabel -> "Euler top"
  ];
  driftPlot = Plot[
    {
      energy[omegaAt[t]] - initialEnergy,
      momentumSquared[omegaAt[t]] - initialMomentumSquared
    },
    {t, 0, tmax},
    PlotLegends -> {"energy drift", "momentum squared drift"},
    AxesLabel -> {"t", "drift"},
    PlotLabel -> "Invariant drift"
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export["figures/rigid_body_euler_top_mathematica.png", GraphicsGrid[{{omegaPlot}, {driftPlot}}]];
  Print["wrote_plot=figures/rigid_body_euler_top_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/rigid_body_euler_top_mathematica.png"]
];
