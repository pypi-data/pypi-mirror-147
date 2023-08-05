def run():
    from .. import pyftc
    import pandas as pd
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

    x = pyftc.acq_load(file, flagPsd=1, timeFirst=900, timeLast=1100)
    print("\n", flush=True)

    # Build pandas data frame
    df_data = {}
    for ch in x["Info"]:
        df_data[ch["Name"]] = x[ch["Alias"]]["Data"]

    # Data frame
    df_data["t"] = x["t"]["Data"]
    df_data = pd.DataFrame(df_data)
    df_data = df_data.set_index("t")
    # Info frame
    df_info = pd.DataFrame(x["Info"])
    df_info = df_info.set_index("Name")

    print(df_data.describe())
    print("\n")
    print(df_info)
    print("\n", flush=True)

    n = 2
    df_data.iloc[:, :n].plot(lw=0.5)
    units = set()
    for i, key in enumerate(x.keys()):
        units.add(x[key]["Unit"])
        if i >= n:
            break
    plt.ylabel(f"{', '.join(units)}")

    ch = list(x.keys())[0]
    if "Psd" in x[ch].keys():
        plt.figure()
        plt.plot(x[ch]["Psd"][0, :], x[ch]["Psd"][1, :])
        plt.xlabel("f [Hz]")
        plt.ylabel(f"PSD ({x[ch]['Unit']})²/Hz")
        plt.yscale("log")

    plt.show()
