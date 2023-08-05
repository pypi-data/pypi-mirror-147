def run():
    from .. import pyftc
    import pandas as pd
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt
    import os
    import pkg_resources

    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    #file = pkg_resources.resource_string(__name__, "test.rpc")
    file = os.path.join(os.path.dirname(__file__), "data", "test.rpc")
    print(f"Loading: {os.path.basename(file)}\n")

    x = pyftc.acq_load(file)
    print("\n", flush=True)

    # Build pandas data frame
    df_data = {}
    df_units = {}
    for ch in x["Info"]:
        df_data[ch["Name"]] = x[ch["Alias"]]["Data"]
        df_units[ch["Name"]] = x[ch["Alias"]]["Unit"]

    # Build xarray
    arr = xr.DataArray(df_data)
    arr.attrs["units"] = df_units
    arr.attrs["info"] = x["Info"]

    # Data frame
    fs = x["fs"]["Data"]
    df_data["t"] = x["t"]["Data"]
    df_data = pd.DataFrame(df_data)
    df_data = df_data.set_index("t")
    # Info frame
    df_info = pd.DataFrame(x["Info"])
    df_info = df_info.set_index("Name")

    df_data.attrs["info"] = x["Info"]

    print(df_data.describe())
    print(df_data.attrs)
    print("\n")
    print(df_info)
    print("\n", flush=True)

    srs = pyftc.srs(df_data.index.to_numpy(), df_data["signal"].to_numpy(),
        f_start=3, f_end=fs / 2, damp=0.05, f_step=-1.05, f_clamped=False, threads=6)
    #print(srs, fs)

    plt.figure()
    plt.plot(srs["metrics"][0], srs["metrics"][9])
    plt.xscale("log")
    plt.yscale("log")
    plt.grid()
    plt.title("FRS")

    plt.figure()
    plt.plot(srs["metrics"][0], srs["metrics"][3])
    plt.xscale("log")
    plt.yscale("log")
    plt.grid()
    plt.title("SRS [m/s²]")

    plt.figure()
    plt.plot(srs["metrics"][0], np.abs(srs["metrics"][7]), "b-")
    plt.plot(srs["metrics"][0], np.abs(srs["metrics"][8]), "g-")
    plt.plot(srs["metrics"][0], np.max(np.array([np.abs(srs["metrics"][7]), 
        np.abs(srs["metrics"][8])]), axis=0), "r--")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid()
    plt.title("SRS [mm]")

    plt.show()

