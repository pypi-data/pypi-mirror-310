import os
import sys
import shutil
from matplotlib import get_configdir
from time import time
from . import styles
from .constants import DECIMALS
from .parameters import journals
from .figures import standard_figsize, standard_rect


def create_matplotlib_style(journal="PR", folder=""):
    """Creates a matplotlib style file in a given folder"""
    d = journals[journal]
    figsz = standard_figsize(journal)
    rect = standard_rect(journal)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(folder + "/{}.mplstyle".format(journal), "w") as f:
        f.write("figure.figsize : {},{}\n".format(*figsz))
        f.write("figure.subplot.left : {}\n".format(rect[0]))
        f.write("figure.subplot.bottom : {}\n".format(rect[1]))
        f.write(
            "figure.subplot.right : {}\n".format(round(rect[0] + rect[2], DECIMALS))
        )
        f.write("figure.subplot.top : {}\n".format(round(rect[1] + rect[3], DECIMALS)))
        try:
            for par in d["rcparameters"]:
                f.write("{} : {}\n".format(par, d["rcparameters"][par]))
        except Exception:
            pass


def diff_dic(dic1, dic2):
    """returns the dfference of two dictionaries as sorted set"""
    mismatch = sorted({key for key in dic1.keys() & dic2 if dic1[key] != dic2[key]})
    return mismatch


if __name__ == "__main__":
    sdir = styles.__path__[0]  # gets styles directory
    cdir = get_configdir()  # gets matplotlib config directory
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            """This script installs configuration styles in matplotlib config directory.
              
To remove configuration: 
1) Go to {cdir}, delete matplotlibrc file and reinstate the previous matplotlibrc file.
Files that have been substituted have been backupped by appending _backup_<time>.  
2) Go to {cdir}//stylelib and delete the undesired .mplstyle files.
The files created by this package are: 
{mplfiles}
3) pip uninstall journal-styles
              
Options:
    install     Installs matplolib styles in matplotlib config directory. Old files are backupped.
    update-styles   Updates the stylefiles in the internal package directory and copies them to 
                    the matplotlib config directory.""".format(
                cdir=cdir,
                mplfiles="".join(
                    ["\n" + f for f in os.listdir(sdir) if f[-8:] == "mplstyle"]
                ),
            )
        )

    elif sys.argv[1] == "install":
        # backup matplotlibrc if present
        if os.path.exists(cdir + "//matplotlibrc"):
            shutil.copy(
                cdir + "//matplotlibrc",
                cdir + "//matplotlibrc_backup_{}".format(time()),
            )
        # substitute matplotlibrc
        shutil.copy(sdir + "//matplotlibrc", cdir + "//matplotlibrc")
        # update styles in local folder
        for journal in journals:
            create_matplotlib_style(journal=journal, folder=sdir)
        # create styles directory if neeeded
        if not os.path.exists(cdir + "//stylelib"):
            os.makedirs(cdir + "//stylelib")
        # copy all the mplstyle into matploltib config directory backupping old files
        for f in os.listdir(sdir):
            if f[-8:] == "mplstyle":
                if os.path.exists(cdir + "//stylelib//{}".format(f)):
                    shutil.copy(
                        cdir + "//stylelib//{}".format(f),
                        cdir + "//stylelib//{}".format(f) + "_backup_{}".format(time()),
                    )
                shutil.copy(sdir + "//" + f, cdir + "//stylelib//{}".format(f))
        # line = "c.InlineBackend.rc = { }\n"
        # config_file = "{}/.ipython/profile_default/ipython_kernel_config.py".format(str(Path.home()))

    elif sys.argv[1] == "update-styles":
        # update styles in local folder
        for journal in journals:
            create_matplotlib_style(journal=journal, folder=sdir)
        # create styles directory if neeeded
        if not os.path.exists(cdir + "//stylelib"):
            os.makedirs(cdir + "//stylelib")
        # copy all the mplstyle into matploltib config directory backupping old files
        for f in os.listdir(sdir):
            if f[-8:] == "mplstyle":
                if os.path.exists(cdir + "//stylelib//{}".format(f)):
                    shutil.copy(
                        cdir + "//stylelib//{}".format(f),
                        cdir + "//stylelib//{}".format(f) + "_backup_{}".format(time()),
                    )
                shutil.copy(sdir + "//" + f, cdir + "//stylelib//{}".format(f))

    else:
        print("unkwnon option {}".format(sys.argv[1]))
