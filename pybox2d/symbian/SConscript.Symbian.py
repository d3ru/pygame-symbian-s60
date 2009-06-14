from scons_symbian import *

import platform

PACKAGE = "Box2D"

src = Glob('../Box2D/Collision/*.cpp')
src += Glob('../Box2D/Collision/Shapes/*.cpp')
src += Glob('../Box2D/Common/*.cpp')
src += Glob('../Box2D/Dynamics/*.cpp')
src += Glob('../Box2D/Dynamics/Contacts/*.cpp')
src += Glob('../Box2D/Dynamics/Controllers/*.cpp')
src += Glob('../Box2D/Dynamics/Joints/*.cpp')
src += Glob('../Box2D/*.cpp')
src += [ "cppwrap.cpp"]

inc = [ join( EPOC32_INCLUDE, "stdapis" ),
        join( EPOC32_INCLUDE, "stdapis", "stlport" ),
        join( EPOC32_INCLUDE, "python25" ),
        "../",
        "../Box2D/",
        "../Box2D/Collision",
        "../Box2D/Collision/Shapes",
        "../Box2D/Common",
                "../Box2D/Dynamics",
                "../Box2D/Dynamics/Contacts",
                "../Box2D/Dynamics/Controllers",
                "../Box2D/Dynamics/Joints",
                ]

if COMPILER == COMPILER_GCCE:
    definput = "kf__Box2D.def"
else:
    definput = None

SymbianProgram( "kf__Box2D", TARGETTYPE_PYD,
                sources = src, 
                includes = inc,
                gcce_options   = "-Wall -Wno-unused",
                winscw_options = "-wchar_t on",
                # libstdcpp. crashes on device
                libraries      = [ "python25", "libc", "libm", #"libstdcpp", 
                                    "euser", 
                                    #"logman",
                                    ],
                package        = PACKAGE,
                definput       = definput,
                elf2e32_args   = "--ignorenoncallable", # Get the .pyd init only
                defines        = ["_WCHAR_T_DECLARED"],
                uid3 = 0xebd8fcbd,
                mmpexport = "box2d.mmp"
                )

ToPackage( package = PACKAGE, source = "../__init__.py", target = "data/pygame/libs/Box2D" )
ToPackage( package = PACKAGE, source = "../Box2D.py", target = "data/pygame/libs/Box2D" )

SymbianPackage( PACKAGE, ensymbleargs = {} )

