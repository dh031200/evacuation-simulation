# Evacuation-Simulation

[![PyPI - Version](https://img.shields.io/pypi/v/evacuation-simulation.svg)](https://pypi.org/project/evacuation-simulation)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/evacuation-simulation.svg)](https://pypi.org/project/evacuation-simulation)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install evacuation-simulation
```

## License

`evacuation-simulation` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## todo

1. In order to calculate the space occupancy rate, the ratio of the total number of spaces (0) that can be moved every
   30 seconds (150 frames) is obtained, and the graph representation and the result value are derived in the form of a
   result. (accuracy_rate.jpg, accruity_rate.csv)   
   1.1 공간 점유율을 계산하기 위해 30초(150frame)마다 전체 이동할 수 있는 공간 수(0)중에서 실제 공간이 점유 된 공간(2)의 비율을 구하고 그래프 표현, 결과값을 형태로 도출한다.(
   occupancy_rate.jpg, occupancy_rate.csv )

2. Save the simulation video (Simulation_scen1_2f, Simulation_scen1_3f, Simulation_scen2_2f, Simulation_scen2_3f)    
   2.1 시뮬레이션 동영상을 저장한다.(Simulation_scen1_2f,Simulation_scen1_3f,Simulation_scen2_2f,Simulation_scen2_3f)

3. During the simulation, a heat map is displayed on the simulation screen showing cases where it is impossible to move
   due to a large crowd (except when it arrives at the destination).    
   3.1 시뮬레이션 중 사람이 많이 몰려 이동이 불가능한 경우(도착지에 도착한 경우 제외)를 보여주는 히트맵을 시뮬레이션 화면에 표시한다.