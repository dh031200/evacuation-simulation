import cv2
import numpy as np

from .agent import Agent
from .envrionment import Environment


def show(name, _map):
    h, w = _map.shape
    v_map = np.full((h, w, 3), (0, 0, 0), dtype=np.uint8)
    v_map[_map == -1] = (255, 255, 255)
    v_map[_map == -2] = (0, 0, 255)
    v_map[_map == 0] = (0, 255, 0)
    v_map[_map == 2] = (255, 0, 0)

    cv2.imshow(name, v_map)
    cv2.waitKey(1)


def wait():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def destroy():
    cv2.destroyAllWindows()


__all__ = 'Agent', 'Environment', 'show', 'wait', 'destroy'
