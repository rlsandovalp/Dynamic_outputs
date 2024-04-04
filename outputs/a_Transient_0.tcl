\set tcl_precision 17

lappend   auto_path $env(PARFLOW_DIR)/bin
package   require parflow
namespace import Parflow::*

#-----------------------------------------------------------------------------
# File input version number
#-----------------------------------------------------------------------------
pfset     FileVersion    4

#-----------------------------------------------------------------------------
# Create solid
#-----------------------------------------------------------------------------
set Mask [pfload -sa "../../../Data/SA/enhanced_mask.sa"]
pfsetgrid {265 165 1} {0.0 0.0 0.0} {2000 2000 1} $Mask

set DMsk [pfload -sa "../../../Data/SA/Dummy_mask.sa"]
pfsetgrid {265 165 1} {0.0 0.0 0.0} {2000 2000 1} $DMsk

set DEM [pfload -sa "../../../Data/SA/DEM_35.sa"]
pfsetgrid {265 165 1} {0.0 0.0 0.0} {2000 2000 1} $DEM

set Top [pfcelldiff $DEM $DEM $DMsk]

set Top [pfcellsumconst $Top 225 $DMsk]
set Bottom [pfcellsumconst $Top -225 $DMsk]

pfpatchysolid -top $Top -bot $Bottom -msk $Mask -pfsol "My_solid.pfsol"

#-----------------------------------------------------------------------------
# Process the slopes
#-----------------------------------------------------------------------------
set slopes_in_x [pfload -sa "../../../Data/SA/SlopeX_35.sa"]
pfsetgrid {265 165 1} {0.0 0.0 0.0} {2000 2000 1} $slopes_in_x
pfsave $slopes_in_x -pfb "slope_x.pfb"

set slopes_in_y [pfload -sa "../../../Data/SA/SlopeY_35.sa"]
pfsetgrid {265 165 1} {0.0 0.0 0.0} {2000 2000 1} $slopes_in_y
pfsave $slopes_in_y -pfb "slope_y.pfb"

#-----------------------------------------------------------------------------
# Import Heterogeneous files
#-----------------------------------------------------------------------------
set mannings [pfload -sa "mannings.sa"]
pfsetgrid {265 165 1} {0.0 0.0 0.0} {2000 2000 1} $mannings
pfsave $mannings -pfb "mannings.pfb"

set keq [pfload -sa "k_eq.sa"]
pfsetgrid {265 165 9} {0.0 0.0 0.0} {2000 2000 25} $keq
pfsave $keq -pfb "k_eq.pfb"

set poreq [pfload -sa "porosity_eq.sa"]
pfsetgrid {265 165 9} {0.0 0.0 0.0} {2000 2000 25} $poreq
pfsave $poreq -pfb "porosity_eq.pfb"

set alphaeq [pfload -sa "alpha_eq.sa"]
pfsetgrid {265 165 9} {0.0 0.0 0.0} {2000 2000 25} $alphaeq
pfsave $alphaeq -pfb "alpha_eq.pfb"

set neq [pfload -sa "n_eq.sa"]
pfsetgrid {265 165 9} {0.0 0.0 0.0} {2000 2000 25} $neq
pfsave $neq -pfb "n_eq.pfb"

set sreseq [pfload -sa "sres_eq.sa"]
pfsetgrid {265 165 9} {0.0 0.0 0.0} {2000 2000 25} $sreseq
pfsave $sreseq -pfb "sres_eq.pfb"

set ssateq [pfload -sa "ssat_eq.sa"]
pfsetgrid {265 165 9} {0.0 0.0 0.0} {2000 2000 25} $ssateq
pfsave $ssateq -pfb "ssat_eq.pfb"

file copy -force "../../../Data/DAT/drv_vegm_2009.dat" "./drv_vegm.dat"
file copy -force "../../../Data/DAT/drv_vegp.dat" "./"
file copy -force "../../../Data/DAT/drv_clmin_first_time.dat" "./drv_clmin.dat"

