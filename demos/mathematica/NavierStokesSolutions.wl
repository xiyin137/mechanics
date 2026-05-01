(* Exact and reduced Navier-Stokes solutions companion demo.

   This script mirrors demos/python/navier_stokes_solutions.py with
   Couette-Poiseuille flow, Hagen-Poiseuille pipe flow, Stokes' first problem,
   the oscillatory Stokes layer, and the Taylor-Green vortex.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/NavierStokesSolutions.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/NavierStokesSolutions.wl --plot

   Authors: GPT 5.5 and Xi Yin.
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

h = 1.0;
muVisc = 1.0;
nuVisc = 0.08;
pipeRadius = 1.0;
pressureForcing = 1.0;
lowerSpeed = 0.0;
upperSpeed = 1.0;
wallSpeed = 1.0;
angularFrequency = 2.0;
rho = 1.0;

couettePoiseuille[y_, h_, mu_, g_, u0_, u1_] :=
  u0 + (u1 - u0) y/h + g y (h - y)/(2 mu);

couettePoiseuilleFlux[h_, mu_, g_, u0_, u1_] :=
  h (u0 + u1)/2 + g h^3/(12 mu);

pipePoiseuille[r_, radius_, mu_, g_] := g (radius^2 - r^2)/(4 mu);
pipePoiseuilleFlux[radius_, mu_, g_] := Pi radius^4 g/(8 mu);

stokesFirst[y_, t_, u_, nu_] := u Erfc[y/(2 Sqrt[nu t])];

oscillatoryStokes[y_, t_, u_, omega_, nu_] := Module[
  {delta = Sqrt[2 nu/omega]},
  u Exp[-y/delta] Cos[omega t - y/delta]
];

taylorGreenAmplitude[t_, nu_, k_, speed_] := speed Exp[-2 nu k^2 t];
taylorGreenVelocity[x_, y_, t_, nu_, k_, speed_] := Module[
  {a = taylorGreenAmplitude[t, nu, k, speed]},
  {a Sin[k x] Cos[k y], -a Cos[k x] Sin[k y]}
];
taylorGreenPressure[x_, y_, t_, nu_, k_, speed_, rho_] := Module[
  {a = taylorGreenAmplitude[t, nu, k, speed]},
  rho a^2 (Cos[2 k x] + Cos[2 k y])/4
];
taylorGreenEnergyDensity[t_, nu_, k_, speed_, rho_] :=
  rho taylorGreenAmplitude[t, nu, k, speed]^2/4;

Print["Navier-Stokes exact-solution diagnostics"];
Print["couette_poiseuille_flux=",
  N[couettePoiseuilleFlux[h, muVisc, pressureForcing, lowerSpeed, upperSpeed], 12]
];
Print["pipe_poiseuille_flux=", N[pipePoiseuilleFlux[pipeRadius, muVisc, pressureForcing], 12]];
Print["stokes_first_wall_value=", N[stokesFirst[0, 0.5, wallSpeed, nuVisc], 12]];
Print["oscillatory_layer_wall_value=",
  N[oscillatoryStokes[0, 0.5, wallSpeed, angularFrequency, nuVisc], 12]
];
Print["taylor_green_energy_density=",
  N[taylorGreenEnergyDensity[0.4, nuVisc, 1.0, 1.0, rho], 12]
];

If[makeFigures,
  profilePlot = Plot[
    Evaluate[{
      couettePoiseuille[y, h, muVisc, 0.0, lowerSpeed, upperSpeed],
      couettePoiseuille[y, h, muVisc, pressureForcing, 0.0, 0.0],
      pipePoiseuille[y, pipeRadius, muVisc, pressureForcing]
    }],
    {y, 0, 1},
    Frame -> True,
    FrameLabel -> {"wall-normal coordinate", "speed"},
    PlotLegends -> {"Couette", "plane Poiseuille", "pipe Poiseuille"},
    PlotLabel -> "Steady laminar profiles"
  ];
  unsteadyPlot = Plot[
    Evaluate[{
      stokesFirst[y, 0.08, wallSpeed, nuVisc],
      stokesFirst[y, 0.35, wallSpeed, nuVisc],
      oscillatoryStokes[y, 0.5, wallSpeed, angularFrequency, nuVisc]
    }],
    {y, 0, 1.5},
    Frame -> True,
    FrameLabel -> {"y", "u(y,t)"},
    PlotLegends -> {"Stokes t=0.08", "Stokes t=0.35", "oscillatory layer"},
    PlotLabel -> "Unsteady viscous penetration"
  ];
  taylorVectorPlot = VectorPlot[
    Evaluate[taylorGreenVelocity[x, y, 0.3, nuVisc, 1.0, 1.0]],
    {x, 0, 2 Pi},
    {y, 0, 2 Pi},
    VectorPoints -> 17,
    Frame -> True,
    PlotLabel -> "Taylor-Green velocity field"
  ];
  taylorPressurePlot = Plot3D[
    taylorGreenPressure[x, y, 0.3, nuVisc, 1.0, 1.0, rho],
    {x, 0, 2 Pi},
    {y, 0, 2 Pi},
    AxesLabel -> {"x", "y", "p"},
    PlotLabel -> "Taylor-Green pressure"
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export[
    "figures/navier_stokes_solutions_mathematica.png",
    GraphicsGrid[{{profilePlot, unsteadyPlot}, {taylorVectorPlot, taylorPressurePlot}}]
  ];
  Print["wrote_plot=figures/navier_stokes_solutions_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/navier_stokes_solutions_mathematica.png"]
];
