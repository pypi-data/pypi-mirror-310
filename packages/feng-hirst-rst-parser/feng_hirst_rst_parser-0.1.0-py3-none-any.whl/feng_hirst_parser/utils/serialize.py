import os.path
import pickle

from feng_hirst_parser.utils.paths import save_folder

SAVE_SUFFIX = ".dat"


def save_data(
        filename: str,
        myobject: object,
        where: str = save_folder,
        suffix: str = SAVE_SUFFIX
):
    with open(os.path.join(where, filename + suffix), "wb") as fo:
        pickle.dump(myobject, fo, protocol=pickle.HIGHEST_PROTOCOL)


def load_data(
        filename: str,
        where: str = save_folder,
        suffix: str = SAVE_SUFFIX
):
    data_file = os.path.join(where, filename + suffix)

    with open(data_file, "rb") as fo:
        return pickle.load(fo)