#-----------------------------------------------------------------------------
# Set Processor topology 
#-----------------------------------------------------------------------------
pfset Process.Topology.P 8
pfset Process.Topology.Q 5
pfset Process.Topology.R 1

#-----------------------------------------------------------------------------
# Computational Grid
#-----------------------------------------------------------------------------
pfset ComputationalGrid.Lower.X           0.0
pfset ComputationalGrid.Lower.Y           0.0
pfset ComputationalGrid.Lower.Z           0.0

pfset ComputationalGrid.NX                265
pfset ComputationalGrid.NY                165
pfset ComputationalGrid.NZ                9

pfset ComputationalGrid.DX                2000.0
pfset ComputationalGrid.DY                2000.0
pfset ComputationalGrid.DZ                25.0

#-----------------------------------------------------------------------------
# Names of the GeomInputs
#-----------------------------------------------------------------------------
pfset GeomInput.Names                       "solidinput"

pfset GeomInput.solidinput.InputType  SolidFile
pfset GeomInput.solidinput.GeomNames  "domain"
pfset GeomInput.solidinput.FileName   "My_solid.pfsol"

pfset Geom.domain.Patches "Bottom Top west east"

#-----------------------------------------------------------------------------
# Domain
#-----------------------------------------------------------------------------
pfset Domain.GeomName                     domain

#--------------------------------------------
# variable dz assignments
#--------------------------------------------
pfset Solver.Nonlinear.VariableDz       True
pfset dzScale.GeomNames                 "domain"
pfset dzScale.Type                      nzList
pfset dzScale.nzListNumber              9

pfset Cell.0.dzScale.Value 5.0
pfset Cell.1.dzScale.Value 2.8
pfset Cell.2.dzScale.Value 0.8
pfset Cell.3.dzScale.Value 0.32
pfset Cell.4.dzScale.Value 0.04
pfset Cell.5.dzScale.Value 0.028
pfset Cell.6.dzScale.Value 0.006
pfset Cell.7.dzScale.Value 0.004
pfset Cell.8.dzScale.Value 0.002
#-----------------------------------------------------------------------------
# Hydraulic Conductivity (values in m/day)
#-----------------------------------------------------------------------------

pfset Geom.Perm.Names                      "domain"
pfset Geom.domain.Perm.Type              "PFBFile"
pfset Geom.domain.Perm.FileName          "k_eq.pfb"


# Isotropic
pfset Perm.TensorType               TensorByGeom
pfset Geom.Perm.TensorByGeom.Names  "domain"
pfset Geom.domain.Perm.TensorValX   10.0
pfset Geom.domain.Perm.TensorValY   10.0
pfset Geom.domain.Perm.TensorValZ   1.0

#-----------------------------------------------------------------------------
# Specific Storage
#-----------------------------------------------------------------------------
pfset SpecificStorage.Type                      Constant
pfset SpecificStorage.GeomNames                 "domain"
pfset Geom.domain.SpecificStorage.Value          0.00016

#-----------------------------------------------------------------------------
# Phases
#-----------------------------------------------------------------------------
pfset Phase.Names                         "water"
pfset Phase.water.Density.Type            Constant
pfset Phase.water.Density.Value           1.0
pfset Phase.water.Viscosity.Type          Constant
pfset Phase.water.Viscosity.Value         1.0

#-----------------------------------------------------------------------------
# Contaminants
#-----------------------------------------------------------------------------
pfset Contaminants.Names                  ""

#-----------------------------------------------------------------------------
# Gravity
#-----------------------------------------------------------------------------
pfset Gravity                             1.0

#-----------------------------------------------------------------------------
# Porosity
#-----------------------------------------------------------------------------
pfset Geom.Porosity.GeomNames               "domain"
pfset Geom.domain.Porosity.Type           "PFBFile"
pfset Geom.domain.Porosity.FileName       "porosity_eq.pfb"

