(* Euler top companion demo.

   Authors: GPT 5.5 and Xi Yin.

   Run with:
     wolframscript -file demos/mathematica/RigidBodyEulerTop.wl

   The script integrates Euler's equations for a free rigid body and reports
   invariant drift. It is designed to be pasted into a Mathematica notebook as
   well.

   Unlike the Python demo, this uses Mathematica's adaptive NDSolveValue
   integrator; long-time drift behavior depends on the selected tolerances.
*)

ClearAll["Global`*"];

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
    omega'[t] == rhs[omega[t]],
    omega[0] == omega0
  },
  omega,
  {t, 0, tmax}
];

energy[w_] := 1/2 Total[inertia w^2];
momentumSquared[w_] := Total[(inertia w)^2];

initialEnergy = energy[omega0];
finalEnergy = energy[sol[tmax]];
initialMomentumSquared = momentumSquared[omega0];
finalMomentumSquared = momentumSquared[sol[tmax]];

Print["energy_initial=", N[initialEnergy, 16]];
Print["energy_final=", N[finalEnergy, 16]];
Print["energy_drift=", N[finalEnergy - initialEnergy, 16]];
Print["momentum_sq_initial=", N[initialMomentumSquared, 16]];
Print["momentum_sq_final=", N[finalMomentumSquared, 16]];
Print["momentum_sq_drift=", N[finalMomentumSquared - initialMomentumSquared, 16]];

omegaPlot = Plot[
  Evaluate[sol[t]],
  {t, 0, tmax},
  PlotLegends -> {"omega1", "omega2", "omega3"},
  AxesLabel -> {"t", "body angular velocity"},
  PlotLabel -> "Euler top"
];

driftPlot = Plot[
  {
    energy[sol[t]] - initialEnergy,
    momentumSquared[sol[t]] - initialMomentumSquared
  },
  {t, 0, tmax},
  PlotLegends -> {"energy drift", "momentum squared drift"},
  AxesLabel -> {"t", "drift"},
  PlotLabel -> "Invariant drift"
];

Print[omegaPlot];
Print[driftPlot];

If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
Export["figures/rigid_body_euler_top_mathematica.png", GraphicsGrid[{{omegaPlot}, {driftPlot}}]];
Print["wrote_plot=figures/rigid_body_euler_top_mathematica.png"];
