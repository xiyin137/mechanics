(* Gauge-theory toy model for deforming bodies.

   Authors: GPT 5.5 and Xi Yin.

   The first part reconstructs a planar Cosserat rod from a curvature
   connection kappa(s). The second part shows an Abelian SO(2)-like connection
   field and its curvature dA.

   Run with:
     wolframscript -file demos/mathematica/GaugeDeformingBody.wl
*)

ClearAll["Global`*"];

length = 8.0;
kappa[s_] := 0.18 + 0.55 Sin[4 Pi s/length];
theta[s_] := NIntegrate[kappa[u], {u, 0, s}];
x[s_] := NIntegrate[Cos[theta[u]], {u, 0, s}];
y[s_] := NIntegrate[Sin[theta[u]], {u, 0, s}];

rod = ParametricPlot[
  {x[s], y[s]},
  {s, 0, length},
  AspectRatio -> Automatic,
  AxesLabel -> {"x", "y"},
  PlotLabel -> "Planar Cosserat rod reconstructed from kappa(s)"
];

curvaturePlot = Plot[
  kappa[s],
  {s, 0, length},
  AxesLabel -> {"s", "kappa(s)"},
  PlotLabel -> "Connection component along the rod"
];

Print["frame_holonomy=", N[theta[length], 16]];
Print[rod];
Print[curvaturePlot];

(* Abelian local frame connection in two material coordinates. *)
ax[x_, y_] := -y/(1 + x^2 + y^2);
ay[x_, y_] := x/(1 + x^2 + y^2);
fieldStrength[x_, y_] := D[ay[xx, yy], xx] - D[ax[xx, yy], yy] /. {xx -> x, yy -> y};

connectionPlot = VectorPlot[
  {ax[x, y], ay[x, y]},
  {x, -2, 2},
  {y, -2, 2},
  PlotLabel -> "Local frame connection A",
  VectorPoints -> 17
];

curvatureDensityPlot = Plot3D[
  fieldStrength[x, y],
  {x, -2, 2},
  {y, -2, 2},
  AxesLabel -> {"x", "y", "Fxy"},
  PlotLabel -> "Curvature dA"
];

Print[connectionPlot];
Print[curvatureDensityPlot];

If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
Export["figures/gauge_deforming_body_mathematica.png",
  GraphicsGrid[{{rod, curvaturePlot}, {connectionPlot, curvatureDensityPlot}}]
];
Print["wrote_plot=figures/gauge_deforming_body_mathematica.png"];