#-----------------------------------------------------------------------------
# Relative Permeability
#-----------------------------------------------------------------------------
pfset Phase.RelPerm.Type                  VanGenuchten
pfset Phase.RelPerm.GeomNames             "domain"
pfset Phase.RelPerm.VanGenuchten.File            1
pfset Geom.domain.RelPerm.Alpha.Filename     "alpha_eq.pfb"
pfset Geom.domain.RelPerm.N.Filename         "n_eq.pfb"

#-----------------------------------------------------------------------------
# Saturation
#-----------------------------------------------------------------------------
pfset Phase.Saturation.Type               VanGenuchten
pfset Phase.Saturation.GeomNames          "domain"
pfset Phase.Saturation.VanGenuchten.File        1
pfset Geom.domain.Saturation.Alpha.Filename          "alpha_eq.pfb"
pfset Geom.domain.Saturation.N.Filename              "n_eq.pfb"
pfset Geom.domain.Saturation.SRes.Filename           "sres_eq.pfb"
pfset Geom.domain.Saturation.SSat.Filename           "ssat_eq.pfb"

#-----------------------------------------------------------------------------
# Topo slopes in x-direction
#-----------------------------------------------------------------------------
pfset TopoSlopesX.Type                                "PFBFile"
pfset TopoSlopesX.GeomNames                           "domain"
pfset TopoSlopesX.FileName                            "slope_x.pfb"

#-----------------------------------------------------------------------------
# Topo slopes in y-direction
#-----------------------------------------------------------------------------
pfset TopoSlopesY.Type                                "PFBFile"
pfset TopoSlopesY.GeomNames                           "domain"
pfset TopoSlopesY.FileName                            "slope_y.pfb"

#-----------------------------------------------------------------------------
# Mannings coefficient
#-----------------------------------------------------------------------------
pfset Mannings.Type                    "PFBFile"
pfset Mannings.GeomNames               "domain"
pfset Mannings.FileName                "mannings.pfb"

#-----------------------------------------------------------------------------
# Boundary Conditions
#-----------------------------------------------------------------------------
pfset BCPressure.PatchNames                   "Bottom Top west east"

pfset Patch.east.BCPressure.Type		                 DirEquilRefPatch
pfset Patch.east.BCPressure.Cycle		                "constant"
pfset Patch.east.BCPressure.RefGeom                      "domain"
pfset Patch.east.BCPressure.RefPatch                     Bottom
pfset Patch.east.BCPressure.alltime.Value	             219

pfset Patch.Top.BCPressure.Type		                    OverlandKinematic
pfset Patch.Top.BCPressure.Cycle		                "constant"
pfset Patch.Top.BCPressure.alltime.Value	             0.0

pfset Patch.west.BCPressure.Type		                 FluxConst
pfset Patch.west.BCPressure.Cycle		                "constant"
pfset Patch.west.BCPressure.alltime.Value	             0.0

pfset Patch.Bottom.BCPressure.Type		                 FluxConst
pfset Patch.Bottom.BCPressure.Cycle		                "constant"
pfset Patch.Bottom.BCPressure.alltime.Value	             0.0

##---------------------------------------------------------
# Initial conditions: water pressure
##---------------------------------------------------------


pfset ICPressure.Type                                   PFBFile
pfset ICPressure.GeomNames                              domain
pfset Geom.domain.ICPressure.FileName                   "./ip_solid.pfb"

#-----------------------------------------------------------------------------
# Timing [units in days]
#-----------------------------------------------------------------------------

pfset TimingInfo.BaseUnit                 1.0
pfset TimingInfo.StartCount               0.0
pfset TimingInfo.StartTime                0.0
pfset TimingInfo.StopTime                 8760.0
pfset TimingInfo.DumpInterval             876.0
pfset TimeStep.Type                       Constant
pfset TimeStep.Value                      1.0

#-----------------------------------------------------------------------------
# Time Cycles
#-----------------------------------------------------------------------------
pfset Cycle.Names                       "constant"

pfset Cycle.constant.Names              "alltime"
pfset Cycle.constant.alltime.Length      10000000
pfset Cycle.constant.Repeat             -1


