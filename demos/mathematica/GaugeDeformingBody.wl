(* Gauge-theory toy model for deforming bodies.

   Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

   The first part reconstructs a planar Cosserat rod from a curvature
   connection kappa(s). The second part shows an Abelian SO(2)-like connection
   field and its curvature dA. The third part matches the Python
   two-rotor deforming-body demo by computing the nonabelian holonomy of a
   closed rectangular stroke in shape space.

   Run with:
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/GaugeDeformingBody.wl
     /Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/GaugeDeformingBody.wl --plot
*)

ClearAll["Global`*"];

makeFigures = MemberQ[$ScriptCommandLine, "--plot"];

length = 8.0;
kappa[s_] := 0.18 + 0.55 Sin[4 Pi s/length];
theta[s_] := 0.18 s + 0.55 length (1 - Cos[4 Pi s/length])/(4 Pi);
xCoord[s_?NumericQ] := NIntegrate[Cos[theta[u]], {u, 0, s}];
yCoord[s_?NumericQ] := NIntegrate[Sin[theta[u]], {u, 0, s}];

Print["frame_holonomy=", N[theta[length], 16]];

(* Abelian local frame connection in two material coordinates. *)
ax[x_, y_] := -y/(1 + x^2 + y^2);
ay[x_, y_] := x/(1 + x^2 + y^2);
fieldStrength[x_, y_] := D[ay[xx, yy], xx] - D[ax[xx, yy], yy] /. {xx -> x, yy -> y};

(* Two-rotor Shapere-Wilczek holonomy model. *)
hat[v_] := {
  {0, -v[[3]], v[[2]]},
  {v[[3]], 0, -v[[1]]},
  {-v[[2]], v[[1]], 0}
};
vee[m_] := {m[[3, 2]], m[[1, 3]], m[[2, 1]]};

i0 = 4.0;
i1 = 1.0;
i2 = 1.5;
deltaAlpha = 0.45;
deltaBeta = 0.35;

ex = {1, 0, 0};
ey = {0, 1, 0};
ez = {0, 0, 1};
aAlpha = (i1/(i0 + i1)) ez;
aBeta = (i2/(i0 + i2)) ey;
curvature = Cross[aAlpha, aBeta];

segments = {
  -aAlpha deltaAlpha,
  -aBeta deltaBeta,
  aAlpha deltaAlpha,
  aBeta deltaBeta
};
rotation = Fold[#1.MatrixExp[hat[#2]] &, IdentityMatrix[3], segments];
angle = ArcCos[Clip[(Tr[rotation] - 1)/2, {-1, 1}]];
skew = (rotation - Transpose[rotation])/2;
rotvec = If[angle < 10^-8, vee[skew], angle/Sin[angle] vee[skew]];
leadingRotvec = curvature deltaAlpha deltaBeta;

Print["A_alpha=", N[aAlpha, 12]];
Print["A_beta=", N[aBeta, 12]];
Print["curvature_vector=", N[curvature, 12]];
Print["leading_rotation_vector=", N[leadingRotvec, 12]];
Print["net_rotation_vector=", N[rotvec, 12]];
Print["orthogonality_error=", ScientificForm[Norm[Transpose[rotation].rotation - IdentityMatrix[3]], 4]];
Print["determinant_error=", ScientificForm[Abs[Det[rotation] - 1], 4]];

If[makeFigures,
  rod = ParametricPlot[
    {xCoord[s], yCoord[s]},
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
  strokePlot = ListLinePlot[
    {{0, 0}, {deltaAlpha, 0}, {deltaAlpha, deltaBeta}, {0, deltaBeta}, {0, 0}},
    Frame -> True,
    AspectRatio -> Automatic,
    PlotMarkers -> Automatic,
    FrameLabel -> {"alpha", "beta"},
    PlotLabel -> "Closed two-rotor shape stroke"
  ];
  rotBar = BarChart[
    rotvec,
    ChartLabels -> {"x", "y", "z"},
    Frame -> True,
    PlotLabel -> "Net body rotation vector"
  ];
  If[!DirectoryQ["figures"], CreateDirectory["figures", CreateIntermediateDirectories -> True]];
  Export["figures/gauge_deforming_body_mathematica.png",
    GraphicsGrid[{{rod, curvaturePlot}, {connectionPlot, curvatureDensityPlot}, {strokePlot, rotBar}}]
  ];
  Print["wrote_plot=figures/gauge_deforming_body_mathematica.png"],
  Print["plot_skipped=pass --plot to write figures/gauge_deforming_body_mathematica.png"]
];
