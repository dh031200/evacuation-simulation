import cv2
import numpy as np

from .agent import Agent, AgentPool
from .envrionment import Environment


def show(name, __map, pool, writer):
    _map = __map.copy()
    for _agent in pool:
        for row, col in _agent.location:
            _map[row, col] = 3

    _map = np.repeat(_map, repeats=2, axis=1)
    _map = np.repeat(_map, repeats=2, axis=0)

    h, w = _map.shape

    v_map = np.full((h, w, 3), (255, 255, 255), dtype=np.uint8)
    # v_map[_map == -1] = (255, 255, 255)
    v_map[_map == 0] = (0, 255, 0)
    v_map[_map == -2] = (0, 0, 255)
    v_map[_map == -3] = (255, 0, 0)
    v_map[_map > 0] = (255, 0, 255)

    # print(v_map.shape)
    writer.write(v_map)
    cv2.imshow(name, v_map)
    cv2.waitKey(1)


def wait():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def destroy():
    cv2.destroyAllWindows()

def set_writer():
    return cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1594, 1054))

def release(writer):
    writer.release()



__all__ = 'Agent', 'AgentPool', 'Environment', 'show', 'wait', 'destroy', 'set_writer', 'release'
