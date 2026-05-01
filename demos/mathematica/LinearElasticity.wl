(* Linear elasticity companion demo.

   This script mirrors demos/python/linear_elasticity.py with closed-form
   formulas for isotropic moduli, wave speeds, axial bars, circular-shaft
   torsion, Euler-Bernoulli beams, and longitudinal bar modes.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/LinearElasticity.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/LinearElasticity.wl --plot

   Authors: GPT 5.5 and Xi Yin.
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

youngMod = 20.0;
poissonRatio = 0.30;
density = 1.0;
length = 1.0;
area = 0.4;
areaMoment = 2.0*10^-2;
radius = 0.12;
force = 1.0;
torque = 0.008;
load = 1.0;

lameFromYoungPoisson[young_, poisson_] := {
  young poisson/((1 + poisson) (1 - 2 poisson)),
  young/(2 (1 + poisson))
};

youngPoissonFromLame[lambda_, mu_] := {
  mu (3 lambda + 2 mu)/(lambda + mu),
  lambda/(2 (lambda + mu))
};

bulkModulus[lambda_, mu_] := lambda + 2 mu/3;
waveSpeeds[lambda_, mu_, rho_] := {Sqrt[(lambda + 2 mu)/rho], Sqrt[mu/rho]};
axialBarElongation[force_, length_, area_, young_] := force length/(young area);
circularPolarMoment[radius_] := Pi radius^4/2;
torsionTwist[torque_, length_, mu_, polarMoment_] := torque length/(mu polarMoment);
torsionShearStress[r_, torque_, polarMoment_] := torque r/polarMoment;
cantileverEndLoad[x_, length_, young_, areaMoment_, endForce_] :=
  endForce x^2 (3 length - x)/(6 young areaMoment);
simplySupportedUniform[x_, length_, young_, areaMoment_, q_] :=
  q x (length^3 - 2 length x^2 + x^3)/(24 young areaMoment);
barFrequency[n_, length_, young_, rho_] := n Pi Sqrt[young/rho]/length;

{lambda, muShear} = lameFromYoungPoisson[youngMod, poissonRatio];
{recoveredYoung, recoveredPoisson} = youngPoissonFromLame[lambda, muShear];
bulk = bulkModulus[lambda, muShear];
{pWaveSpeed, sWaveSpeed} = waveSpeeds[lambda, muShear, density];
polarMoment = circularPolarMoment[radius];
frequencies = Table[barFrequency[n, length, youngMod, density], {n, 1, 3}];

Print["Linear elasticity diagnostics"];
Print["young=", N[youngMod, 12]];
Print["poisson=", N[poissonRatio, 12]];
Print["lambda=", N[lambda, 12]];
Print["mu=", N[muShear, 12]];
Print["bulk_modulus=", N[bulk, 12]];
Print["recovered_young=", N[recoveredYoung, 12]];
Print["recovered_poisson=", N[recoveredPoisson, 12]];
Print["p_wave_speed=", N[pWaveSpeed, 12]];
Print["s_wave_speed=", N[sWaveSpeed, 12]];
Print["bar_frequencies=", N[frequencies, 12]];
Print["axial_bar_elongation=", N[axialBarElongation[force, length, area, youngMod], 12]];
Print["circular_polar_moment=", N[polarMoment, 12]];
Print["torsion_twist=", N[torsionTwist[torque, length, muShear, polarMoment], 12]];
Print["cantilever_tip_deflection=",
  N[cantileverEndLoad[length, length, youngMod, areaMoment, force], 12]
];

If[makeFigures,
  modePlot = Plot[
    Evaluate[Table[Sin[n Pi x/length], {n, 1, 3}]],
    {x, 0, length},
    Frame -> True,
    FrameLabel -> {"x/L", "normalized displacement"},
    PlotLegends -> {"mode 1", "mode 2", "mode 3"},
    PlotLabel -> "Fixed-fixed bar modes"
  ];
  beamPlot = Plot[
    Evaluate[{
      cantileverEndLoad[x, length, youngMod, areaMoment, force],
      simplySupportedUniform[x, length, youngMod, areaMoment, load]
    }],
    {x, 0, length},
    Frame -> True,
    FrameLabel -> {"x/L", "deflection"},
    PlotLegends -> {"cantilever end load", "simply supported uniform load"},
    PlotLabel -> "Euler-Bernoulli deflection formulas"
  ];
  torsionPlot = Plot[
    torsionShearStress[r, torque, polarMoment],
    {r, 0, radius},
    Frame -> True,
    FrameLabel -> {"r", "tau"},
    PlotLabel -> "Circular-shaft torsion stress"
  ];
  moduliPlot = Plot[
    Evaluate[{
      bulkModulus @@ lameFromYoungPoisson[youngMod, nu],
      Last[lameFromYoungPoisson[youngMod, nu]]
    }],
    {nu, -0.2, 0.49},
    PlotRange -> All,
    Frame -> True,
    FrameLabel -> {"Poisson ratio", "modulus"},
    PlotLegends -> {"bulk modulus", "shear modulus"},
    PlotLabel -> "Approach to incompressibility"
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export[
    "figures/linear_elasticity_mathematica.png",
    GraphicsGrid[{{modePlot, beamPlot}, {torsionPlot, moduliPlot}}]
  ];
  Print["wrote_plot=figures/linear_elasticity_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/linear_elasticity_mathematica.png"]
];