#-----------------------------------------------------------------------------
# Phase sources:
#-----------------------------------------------------------------------------
pfset PhaseSources.water.Type                         "Constant"
pfset PhaseSources.water.GeomNames                    "domain"
pfset PhaseSources.water.Geom.domain.Value            0.0

#-----------------------------------------------------------------------------
# Exact solution specification for error calculations
#-----------------------------------------------------------------------------
pfset KnownSolution                                   NoKnownSolution

#-----------------------------------------------------------------------------
# Wells
#-----------------------------------------------------------------------------
pfset Wells.Names                         ""


#-----------------------------------------------------------------------------
# Set solver parameters
#-----------------------------------------------------------------------------
pfset Solver                                                Richards
pfset Solver.MaxIter                                        1000000

pfset Solver.TerrainFollowingGrid                           True

pfset Solver.Nonlinear.MaxIter                              800
pfset Solver.Nonlinear.ResidualTol                          1e-5

pfset Solver.Drop                                           1E-20
pfset Solver.AbsTol                                         1E-10

pfset Solver.Nonlinear.UseJacobian                          True
pfset Solver.Nonlinear.StepTol				                1e-25
pfset Solver.Nonlinear.Globalization                        LineSearch
pfset Solver.Linear.KrylovDimension                         15
pfset Solver.Linear.MaxRestarts                             10
pfset Solver.MaxConvergenceFailures                         10

pfset Solver.Linear.Preconditioner                          PFMG
pfset Solver.PrintSubsurf                                   True
pfset Solver.PrintSaturation                                True


## --------------------------------------------------------
# CLM settings
## --------------------------------------------------------
pfset Solver.LSM                                         CLM
pfset Solver.CLM.MetForcing                              3D
pfset Solver.CLM.MetFileName                             "FORCING_lombardy"
pfset Solver.CLM.MetFilePath                             "forcings/"
pfset Solver.CLM.MetFileNT                               24
pfset Solver.CLM.CLMDumpInterval                         876


pfset Solver.PrintCLM                                    True
pfset Solver.CLM.SingleFile                              True
pfset Solver.WriteCLMBinary                              False
pfset Solver.CLM.BinaryOutDir                            False
pfset Solver.CLM.WriteLogs                               False
pfset Solver.CLM.WriteLastRST                            True
pfset Solver.CLM.RootZoneNZ                              5
pfset Solver.CLM.SoiLayer                                5


#-----------------------------------------------------------------------------
# Print Outputs
#-----------------------------------------------------------------------------
pfset Solver.PrintSlopes                            True
pfset Solver.PrintMannings                          True

#-----------------------------------------------------------------------------
# Distribute inputs
#-----------------------------------------------------------------------------
pfdist -nz 1 "slope_x.pfb"
pfdist -nz 1 "slope_y.pfb"
pfdist -nz 9 "ip_solid.pfb"
pfdist -nz 9 "k_eq.pfb"
pfdist -nz 9 "porosity_eq.pfb"
pfdist -nz 9 "alpha_eq.pfb"
pfdist -nz 9 "n_eq.pfb"
pfdist -nz 9 "sres_eq.pfb"
pfdist -nz 9 "ssat_eq.pfb"
pfdist -nz 1 "mannings.pfb"

#-----------------------------------------------------------------------------
# Run Simulation 
#-----------------------------------------------------------------------------
set runname "Dynamic_Spinup"
puts "ParFlow run Started"
pfrun    $runname
puts "ParFlow run Complete"

#-----------------------------------------------------------------------------
# Undistribute outputs
#-----------------------------------------------------------------------------
pfundist $runname
pfundist "slope_x.pfb"
pfundist "slope_y.pfb"
pfundist "ip_solid.pfb"
pfundist "k_eq.pfb"
pfundist "porosity_eq.pfb"
pfundist "alpha_eq.pfb"
pfundist "n_eq.pfb"
pfundist "sres_eq.pfb"
pfundist "ssat_eq.pfb"
pfundist "mannings.pfb"
