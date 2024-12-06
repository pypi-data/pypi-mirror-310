import os
import numpy as np


keywords = {
            'm_r': 27,
            'm_nmPerCount': 24,
            'm_theta': 31,
            'm_moap': 30
            }


def read_pli(path: str, ishape: tuple | np.ndarray = (1024, 1392)):
    """
    Load retardance and azimuth data from Abrio(tm) .pli file

    Parameters
    ----------
    path : str
        Path to .pli file.
    ishape : tuple of int or ndarray, optional
        Image shape. Default is 1024 rows and 1392 columns.

    Returns
    -------
    tuple
        Two arrays with shape 'ishape': retardance and azimuth data.

    Raises
    ------
    ValueError
        If file extension is not '.pli'.
    KeyError
        If any of keywords not found in file. Keywords are: 'm_r', 'm_nmPerCount', 'm_theta' and 'm_moap'.

    """
    ext = os.path.splitext(path)[-1].lower()
    if ext != '.pli':
        raise ValueError(f'File has wrong extension: {ext}.')

    with open(path, 'rb') as pli:
        distances = []
        stream = pli.read()
        for key, d in keywords.items():
            ind = stream.find(key.encode('utf-8'))
            distances.append((key, ind + d))

            if ind == -1:
                raise KeyError(f"Keyword '{key}' is not found in file")

        distances = dict(distances)

        # Retardance nm per count
        pli.seek(distances['m_nmPerCount'])
        count = pli.read(4)
        count = np.frombuffer(count, dtype=np.float32)

        # Retardance image
        pli.seek(distances['m_r'])
        ret = pli.read(np.prod(ishape) * 2)
        ret = np.frombuffer(ret, dtype=np.uint16)
        ret = np.reshape(ret, ishape)
        ret = ret * count

        # Azimuth image
        pli.seek(distances['m_theta'])
        az = pli.read(np.prod(ishape) * 2)
        az = np.frombuffer(az, dtype=np.uint16)
        az = np.reshape(az, ishape)

    return ret, az
