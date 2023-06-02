import cv2
import numpy as np

from .agent import Agent, AgentPool
from .envrionment import Environment


def show(name, __map, pool):
    _map = __map.copy()
    for _agent in pool:
        for row, col in _agent.location:
            _map[row, col] = 3

    _map = np.repeat(_map, repeats=2, axis=1)
    _map = np.repeat(_map, repeats=2, axis=0)

    h, w = _map.shape

    v_map = np.full((h, w, 3), (0, 0, 0), dtype=np.uint8)
    # v_map[_map == -1] = (255, 255, 255)
    v_map[_map == -2] = (0, 255, 0)
    v_map[_map == 0] = (255, 255, 255)
    v_map[_map == 2] = (255, 0, 0)
    v_map[_map == 3] = (0, 0, 255)

    cv2.imshow(name, v_map)
    cv2.waitKey(1)


def wait():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def destroy():
    cv2.destroyAllWindows()


__all__ = 'Agent', 'AgentPool', 'Environment', 'show', 'wait', 'destroy'
