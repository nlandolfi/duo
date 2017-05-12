import numpy as np

norm = np.linalg.norm

def angle_between(v1, v2):
    if norm(v1) == 0 or norm(v2) == 0:
        return np.pi

    v1_u = v1 / norm(v1)
    v2_u = v2 / norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
