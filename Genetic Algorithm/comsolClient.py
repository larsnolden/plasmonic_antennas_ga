import mph
from jpype import JBoolean, JClass, JArray, JString
import time


def printElapsedTime(startTime, index):
    elapsedTime = time.time() - startTime
    minutes = int(elapsedTime // 60)
    seconds = int(elapsedTime % 60)
    print(f"Until {index}: {minutes} minutes {seconds} seconds")


def runSimulation(
    outer_contour_file_path,
    inner_contour_file_path=None,
    mesh_resolution="normal",
    model_path=None,
):
    # Pre
    print(f"running simulation")
    print(f"mesh_resolution: {mesh_resolution}")
    startTime = time.time()

    client = mph.start()
    # server = mph.Server(cores=1)

    # create the model.java
    model = client.create("Model")

    model.java.modelPath("./")

    # show Jpype the intention of using an integer with Integer()
    # this has to run after the model is created
    Integer = JClass("java.lang.Integer")

    model.java.label("silver_plasmonic_nano_antenna.mph")

    model.java.title("Silver Plasmonic Nano Antenna")

    # Main
    model.java.param().set("w", "750[nm]", "Width of physical geometry")
    model.java.param().set("w", "750[nm]", "Width of physical geometry")
    model.java.param().set("t_pml", "150[nm]", "PML thickness")
    model.java.param().set("h_air", "400[nm]", "Air domain height")
    model.java.param().set("h_subs", "250[nm]", "Substrate domain height")
    model.java.param().set("na", "1", "Refractive index, air")
    model.java.param().set("nb", "1.5", "Refractive index, substrate")
    model.java.param().set("lda0", "532[nm]", "Wavelength")
    model.java.param().set("phi", "0", "Azimuthal angle of incidence in both media")
    model.java.param().set("theta", "0", "Polar angle of incidence in air")
    model.java.param().set(
        "thetab", "asin(na/nb*sin(theta))", "Polar angle in substrate"
    )
    model.java.param().set("I0", "1[W/m^2]", "Intensity of incident field")
    model.java.param().set("P", "I0*w^2*cos(theta)", "Port power")

    model.java.component().create("comp1", JBoolean(True))

    model.java.component("comp1").geom().create("geom1", 3)

    model.java.result().table().create("tbl1", "Table")
    model.java.result().table().create("tbl2", "Table")

    model.java.component("comp1").mesh().create("mesh1")

    model.java.component("comp1").geom("geom1").selection().create(
        "csel1", "CumulativeSelection"
    )
    model.java.component("comp1").geom("geom1").selection("csel1").label(
        "Physical Domains Geometry"
    )
    model.java.component("comp1").geom("geom1").create("blk1", "Block")
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "selresult", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "pos", ["0", "0", "(h_air+t_pml)/2"]
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set("base", "center")
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "size", ["w+2*t_pml", "w+2*t_pml", "h_air+t_pml"]
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layername", ["Layer 1"]
    )
    model.java.component("comp1").geom("geom1").feature("blk1").setIndex(
        "layer", "t_pml", 0
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layerleft", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layerright", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layerfront", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layerback", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layerbottom", JBoolean(False)
    )
    model.java.component("comp1").geom("geom1").feature("blk1").set(
        "layertop", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").create("blk2", "Block")
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "selresult", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "pos", ["0", "0", "-(h_subs+t_pml)/2"]
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set("base", "center")
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "size", ["w+2*t_pml", "w+2*t_pml", "h_subs+t_pml"]
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "layername", ["Layer 1"]
    )
    model.java.component("comp1").geom("geom1").feature("blk2").setIndex(
        "layer", "t_pml", Integer(0)
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "layerleft", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "layerright", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "layerfront", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("blk2").set(
        "layerback", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").create("sel_pc1", "ExplicitSelection")
    model.java.component("comp1").geom("geom1").feature("sel_pc1").selection(
        "selection"
    ).init(2)
    model.java.component("comp1").geom("geom1").feature("sel_pc1").selection(
        "selection"
    ).set("blk1(1)", 31, 54)
    model.java.component("comp1").geom("geom1").feature("sel_pc1").selection(
        "selection"
    ).set("blk2(1)", 34, 57)
    model.java.component("comp1").geom("geom1").create("sel_pc2", "ExplicitSelection")
    model.java.component("comp1").geom("geom1").feature("sel_pc2").selection(
        "selection"
    ).init(2)
    model.java.component("comp1").geom("geom1").feature("sel_pc2").selection(
        "selection"
    ).set("blk1(1)", 32, 39)
    model.java.component("comp1").geom("geom1").feature("sel_pc2").selection(
        "selection"
    ).set("blk2(1)", 35, 42)
    model.java.component("comp1").geom("geom1").create("sel_ftri1", "ExplicitSelection")
    model.java.component("comp1").geom("geom1").feature("sel_ftri1").selection(
        "selection"
    ).init(2)
    model.java.component("comp1").geom("geom1").feature("sel_ftri1").selection(
        "selection"
    ).set("blk1(1)", 31, 32, 39, 54)
    model.java.component("comp1").geom("geom1").feature("sel_ftri1").selection(
        "selection"
    ).set("blk2(1)", 34, 35, 42, 57)
    model.java.component("comp1").geom("geom1").create("air", "ExplicitSelection")
    model.java.component("comp1").geom("geom1").feature("air").selection(
        "selection"
    ).set("blk1(1)", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    model.java.component("comp1").geom("geom1").create("substrate", "ExplicitSelection")
    model.java.component("comp1").geom("geom1").feature("substrate").selection(
        "selection"
    ).set("blk2(1)", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    model.java.component("comp1").geom("geom1").create("wp1", "WorkPlane")
    model.java.component("comp1").geom("geom1").feature("wp1").set(
        "unite", JBoolean(True)
    )
    model.java.component("comp1").geom("geom1").feature("wp1").geom().create(
        "image_ic", "InterpolationCurve"
    )
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "image_ic"
    ).set("type", "solid")
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "image_ic"
    ).set("source", "file")
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "image_ic"
    ).set("filename", outer_contour_file_path)
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "image_ic"
    ).set("struct", "sectionwise")
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "image_ic"
    ).set("rtol", 0.001)
    model.java.component("comp1").geom("geom1").feature("wp1").geom().create(
        "scale_ic", "Scale"
    )
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "scale_ic"
    ).setIndex("factor", "5.000000000000001E-7/2400", Integer(0))
    model.java.component("comp1").geom("geom1").feature("wp1").geom().feature(
        "scale_ic"
    ).selection("input").set("image_ic")
    model.java.component("comp1").geom("geom1").create("ext1", "Extrude")
    model.java.component("comp1").geom("geom1").feature("ext1").setIndex(
        "distance", "40[nm]", Integer(0)
    )
    model.java.component("comp1").geom("geom1").feature("ext1").selection("input").set(
        "wp1"
    )
    nano_particle_handle = None
    if inner_contour_file_path is not None:
        model.java.component("comp1").geom("geom1").create("wp2", "WorkPlane")
        model.java.component("comp1").geom("geom1").feature("wp2").set(
            "unite", JBoolean(True)
        )
        model.java.component("comp1").geom("geom1").feature("wp2").geom().create(
            "ic1", "InterpolationCurve"
        )
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "ic1"
        ).set("type", "solid")
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "ic1"
        ).set("source", "file")
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "ic1"
        ).set("filename", inner_contour_file_path)
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "ic1"
        ).set("struct", "sectionwise")
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "ic1"
        ).set("rtol", 0.001)
        model.java.component("comp1").geom("geom1").feature("wp2").geom().create(
            "scale_ic1", "Scale"
        )
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "scale_ic1"
        ).label("Scale")
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "scale_ic1"
        ).setIndex("factor", "5.000000000000001E-7/2400", Integer(0))
        model.java.component("comp1").geom("geom1").feature("wp2").geom().feature(
            "scale_ic1"
        ).selection("input").set("ic1")
        model.java.component("comp1").geom("geom1").create("ext2", "Extrude")
        model.java.component("comp1").geom("geom1").feature("ext2").setIndex(
            "distance", "40[nm]", Integer(0)
        )
        model.java.component("comp1").geom("geom1").feature("ext2").selection(
            "input"
        ).set("wp2")
        model.java.component("comp1").geom("geom1").create("mov2", "Move")
        model.java.component("comp1").geom("geom1").feature("mov2").label("Move")
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "displx", "-250[nm]"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "disply", "-250[nm]"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").selection(
            "input"
        ).set("ext1", "ext2")
        model.java.component("comp1").geom("geom1").create("dif1", "Difference")
        model.java.component("comp1").geom("geom1").feature("dif1").label(
            "Nanoparticle"
        )
        model.java.component("comp1").geom("geom1").feature("dif1").set(
            "contributeto", "csel1"
        )
        model.java.component("comp1").geom("geom1").feature("dif1").set(
            "selresult", JBoolean(True)
        )
        model.java.component("comp1").geom("geom1").feature("dif1").set(
            "selresultshow", "all"
        )

        model.java.component("comp1").geom("geom1").feature("dif1").selection(
            "input"
        ).set("mov2(1)")
        model.java.component("comp1").geom("geom1").feature("dif1").selection(
            "input2"
        ).set("mov2(2)")

        nano_particle_handle = "geom1_dif1"
    else:
        model.java.component("comp1").geom("geom1").create("mov2", "Move")
        model.java.component("comp1").geom("geom1").feature("mov2").label(
            "Nanoparticle"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "contributeto", "csel1"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "selresult", JBoolean(True)
        )
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "selresultshow", "all"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "displx", "-250[nm]"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").set(
            "disply", "-250[nm]"
        )
        model.java.component("comp1").geom("geom1").feature("mov2").selection(
            "input"
        ).set("ext1")
        nano_particle_handle = "geom1_mov2"
    model.java.component("comp1").geom("geom1").run("fin")
    model.java.component("comp1").geom("geom1").create("sel1", "ExplicitSelection")
    model.java.component("comp1").geom("geom1").feature("sel1").label(
        "Physical domains without antenna"
    )
    model.java.component("comp1").geom("geom1").feature("sel1").selection(
        "selection"
    ).set("fin(1)", 18, 19)
    model.java.component("comp1").geom("geom1").feature("sel1").set(
        "contributeto", "csel1"
    )
    model.java.component("comp1").geom("geom1").create("comsel1", "ComplementSelection")
    model.java.component("comp1").geom("geom1").feature("comsel1").label(
        "PML Domains Geometry"
    )
    model.java.component("comp1").geom("geom1").feature("comsel1").set(
        "input", ["csel1"]
    )
    model.java.component("comp1").geom("geom1").run()
    if inner_contour_file_path is not None:
        model.java.component("comp1").geom("geom1").run("dif1")

    model.java.component("comp1").selection().create("sel2", "Explicit")
    model.java.component("comp1").selection("sel2").set(1, 2, 3)
    model.java.component("comp1").selection().create("sel3", "Explicit")
    model.java.component("comp1").selection("sel3").geom("geom1", 3, 2, ["exterior"])
    model.java.component("comp1").selection("sel3").set(1, 2, 3, 4, 5, 6, 7)
    model.java.component("comp1").selection().create("uni1", "Union")

    model.java.component("comp1").variable().create("var1")
    model.java.component("comp1").variable("var1").set("ewfd.Ey", "0")
    model.java.component("comp1").variable("var1").set("ewfd.Ez", "0")
    model.java.component("comp1").variable("var1").set("ewfd.Ex", "0")
    model.java.component("comp1").variable("var1").selection().named("geom1_comsel1")
    model.java.component("comp1").variable().create("var2")
    model.java.component("comp1").variable("var2").set("E0x", "-sin(phi)")
    model.java.component("comp1").variable("var2").set("E0y", "cos(phi)")
    model.java.component("comp1").variable("var2").selection().geom("geom1", Integer(2))
    model.java.component("comp1").variable("var2").selection().set(62, 68)
    model.java.component("comp1").variable().create("var3")
    model.java.component("comp1").variable("var3").set(
        "nrelPoav",
        "nx*ewfd2.relPoavx+ny*ewfd2.relPoavy+nz*ewfd2.relPoavz",
        "Relative normal Poynting flux",
    )
    model.java.component("comp1").variable("var3").set(
        "sigma_sc", "intop_surf(nrelPoav)/I0", "Scattering cross section"
    )
    model.java.component("comp1").variable("var3").set(
        "sigma_abs", "intop_vol(ewfd2.Qh)/I0", "Absorption cross section"
    )
    model.java.component("comp1").variable("var3").set(
        "sigma_ext", "sigma_sc+sigma_abs", "Extinction cross section"
    )

    model.java.component("comp1").view("view1").clip().create("plane1", "ClipPlane")
    model.java.component("comp1").view("view1").clip().create("plane2", "ClipPlane")

    model.java.component("comp1").material().create("mat1", "Common")
    model.java.component("comp1").material().create("mat2", "Common")
    model.java.component("comp1").material().create("mat5", "Common")
    model.java.component("comp1").material("mat1").selection().named("geom1_air")
    model.java.component("comp1").material("mat1").propertyGroup().create(
        "RefractiveIndex", "Refractive index"
    )
    model.java.component("comp1").material("mat2").selection().named("geom1_substrate")
    model.java.component("comp1").material("mat2").propertyGroup().create(
        "RefractiveIndex", "Refractive index"
    )
    model.java.component("comp1").material("mat5").selection().named(
        f"{nano_particle_handle}_dom"
    )
    model.java.component("comp1").material("mat5").propertyGroup().create(
        "RefractiveIndex", "Refractive index"
    )
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func().create("int1", "Interpolation")
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func().create("int2", "Interpolation")

    model.java.component("comp1").cpl().create("intop1", "Integration")
    model.java.component("comp1").cpl().create("intop2", "Integration")
    model.java.component("comp1").cpl("intop1").selection().named(
        f"{nano_particle_handle}_dom"
    )
    model.java.component("comp1").cpl("intop2").selection().named(
        f"{nano_particle_handle}_bnd"
    )

    model.java.component("comp1").coordSystem().create("pml1", "PML")
    model.java.component("comp1").coordSystem("pml1").selection().named("geom1_comsel1")

    model.java.component("comp1").physics().create(
        "ewfd", "ElectromagneticWavesFrequencyDomain", "geom1"
    )
    model.java.component("comp1").physics("ewfd").selection().named("geom1_csel1_dom")
    model.java.component("comp1").physics("ewfd").create(
        "wee2", "WaveEquationElectric", Integer(3)
    )
    model.java.component("comp1").physics("ewfd").feature("wee2").selection().named(
        f"{nano_particle_handle}_dom"
    )
    model.java.component("comp1").physics("ewfd").create("port1", "Port", Integer(2))
    model.java.component("comp1").physics("ewfd").feature("port1").selection().set(68)
    model.java.component("comp1").physics("ewfd").create("port2", "Port", Integer(2))
    model.java.component("comp1").physics("ewfd").feature("port2").selection().set(62)
    model.java.component("comp1").physics("ewfd").create(
        "pc1", "PeriodicCondition", Integer(2)
    )
    model.java.component("comp1").physics("ewfd").feature("pc1").selection().named(
        "geom1_sel_pc1"
    )
    model.java.component("comp1").physics("ewfd").create(
        "pc2", "PeriodicCondition", Integer(2)
    )
    model.java.component("comp1").physics("ewfd").feature("pc2").selection().named(
        "geom1_sel_pc2"
    )
    model.java.component("comp1").physics().create(
        "ewfd2", "ElectromagneticWavesFrequencyDomain", "geom1"
    )

    model.java.component("comp1").mesh("mesh1").create("size1", "Size")
    model.java.component("comp1").mesh("mesh1").create("size2", "Size")
    model.java.component("comp1").mesh("mesh1").create("ftri1", "FreeTri")
    model.java.component("comp1").mesh("mesh1").create("ftet1", "FreeTet")
    model.java.component("comp1").mesh("mesh1").create("swe1", "Sweep")
    model.java.component("comp1").mesh("mesh1").feature("size1").selection().named(
        f"{nano_particle_handle}_dom"
    )
    model.java.component("comp1").mesh("mesh1").feature("size2").selection().geom(
        "geom1", Integer(3)
    )
    model.java.component("comp1").mesh("mesh1").feature("size2").selection().set(18)
    model.java.component("comp1").mesh("mesh1").feature("ftri1").selection().named(
        "geom1_sel_ftri1"
    )
    model.java.component("comp1").mesh("mesh1").feature("ftet1").selection().named(
        "geom1_csel1_dom"
    )
    model.java.component("comp1").mesh("mesh1").feature("swe1").create(
        "dis1", "Distribution"
    )

    model.java.result().table("tbl2").comments("LightToHeat")

    model.java.component("comp1").material("mat1").label("Air")
    model.java.component("comp1").material("mat1").propertyGroup("RefractiveIndex").set(
        "n", ["na", "0", "0", "0", "na", "0", "0", "0", "na"]
    )
    model.java.component("comp1").material("mat2").label("Substrate")
    model.java.component("comp1").material("mat2").propertyGroup("RefractiveIndex").set(
        "n", ["nb", "0", "0", "0", "nb", "0", "0", "0", "nb"]
    )
    model.java.component("comp1").material("mat5").label(
        "Ag (Silver) (Rakic et al. 1998: Brendel-Bormann model n,k 0.248-12.4 um)"
    )
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int1").set("funcname", "nr")
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int1").set(
        "table",
        [
            ["2.4797e-01", "8.4863e-01"],
            ["2.5289e-01", "8.2493e-01"],
            ["2.5791e-01", "7.9699e-01"],
            ["2.6303e-01", "8.0009e-01"],
            ["2.6825e-01", "8.7536e-01"],
            ["2.7358e-01", "1.0320e+00"],
            ["2.7901e-01", "1.2351e+00"],
            ["2.8455e-01", "1.4245e+00"],
            ["2.9020e-01", "1.5424e+00"],
            ["2.9596e-01", "1.5549e+00"],
            ["3.0184e-01", "1.4594e+00"],
            ["3.0783e-01", "1.2767e+00"],
            ["3.1394e-01", "1.0361e+00"],
            ["3.2017e-01", "7.6783e-01"],
            ["3.2653e-01", "5.2213e-01"],
            ["3.3301e-01", "3.6378e-01"],
            ["3.3962e-01", "2.7960e-01"],
            ["3.4637e-01", "2.3178e-01"],
            ["3.5324e-01", "2.0172e-01"],
            ["3.6025e-01", "1.8151e-01"],
            ["3.6741e-01", "1.6741e-01"],
            ["3.7470e-01", "1.5739e-01"],
            ["3.8214e-01", "1.5021e-01"],
            ["3.8973e-01", "1.4506e-01"],
            ["3.9746e-01", "1.4141e-01"],
            ["4.0535e-01", "1.3887e-01"],
            ["4.1340e-01", "1.3716e-01"],
            ["4.2161e-01", "1.3609e-01"],
            ["4.2998e-01", "1.3550e-01"],
            ["4.3852e-01", "1.3529e-01"],
            ["4.4722e-01", "1.3537e-01"],
            ["4.5610e-01", "1.3569e-01"],
            ["4.6515e-01", "1.3621e-01"],
            ["4.7439e-01", "1.3687e-01"],
            ["4.8381e-01", "1.3767e-01"],
            ["4.9341e-01", "1.3857e-01"],
            ["5.0321e-01", "1.3958e-01"],
            ["5.1320e-01", "1.4067e-01"],
            ["5.2339e-01", "1.4184e-01"],
            ["5.3378e-01", "1.4308e-01"],
            ["5.4437e-01", "1.4440e-01"],
            ["5.5518e-01", "1.4578e-01"],
            ["5.6620e-01", "1.4723e-01"],
            ["5.7744e-01", "1.4875e-01"],
            ["5.8891e-01", "1.5034e-01"],
            ["6.0060e-01", "1.5200e-01"],
            ["6.1252e-01", "1.5373e-01"],
            ["6.2468e-01", "1.5554e-01"],
            ["6.3709e-01", "1.5742e-01"],
            ["6.4973e-01", "1.5939e-01"],
            ["6.6263e-01", "1.6143e-01"],
            ["6.7579e-01", "1.6356e-01"],
            ["6.8920e-01", "1.6579e-01"],
            ["7.0289e-01", "1.6810e-01"],
            ["7.1684e-01", "1.7051e-01"],
            ["7.3107e-01", "1.7303e-01"],
            ["7.4559e-01", "1.7565e-01"],
            ["7.6039e-01", "1.7838e-01"],
            ["7.7549e-01", "1.8123e-01"],
            ["7.9088e-01", "1.8420e-01"],
            ["8.0658e-01", "1.8729e-01"],
            ["8.2260e-01", "1.9051e-01"],
            ["8.3893e-01", "1.9387e-01"],
            ["8.5558e-01", "1.9737e-01"],
            ["8.7257e-01", "2.0102e-01"],
            ["8.8989e-01", "2.0482e-01"],
            ["9.0756e-01", "2.0878e-01"],
            ["9.2557e-01", "2.1291e-01"],
            ["9.4395e-01", "2.1721e-01"],
            ["9.6269e-01", "2.2169e-01"],
            ["9.8180e-01", "2.2636e-01"],
            ["1.0013e+00", "2.3122e-01"],
            ["1.0212e+00", "2.3628e-01"],
            ["1.0414e+00", "2.4155e-01"],
            ["1.0621e+00", "2.4705e-01"],
            ["1.0832e+00", "2.5277e-01"],
            ["1.1047e+00", "2.5872e-01"],
            ["1.1266e+00", "2.6493e-01"],
            ["1.1490e+00", "2.7138e-01"],
            ["1.1718e+00", "2.7811e-01"],
            ["1.1951e+00", "2.8511e-01"],
            ["1.2188e+00", "2.9239e-01"],
            ["1.2430e+00", "2.9998e-01"],
            ["1.2677e+00", "3.0788e-01"],
            ["1.2929e+00", "3.1609e-01"],
            ["1.3185e+00", "3.2465e-01"],
            ["1.3447e+00", "3.3355e-01"],
            ["1.3714e+00", "3.4281e-01"],
            ["1.3986e+00", "3.5245e-01"],
            ["1.4264e+00", "3.6249e-01"],
            ["1.4547e+00", "3.7292e-01"],
            ["1.4836e+00", "3.8379e-01"],
            ["1.5130e+00", "3.9509e-01"],
            ["1.5431e+00", "4.0684e-01"],
            ["1.5737e+00", "4.1908e-01"],
            ["1.6050e+00", "4.3180e-01"],
            ["1.6368e+00", "4.4504e-01"],
            ["1.6693e+00", "4.5882e-01"],
            ["1.7025e+00", "4.7314e-01"],
            ["1.7363e+00", "4.8805e-01"],
            ["1.7707e+00", "5.0355e-01"],
            ["1.8059e+00", "5.1967e-01"],
            ["1.8417e+00", "5.3644e-01"],
            ["1.8783e+00", "5.5389e-01"],
            ["1.9156e+00", "5.7203e-01"],
            ["1.9536e+00", "5.9090e-01"],
            ["1.9924e+00", "6.1053e-01"],
            ["2.0319e+00", "6.3094e-01"],
            ["2.0723e+00", "6.5216e-01"],
            ["2.1134e+00", "6.7424e-01"],
            ["2.1554e+00", "6.9719e-01"],
            ["2.1982e+00", "7.2106e-01"],
            ["2.2418e+00", "7.4588e-01"],
            ["2.2863e+00", "7.7170e-01"],
            ["2.3317e+00", "7.9854e-01"],
            ["2.3780e+00", "8.2645e-01"],
            ["2.4252e+00", "8.5546e-01"],
            ["2.4734e+00", "8.8564e-01"],
            ["2.5225e+00", "9.1701e-01"],
            ["2.5725e+00", "9.4962e-01"],
            ["2.6236e+00", "9.8353e-01"],
            ["2.6757e+00", "1.0188e+00"],
            ["2.7288e+00", "1.0554e+00"],
            ["2.7830e+00", "1.0935e+00"],
            ["2.8383e+00", "1.1332e+00"],
            ["2.8946e+00", "1.1743e+00"],
            ["2.9521e+00", "1.2171e+00"],
            ["3.0107e+00", "1.2616e+00"],
            ["3.0704e+00", "1.3079e+00"],
            ["3.1314e+00", "1.3560e+00"],
            ["3.1936e+00", "1.4060e+00"],
            ["3.2570e+00", "1.4579e+00"],
            ["3.3216e+00", "1.5119e+00"],
            ["3.3876e+00", "1.5680e+00"],
            ["3.4548e+00", "1.6263e+00"],
            ["3.5234e+00", "1.6869e+00"],
            ["3.5934e+00", "1.7499e+00"],
            ["3.6647e+00", "1.8153e+00"],
            ["3.7375e+00", "1.8833e+00"],
            ["3.8117e+00", "1.9540e+00"],
            ["3.8873e+00", "2.0274e+00"],
            ["3.9645e+00", "2.1036e+00"],
            ["4.0432e+00", "2.1829e+00"],
            ["4.1235e+00", "2.2652e+00"],
            ["4.2053e+00", "2.3507e+00"],
            ["4.2888e+00", "2.4396e+00"],
            ["4.3740e+00", "2.5319e+00"],
            ["4.4608e+00", "2.6277e+00"],
            ["4.5494e+00", "2.7273e+00"],
            ["4.6397e+00", "2.8307e+00"],
            ["4.7318e+00", "2.9381e+00"],
            ["4.8257e+00", "3.0496e+00"],
            ["4.9216e+00", "3.1654e+00"],
            ["5.0193e+00", "3.2856e+00"],
            ["5.1189e+00", "3.4104e+00"],
            ["5.2205e+00", "3.5400e+00"],
            ["5.3242e+00", "3.6745e+00"],
            ["5.4299e+00", "3.8141e+00"],
            ["5.5377e+00", "3.9591e+00"],
            ["5.6476e+00", "4.1095e+00"],
            ["5.7597e+00", "4.2656e+00"],
            ["5.8741e+00", "4.4275e+00"],
            ["5.9907e+00", "4.5956e+00"],
            ["6.1096e+00", "4.7699e+00"],
            ["6.2309e+00", "4.9508e+00"],
            ["6.3546e+00", "5.1384e+00"],
            ["6.4808e+00", "5.3329e+00"],
            ["6.6094e+00", "5.5347e+00"],
            ["6.7407e+00", "5.7439e+00"],
            ["6.8745e+00", "5.9609e+00"],
            ["7.0110e+00", "6.1857e+00"],
            ["7.1502e+00", "6.4188e+00"],
            ["7.2921e+00", "6.6604e+00"],
            ["7.4369e+00", "6.9107e+00"],
            ["7.5845e+00", "7.1701e+00"],
            ["7.7351e+00", "7.4389e+00"],
            ["7.8887e+00", "7.7172e+00"],
            ["8.0453e+00", "8.0055e+00"],
            ["8.2050e+00", "8.3040e+00"],
            ["8.3679e+00", "8.6131e+00"],
            ["8.5340e+00", "8.9330e+00"],
            ["8.7034e+00", "9.2642e+00"],
            ["8.8762e+00", "9.6068e+00"],
            ["9.0524e+00", "9.9614e+00"],
            ["9.2322e+00", "1.0328e+01"],
            ["9.4154e+00", "1.0707e+01"],
            ["9.6024e+00", "1.1100e+01"],
            ["9.7930e+00", "1.1505e+01"],
            ["9.9874e+00", "1.1924e+01"],
            ["1.0186e+01", "1.2357e+01"],
            ["1.0388e+01", "1.2805e+01"],
            ["1.0594e+01", "1.3267e+01"],
            ["1.0804e+01", "1.3744e+01"],
            ["1.1019e+01", "1.4237e+01"],
            ["1.1238e+01", "1.4746e+01"],
            ["1.1461e+01", "1.5270e+01"],
            ["1.1688e+01", "1.5812e+01"],
            ["1.1920e+01", "1.6370e+01"],
            ["1.2157e+01", "1.6946e+01"],
            ["1.2398e+01", "1.7540e+01"],
        ],
    )
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int1").set("fununit", ["1"])
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int1").set("argunit", ["um"])
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int2").set("funcname", "ni")
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int2").set(
        "table",
        [
            ["2.4797e-01", "1.1920e+00"],
            ["2.5289e-01", "1.2193e+00"],
            ["2.5791e-01", "1.2844e+00"],
            ["2.6303e-01", "1.3955e+00"],
            ["2.6825e-01", "1.5246e+00"],
            ["2.7358e-01", "1.6142e+00"],
            ["2.7901e-01", "1.6125e+00"],
            ["2.8455e-01", "1.5017e+00"],
            ["2.9020e-01", "1.3028e+00"],
            ["2.9596e-01", "1.0631e+00"],
            ["3.0184e-01", "8.3581e-01"],
            ["3.0783e-01", "6.6203e-01"],
            ["3.1394e-01", "5.6621e-01"],
            ["3.2017e-01", "5.6549e-01"],
            ["3.2653e-01", "6.7421e-01"],
            ["3.3301e-01", "8.4735e-01"],
            ["3.3962e-01", "1.0142e+00"],
            ["3.4637e-01", "1.1589e+00"],
            ["3.5324e-01", "1.2860e+00"],
            ["3.6025e-01", "1.4005e+00"],
            ["3.6741e-01", "1.5059e+00"],
            ["3.7470e-01", "1.6045e+00"],
            ["3.8214e-01", "1.6979e+00"],
            ["3.8973e-01", "1.7873e+00"],
            ["3.9746e-01", "1.8736e+00"],
            ["4.0535e-01", "1.9574e+00"],
            ["4.1340e-01", "2.0394e+00"],
            ["4.2161e-01", "2.1200e+00"],
            ["4.2998e-01", "2.1995e+00"],
            ["4.3852e-01", "2.2782e+00"],
            ["4.4722e-01", "2.3564e+00"],
            ["4.5610e-01", "2.4344e+00"],
            ["4.6515e-01", "2.5122e+00"],
            ["4.7439e-01", "2.5901e+00"],
            ["4.8381e-01", "2.6682e+00"],
            ["4.9341e-01", "2.7466e+00"],
            ["5.0321e-01", "2.8254e+00"],
            ["5.1320e-01", "2.9048e+00"],
            ["5.2339e-01", "2.9848e+00"],
            ["5.3378e-01", "3.0656e+00"],
            ["5.4437e-01", "3.1471e+00"],
            ["5.5518e-01", "3.2295e+00"],
            ["5.6620e-01", "3.3128e+00"],
            ["5.7744e-01", "3.3971e+00"],
            ["5.8891e-01", "3.4825e+00"],
            ["6.0060e-01", "3.5690e+00"],
            ["6.1252e-01", "3.6567e+00"],
            ["6.2468e-01", "3.7455e+00"],
            ["6.3709e-01", "3.8357e+00"],
            ["6.4973e-01", "3.9272e+00"],
            ["6.6263e-01", "4.0200e+00"],
            ["6.7579e-01", "4.1143e+00"],
            ["6.8920e-01", "4.2100e+00"],
            ["7.0289e-01", "4.3072e+00"],
            ["7.1684e-01", "4.4061e+00"],
            ["7.3107e-01", "4.5065e+00"],
            ["7.4559e-01", "4.6085e+00"],
            ["7.6039e-01", "4.7123e+00"],
            ["7.7549e-01", "4.8178e+00"],
            ["7.9088e-01", "4.9251e+00"],
            ["8.0658e-01", "5.0343e+00"],
            ["8.2260e-01", "5.1453e+00"],
            ["8.3893e-01", "5.2583e+00"],
            ["8.5558e-01", "5.3732e+00"],
            ["8.7257e-01", "5.4902e+00"],
            ["8.8989e-01", "5.6093e+00"],
            ["9.0756e-01", "5.7304e+00"],
            ["9.2557e-01", "5.8538e+00"],
            ["9.4395e-01", "5.9793e+00"],
            ["9.6269e-01", "6.1072e+00"],
            ["9.8180e-01", "6.2373e+00"],
            ["1.0013e+00", "6.3699e+00"],
            ["1.0212e+00", "6.5048e+00"],
            ["1.0414e+00", "6.6423e+00"],
            ["1.0621e+00", "6.7823e+00"],
            ["1.0832e+00", "6.9248e+00"],
            ["1.1047e+00", "7.0700e+00"],
            ["1.1266e+00", "7.2179e+00"],
            ["1.1490e+00", "7.3686e+00"],
            ["1.1718e+00", "7.5221e+00"],
            ["1.1951e+00", "7.6785e+00"],
            ["1.2188e+00", "7.8378e+00"],
            ["1.2430e+00", "8.0001e+00"],
            ["1.2677e+00", "8.1654e+00"],
            ["1.2929e+00", "8.3339e+00"],
            ["1.3185e+00", "8.5056e+00"],
            ["1.3447e+00", "8.6805e+00"],
            ["1.3714e+00", "8.8587e+00"],
            ["1.3986e+00", "9.0403e+00"],
            ["1.4264e+00", "9.2254e+00"],
            ["1.4547e+00", "9.4140e+00"],
            ["1.4836e+00", "9.6062e+00"],
            ["1.5130e+00", "9.8021e+00"],
            ["1.5431e+00", "1.0002e+01"],
            ["1.5737e+00", "1.0205e+01"],
            ["1.6050e+00", "1.0412e+01"],
            ["1.6368e+00", "1.0624e+01"],
            ["1.6693e+00", "1.0839e+01"],
            ["1.7025e+00", "1.1059e+01"],
            ["1.7363e+00", "1.1282e+01"],
            ["1.7707e+00", "1.1510e+01"],
            ["1.8059e+00", "1.1743e+01"],
            ["1.8417e+00", "1.1979e+01"],
            ["1.8783e+00", "1.2221e+01"],
            ["1.9156e+00", "1.2467e+01"],
            ["1.9536e+00", "1.2718e+01"],
            ["1.9924e+00", "1.2973e+01"],
            ["2.0319e+00", "1.3234e+01"],
            ["2.0723e+00", "1.3499e+01"],
            ["2.1134e+00", "1.3770e+01"],
            ["2.1554e+00", "1.4046e+01"],
            ["2.1982e+00", "1.4327e+01"],
            ["2.2418e+00", "1.4614e+01"],
            ["2.2863e+00", "1.4906e+01"],
            ["2.3317e+00", "1.5203e+01"],
            ["2.3780e+00", "1.5507e+01"],
            ["2.4252e+00", "1.5816e+01"],
            ["2.4734e+00", "1.6131e+01"],
            ["2.5225e+00", "1.6453e+01"],
            ["2.5725e+00", "1.6780e+01"],
            ["2.6236e+00", "1.7114e+01"],
            ["2.6757e+00", "1.7454e+01"],
            ["2.7288e+00", "1.7801e+01"],
            ["2.7830e+00", "1.8154e+01"],
            ["2.8383e+00", "1.8514e+01"],
            ["2.8946e+00", "1.8881e+01"],
            ["2.9521e+00", "1.9255e+01"],
            ["3.0107e+00", "1.9636e+01"],
            ["3.0704e+00", "2.0025e+01"],
            ["3.1314e+00", "2.0421e+01"],
            ["3.1936e+00", "2.0824e+01"],
            ["3.2570e+00", "2.1235e+01"],
            ["3.3216e+00", "2.1654e+01"],
            ["3.3876e+00", "2.2081e+01"],
            ["3.4548e+00", "2.2516e+01"],
            ["3.5234e+00", "2.2959e+01"],
            ["3.5934e+00", "2.3410e+01"],
            ["3.6647e+00", "2.3870e+01"],
            ["3.7375e+00", "2.4339e+01"],
            ["3.8117e+00", "2.4817e+01"],
            ["3.8873e+00", "2.5303e+01"],
            ["3.9645e+00", "2.5799e+01"],
            ["4.0432e+00", "2.6304e+01"],
            ["4.1235e+00", "2.6818e+01"],
            ["4.2053e+00", "2.7342e+01"],
            ["4.2888e+00", "2.7876e+01"],
            ["4.3740e+00", "2.8419e+01"],
            ["4.4608e+00", "2.8973e+01"],
            ["4.5494e+00", "2.9537e+01"],
            ["4.6397e+00", "3.0111e+01"],
            ["4.7318e+00", "3.0696e+01"],
            ["4.8257e+00", "3.1291e+01"],
            ["4.9216e+00", "3.1898e+01"],
            ["5.0193e+00", "3.2515e+01"],
            ["5.1189e+00", "3.3143e+01"],
            ["5.2205e+00", "3.3783e+01"],
            ["5.3242e+00", "3.4435e+01"],
            ["5.4299e+00", "3.5098e+01"],
            ["5.5377e+00", "3.5773e+01"],
            ["5.6476e+00", "3.6460e+01"],
            ["5.7597e+00", "3.7159e+01"],
            ["5.8741e+00", "3.7870e+01"],
            ["5.9907e+00", "3.8594e+01"],
            ["6.1096e+00", "3.9331e+01"],
            ["6.2309e+00", "4.0080e+01"],
            ["6.3546e+00", "4.0842e+01"],
            ["6.4808e+00", "4.1618e+01"],
            ["6.6094e+00", "4.2407e+01"],
            ["6.7407e+00", "4.3209e+01"],
            ["6.8745e+00", "4.4025e+01"],
            ["7.0110e+00", "4.4854e+01"],
            ["7.1502e+00", "4.5697e+01"],
            ["7.2921e+00", "4.6555e+01"],
            ["7.4369e+00", "4.7426e+01"],
            ["7.5845e+00", "4.8312e+01"],
            ["7.7351e+00", "4.9212e+01"],
            ["7.8887e+00", "5.0126e+01"],
            ["8.0453e+00", "5.1055e+01"],
            ["8.2050e+00", "5.1999e+01"],
            ["8.3679e+00", "5.2958e+01"],
            ["8.5340e+00", "5.3931e+01"],
            ["8.7034e+00", "5.4920e+01"],
            ["8.8762e+00", "5.5923e+01"],
            ["9.0524e+00", "5.6942e+01"],
            ["9.2322e+00", "5.7976e+01"],
            ["9.4154e+00", "5.9025e+01"],
            ["9.6024e+00", "6.0090e+01"],
            ["9.7930e+00", "6.1170e+01"],
            ["9.9874e+00", "6.2265e+01"],
            ["1.0186e+01", "6.3376e+01"],
            ["1.0388e+01", "6.4502e+01"],
            ["1.0594e+01", "6.5643e+01"],
            ["1.0804e+01", "6.6800e+01"],
            ["1.1019e+01", "6.7973e+01"],
            ["1.1238e+01", "6.9160e+01"],
            ["1.1461e+01", "7.0363e+01"],
            ["1.1688e+01", "7.1581e+01"],
            ["1.1920e+01", "7.2814e+01"],
            ["1.2157e+01", "7.4063e+01"],
            ["1.2398e+01", "7.5326e+01"],
        ],
    )

    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int2").set("fununit", ["1"])
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).func("int2").set("argunit", ["um"])
    model.java.component("comp1").material("mat5").propertyGroup("RefractiveIndex").set(
        "n",
        [
            "nr(c_const/freq)",
            "0",
            "0",
            "0",
            "nr(c_const/freq)",
            "0",
            "0",
            "0",
            "nr(c_const/freq)",
        ],
    )
    model.java.component("comp1").material("mat5").propertyGroup("RefractiveIndex").set(
        "ki",
        [
            "ni(c_const/freq)",
            "0",
            "0",
            "0",
            "ni(c_const/freq)",
            "0",
            "0",
            "0",
            "ni(c_const/freq)",
        ],
    )
    model.java.component("comp1").material("mat5").propertyGroup(
        "RefractiveIndex"
    ).addInput("frequency")

    model.java.component("comp1").cpl("intop1").set("opname", "intop_vol")
    model.java.component("comp1").cpl("intop2").set("opname", "intop_surf")

    model.java.component("comp1").coordSystem("pml1").set("wavelengthSource", "ewfd2")

    model.java.common("cminpt").set("modified", [["frequency", "563.5 [THz]"]])

    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "DisplacementFieldModel", "RelativePermittivity"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "omegap", "13.8*10^15"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set("f", Integer(1))
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "omega0", "400[THz]"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "epsilonr_mat", "userdef"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "epsilonr", [[0.054007], [0], [0], [0], [0.054007], [0], [0], [0], [0.054007]]
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "epsilonInf_mat", "from_mat"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "mur_mat", "userdef"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "sigma_mat", "userdef"
    )
    model.java.component("comp1").physics("ewfd").feature("wee1").set(
        "sigma",
        [["45e6"], ["0"], ["0"], ["0"], ["45e6"], ["0"], ["0"], ["0"], ["45e6"]],
    )
    model.java.component("comp1").physics("ewfd").feature("wee2").set(
        "n", [["na"], ["0"], ["0"], ["0"], ["na"], ["0"], ["0"], ["0"], ["na"]]
    )
    model.java.component("comp1").physics("ewfd").feature("port1").set("Pin", "P")
    model.java.component("comp1").physics("ewfd").feature("port1").set(
        "PortType", "Periodic"
    )
    model.java.component("comp1").physics("ewfd").feature("port1").set(
        "Eampl", [["E0x"], ["E0y"], ["0"]]
    )
    model.java.component("comp1").physics("ewfd").feature("port1").set(
        "alpha1_inc", "theta"
    )
    model.java.component("comp1").physics("ewfd").feature("port1").set(
        "alpha2_inc", "phi"
    )
    model.java.component("comp1").physics("ewfd").feature("port1").set(
        "n", [["na"], ["0"], ["0"], ["0"], ["na"], ["0"], ["0"], ["0"], ["na"]]
    )
    model.java.component("comp1").physics("ewfd").feature("port2").set(
        "PortType", "Periodic"
    )
    model.java.component("comp1").physics("ewfd").feature("port2").set(
        "Eampl", [["E0x"], ["E0y"], ["0"]]
    )
    model.java.component("comp1").physics("ewfd").feature("port2").set(
        "n", [["nb"], ["0"], ["0"], ["0"], ["nb"], ["0"], ["0"], ["0"], ["nb"]]
    )
    model.java.component("comp1").physics("ewfd").feature("pc1").set(
        "PeriodicType", "Floquet"
    )
    model.java.component("comp1").physics("ewfd").feature("pc1").set(
        "Floquet_source", "FromPeriodicPort"
    )
    model.java.component("comp1").physics("ewfd").feature("pc2").set(
        "PeriodicType", "Floquet"
    )
    model.java.component("comp1").physics("ewfd").feature("pc2").set(
        "Floquet_source", "FromPeriodicPort"
    )
    model.java.component("comp1").physics("ewfd2").prop("BackgroundField").set(
        "SolveFor", "scatteredField"
    )
    model.java.component("comp1").physics("ewfd2").prop("BackgroundField").set(
        "Eb", [["ewfd.Ex"], ["ewfd.Ey"], ["ewfd.Ez"]]
    )
    model.java.component("comp1").physics("ewfd2").feature("wee1").set(
        "DisplacementFieldModel", "RelativePermittivity"
    )
    model.java.component("comp1").physics("ewfd2").feature("wee1").set(
        "omegap", "13.8*10^15"
    )
    model.java.component("comp1").physics("ewfd2").feature("wee1").set("f", Integer(1))
    model.java.component("comp1").physics("ewfd2").feature("wee1").set(
        "omega0", "400[THz]"
    )
    model.java.component("comp1").physics("ewfd2").feature("wee1").set(
        "mur_mat", "userdef"
    )
    model.java.component("comp1").physics("ewfd2").feature("wee1").set(
        "sigma_mat", "userdef"
    )

    model.java.component("comp1").mesh("mesh1").feature("size").set("custom", "on")
    model.java.component("comp1").mesh("mesh1").feature("size").set("hmax", "lda0/6")
    model.java.component("comp1").mesh("mesh1").feature("size1").set(
        "hauto", Integer(4)
    )
    model.java.component("comp1").mesh("mesh1").feature("size2").set("custom", "on")
    model.java.component("comp1").mesh("mesh1").feature("size2").set(
        "hmax", "lda0/6/nb"
    )
    model.java.component("comp1").mesh("mesh1").feature("size2").set(
        "hmaxactive", JBoolean(True)
    )
    model.java.component("comp1").mesh("mesh1").feature("ftri1").set(
        "smoothmaxiter", Integer(10)
    )
    model.java.component("comp1").mesh("mesh1").feature("ftri1").set(
        "smoothmaxdepth", Integer(10)
    )
    model.java.component("comp1").mesh("mesh1").feature("ftet1").set(
        "smoothmaxiter", Integer(10)
    )
    model.java.component("comp1").mesh("mesh1").feature("ftet1").set(
        "smoothmaxdepth", Integer(10)
    )
    model.java.component("comp1").mesh("mesh1").feature("ftet1").set("optlevel", "high")
    model.java.component("comp1").mesh("mesh1").feature("swe1").set(
        "smoothmaxiter", Integer(10)
    )
    model.java.component("comp1").mesh("mesh1").feature("swe1").set(
        "smoothmaxdepth", Integer(10)
    )
    model.java.component("comp1").mesh("mesh1").feature("swe1").feature("dis1").set(
        "numelem", Integer(8)
    )
    model.java.component("comp1").mesh("mesh1").run()

    model.java.study().create("std1")
    model.java.study("std1").create("wave", "Wavelength")
    model.java.study("std1").create("wave2", "Wavelength")
    model.java.study("std1").feature("wave").set(
        "activate",
        ["ewfd", "on", "ewfd2", "off", "frame:spatial1", "on", "frame:material1", "on"],
    )
    model.java.study("std1").feature("wave2").set(
        "activate",
        ["ewfd", "off", "ewfd2", "on", "frame:spatial1", "on", "frame:material1", "on"],
    )


    model.java.sol().create("sol1")
    model.java.sol("sol1").study("std1")
    model.java.sol("sol1").attach("std1")
    model.java.sol("sol1").create("st1", "StudyStep")
    model.java.sol("sol1").create("v1", "Variables")
    model.java.sol("sol1").create("s1", "Stationary")
    model.java.sol("sol1").create("st2", "StudyStep")
    model.java.sol("sol1").create("v2", "Variables")
    model.java.sol("sol1").create("s2", "Stationary")
    model.java.sol("sol1").feature("s1").create("p1", "Parametric")
    model.java.sol("sol1").feature("s1").create("fc1", "FullyCoupled")
    model.java.sol("sol1").feature("s1").create("d1", "Direct")
    model.java.sol("sol1").feature("s1").create("i1", "Iterative")
    model.java.sol("sol1").feature("s1").feature("i1").create("mg1", "Multigrid")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).create("va1", "Vanka")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).create("sv1", "SORVector")
    model.java.sol("sol1").feature("s1").feature().remove("fcDef")
    model.java.sol("sol1").feature("s2").create("p1", "Parametric")
    model.java.sol("sol1").feature("s2").create("fc1", "FullyCoupled")
    model.java.sol("sol1").feature("s2").create("i1", "Iterative")
    model.java.sol("sol1").feature("s2").create("i2", "Iterative")
    model.java.sol("sol1").feature("s2").feature("i1").create("mg1", "Multigrid")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "pr"
    ).create("sv1", "SORVector")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "po"
    ).create("sv1", "SORVector")
    model.java.sol("sol1").feature("s2").feature("i2").create("mg1", "Multigrid")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "pr"
    ).create("sv1", "SORVector")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "po"
    ).create("sv1", "SORVector")
    model.java.sol("sol1").feature("s2").feature().remove("fcDef")
    model.java.sol().create("sol2")
    model.java.sol("sol2").study("std1")
    model.java.sol("sol2").label("Parametric Solutions 1")
    model.java.result().dataset().remove("dset2")
    model.java.result().numerical().create("int1", "IntVolume")
    model.java.result().numerical().create("gev1", "EvalGlobal")
    model.java.result().numerical("int1").selection().named(
        f"{nano_particle_handle}_dom"
    )
    model.java.result().numerical("int1").set("probetag", "none")
    model.java.result().numerical("gev1").set("probetag", "none")
    model.java.result().create("pg1", "PlotGroup3D")
    model.java.result().create("pg2", "PlotGroup1D")
    model.java.result().create("pg3", "PlotGroup3D")
    model.java.result("pg1").create("mslc1", "Multislice")
    model.java.result("pg2").create("plz1", "Polarization")
    model.java.result("pg2").create("plz2", "Polarization")
    model.java.result("pg2").feature("plz1").create("col1", "Color")
    model.java.result("pg2").feature("plz2").create("col1", "Color")
    model.java.result("pg3").create("mslc1", "Multislice")
    model.java.result("pg3").feature("mslc1").set("expr", "ewfd2.normE")

    model.java.nodeGroup().create("grp1", "Definitions", "comp1")
    model.java.nodeGroup("grp1").set("type", "selection")
    model.java.nodeGroup("grp1").placeAfter("selection", "uni1")

    model.java.study("std1").feature("wave").set("plist", "lda0")
    model.java.study("std1").feature("wave2").set("plist", "lda0")

    model.java.sol("sol1").attach("std1")
    model.java.sol("sol1").feature("st1").label("Compile Equations: Wavelength Domain")
    model.java.sol("sol1").feature("v1").label("Dependent Variables 1.1")
    model.java.sol("sol1").feature("v1").set("clistctrl", ["p1"])
    model.java.sol("sol1").feature("v1").set("cname", ["lambda0"])
    model.java.sol("sol1").feature("v1").set("clist", ["lda0"])
    model.java.sol("sol1").feature("s1").label("Stationary Solver 1.1")
    model.java.sol("sol1").feature("s1").set("stol", 0.01)
    model.java.sol("sol1").feature("s1").feature("dDef").active(JBoolean(True))
    model.java.sol("sol1").feature("s1").feature("dDef").label("Direct 2")
    model.java.sol("sol1").feature("s1").feature("dDef").set("linsolver", "pardiso")
    model.java.sol("sol1").feature("s1").feature("aDef").label("Advanced 1")
    model.java.sol("sol1").feature("s1").feature("aDef").set(
        "complexfun", JBoolean(True)
    )
    model.java.sol("sol1").feature("s1").feature("p1").label("Parametric 1.1")
    model.java.sol("sol1").feature("s1").feature("p1").set("pname", ["lambda0"])
    model.java.sol("sol1").feature("s1").feature("p1").set("plistarr", ["lda0"])
    model.java.sol("sol1").feature("s1").feature("p1").set("punit", ["\u00b5m"])
    model.java.sol("sol1").feature("s1").feature("p1").set("pcontinuationmode", "no")
    model.java.sol("sol1").feature("s1").feature("p1").set("preusesol", "auto")
    model.java.sol("sol1").feature("s1").feature("p1").set(
        "uselsqdata", JBoolean(False)
    )
    model.java.sol("sol1").feature("s1").feature("fc1").label("Fully Coupled 1.1")
    model.java.sol("sol1").feature("s1").feature("d1").label(
        "Suggested Direct Solver (ewfd)"
    )
    model.java.sol("sol1").feature("s1").feature("i1").label(
        "Suggested Iterative Solver (ewfd)"
    )
    model.java.sol("sol1").feature("s1").feature("i1").set("itrestart", Integer(300))
    model.java.sol("sol1").feature("s1").feature("i1").set("prefuntype", "right")
    model.java.sol("sol1").feature("s1").feature("i1").feature("ilDef").label(
        "Incomplete LU 1"
    )
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").label(
        "Multigrid 1.1"
    )
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").set(
        "iter", Integer(1)
    )
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).label("Presmoother 1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("soDef").label("SOR 1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("va1").label("Vanka 1.1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("va1").set("iter", Integer(1))
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("va1").set("vankavars", ["comp1_E"])
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("va1").set("vankasolv", "stored")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("va1").set("vankarelax", 0.95)
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).label("Postsmoother 1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).feature("soDef").label("SOR 1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).feature("sv1").label("SOR Vector 1.1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).feature("sv1").set("iter", Integer(1))
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).feature("sv1").set("relax", 0.5)
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "po"
    ).feature("sv1").set("sorvecdof", ["comp1_E"])
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "cs"
    ).label("Coarse Solver 1")
    model.java.sol("sol1").feature("s1").feature("i1").feature("mg1").feature(
        "cs"
    ).feature("dDef").label("Direct 1")
    model.java.sol("sol1").feature("st2").label(
        "Compile Equations: Wavelength Domain 2"
    )

    model.java.sol("sol1").feature("st2").set("studystep", "wave2")
    model.java.sol("sol1").feature("v2").label("Dependent Variables 2.1")
    model.java.sol("sol1").feature("v2").set("initmethod", "sol")
    model.java.sol("sol1").feature("v2").set("initsol", "sol1")
    model.java.sol("sol1").feature("v2").set("solnum", "auto")
    model.java.sol("sol1").feature("v2").set("notsolmethod", "sol")
    model.java.sol("sol1").feature("v2").set("notsol", "sol1")
    model.java.sol("sol1").feature("v2").set("notsolnum", "auto")
    model.java.sol("sol1").feature("v2").set("clistctrl", ["p1"])
    model.java.sol("sol1").feature("v2").set("cname", ["lambda0"])
    model.java.sol("sol1").feature("v2").set("clist", ["lda0"])
    model.java.sol("sol1").feature("s2").label("Stationary Solver 2.1")
    model.java.sol("sol1").feature("s2").feature("dDef").active(JBoolean(True))
    model.java.sol("sol1").feature("s2").feature("dDef").label("Direct 1")
    model.java.sol("sol1").feature("s2").feature("dDef").set("linsolver", "pardiso")
    model.java.sol("sol1").feature("s2").feature("aDef").label("Advanced 1")
    model.java.sol("sol1").feature("s2").feature("aDef").set(
        "complexfun", JBoolean(True)
    )
    model.java.sol("sol1").feature("s2").feature("p1").label("Parametric 1.1")
    model.java.sol("sol1").feature("s2").feature("p1").set("pname", ["lambda0"])
    model.java.sol("sol1").feature("s2").feature("p1").set("plistarr", ["lda0"])
    model.java.sol("sol1").feature("s2").feature("p1").set("punit", ["\u00b5m"])
    model.java.sol("sol1").feature("s2").feature("p1").set("pcontinuationmode", "no")
    model.java.sol("sol1").feature("s2").feature("p1").set("preusesol", "auto")
    model.java.sol("sol1").feature("s2").feature("p1").set(
        "uselsqdata", JBoolean(False)
    )
    model.java.sol("sol1").feature("s2").feature("fc1").label("Fully Coupled 1.1")
    model.java.sol("sol1").feature("s2").feature("i1").label(
        "Suggested Iterative Solver (ewfd2)"
    )
    model.java.sol("sol1").feature("s2").feature("i1").set("linsolver", "bicgstab")
    model.java.sol("sol1").feature("s2").feature("i1").feature("ilDef").label(
        "Incomplete LU 1"
    )
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").label(
        "Multigrid 1.1"
    )
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "pr"
    ).label("Presmoother 1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("soDef").label("SOR 1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("sv1").label("SOR Vector 1.1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "pr"
    ).feature("sv1").set("sorvecdof", ["comp1_E2"])
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "po"
    ).label("Postsmoother 1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "po"
    ).feature("soDef").label("SOR 1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "po"
    ).feature("sv1").label("SOR Vector 1.1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "po"
    ).feature("sv1").set("sorvecdof", ["comp1_E2"])
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "cs"
    ).label("Coarse Solver 1")
    model.java.sol("sol1").feature("s2").feature("i1").feature("mg1").feature(
        "cs"
    ).feature("dDef").label("Direct 1")
    model.java.sol("sol1").feature("s2").feature("i2").label(
        "Suggested Iterative Solver (ewfd2) 2"
    )
    model.java.sol("sol1").feature("s2").feature("i2").set("linsolver", "fgmres")
    model.java.sol("sol1").feature("s2").feature("i2").feature("ilDef").label(
        "Incomplete LU 1"
    )
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").label(
        "Multigrid 1.1"
    )
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "pr"
    ).label("Presmoother 1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "pr"
    ).feature("soDef").label("SOR 1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "pr"
    ).feature("sv1").label("SOR Vector 1.1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "pr"
    ).feature("sv1").set("sorvecdof", ["comp1_E2"])
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "po"
    ).label("Postsmoother 1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "po"
    ).feature("soDef").label("SOR 1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "po"
    ).feature("sv1").label("SOR Vector 1.1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "po"
    ).feature("sv1").set("sorvecdof", ["comp1_E2"])
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "cs"
    ).label("Coarse Solver 1")
    model.java.sol("sol1").feature("s2").feature("i2").feature("mg1").feature(
        "cs"
    ).feature("dDef").label("Direct 1")
    model.java.sol("sol1").runAll()

    model.java.result().numerical("int1").label("LightToHeat")
    model.java.result().numerical("int1").set("table", "tbl2")
    model.java.result().numerical("int1").set("expr", ["ewfd2.Qh/(I0*w*w)"])
    model.java.result().numerical("int1").set("unit", ["1"])
    model.java.result().numerical("int1").set("descr", [""])
    model.java.result().numerical("gev1").label(
        "Reflectance, Transmittance, and Absorptance (ewfd)"
    )
    model.java.result().numerical("gev1").set("table", "tbl1")
    model.java.result().numerical("gev1").set(
        "expr",
        [
            "ewfd.Rorder_0_0",
            "ewfd.Rtotal",
            "ewfd.Torder_0_0",
            "ewfd.Ttotal",
            "ewfd.RTtotal",
            "ewfd.Atotal",
        ],
    )
    model.java.result().numerical("gev1").set("unit", ["1", "1", "1", "1", "1", "1"])
    model.java.result().numerical("gev1").set(
        "descr",
        [
            "Reflectance, order [0,0]",
            "Total reflectance",
            "Transmittance, order [0,0]",
            "Total transmittance",
            "Total reflectance and transmittance",
            "Absorptance",
        ],
    )

    model.java.result().numerical("int1").setResult()
    model.java.result().numerical("gev1").setResult()
    model.java.result("pg1").label("Electric Field (ewfd)")
    model.java.result("pg1").set("frametype", "spatial")
    model.java.result("pg1").feature("mslc1").set("smooth", "internal")
    model.java.result("pg1").feature("mslc1").set("resolution", "normal")
    model.java.result("pg2").label("Polarization Plot (ewfd)")
    model.java.result("pg2").set("looplevelinput", ["manual"])
    model.java.result("pg2").set("titletype", "manual")
    model.java.result("pg2").set("title", "Polarization states, Color: Phase (Radians)")
    model.java.result("pg2").feature("plz1").set("linewidth", Integer(2))
    model.java.result("pg2").feature("plz1").set("linewidthslider", Integer(2))
    model.java.result("pg2").feature("plz1").set("legend", JBoolean(True))
    model.java.result("pg2").feature("plz1").set("legendmethod", "manual")
    model.java.result("pg2").feature("plz1").set("legends", ["Reflection"])
    model.java.result("pg2").feature("plz2").set("linestyle", "dashed")
    model.java.result("pg2").feature("plz2").set("linewidth", Integer(2))
    model.java.result("pg2").feature("plz2").set("linewidthslider", Integer(2))
    model.java.result("pg2").feature("plz2").set("legend", JBoolean(True))
    model.java.result("pg2").feature("plz2").set("legendmethod", "manual")
    model.java.result("pg2").feature("plz2").set("legends", ["Transmission"])
    model.java.result("pg3").label("Electric Field (ewfd2)")
    model.java.result("pg3").set("frametype", "spatial")
    model.java.result("pg3").feature("mslc1").set("smooth", "internal")
    model.java.result("pg3").feature("mslc1").set("resolution", "normal")

    # Post

    model.java.result().numerical("int1").label("LightToHeat")
    # model.java.result().numerical("int1").set("table", "tbl13")
    model.java.result().numerical("int1").set("expr", ["ewfd2.Qh/(I0*w*w)"])
    model.java.result().numerical("int1").set("unit", ["1"])
    model.java.result().numerical("int1").set("descr", [""])
    model.java.result().numerical("int1").setResult()
    model.java.result("pg1").feature("surf1").set("resolution", mesh_resolution)

    print("Running study...")
    # model.java.study("std1").run()

    if model_path:
        model.save(model_path)

    print(model.java.result().numerical("int1").computeResult()[0][0][0])
    printElapsedTime(startTime, "finish")

    return float(model.java.result().numerical("int1").computeResult()[0][0][0])
