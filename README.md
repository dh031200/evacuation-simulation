# Evacuation-Simulation

[![PyPI - Version](https://img.shields.io/pypi/v/evacuation-simulation.svg)](https://pypi.org/project/evacuation-simulation)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/evacuation-simulation.svg)](https://pypi.org/project/evacuation-simulation)

-----


**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install git+https://github.com/dh031200/evacuation-simulation
```

## Map directory tree
```
Workspace
└ map
　 ├ 2f_grid_S_1.csv
　 ├ 2f_grid_S_2.csv
　 ├ 3f_grid_S_1.csv
　 └ 3f_grid_S_2.csv
```


## Usage

#### Arguments
* `--map_dir`, `-m` : map directory
* `--floor`, `-f` : floor for simulation
* `--scenario`, `-s` : scenario for simulation
* `--generate_frequency`, `-gf` : agent generate frequency (optional, default: 0.01)
  * `<<0-Less-------More-1>>`
* `--adult_kids_ratio`, `-akr` : agent adult-kids ratio (optional, default: 0.7)
  * `<<0-Kid-------Adult-1>>`
* `--random_move_ratio`, `-rmr` : agent random move ratio (optional, default: 0.2)
  * `<<0-Planned-------Random-1>>`
* `--remove_arrived_agents`, `-rma` : remove arrived agents (optional, default: True)

#### Command example
```bash
# 2층 1번 시나리오 [frequency: 0.01, 아이3:7어른, 도착한 에이전트 제거]
evacuation-simulation -m map -f 2 -s 2

# 2층 1번 시나리오 agent [frequency: 0.001, adult_kids_ratio:0.0(아이만), 도착한 에이전트 제거 하지 않음]
evacuation-simulation -m map -f 2 -s 2 -gf 0.001 -akr 0.0 -rmr False

# 2층 1번 시나리오 agent [frequency: 0.01, adult_kids_ratio:0.9(아이1:9어른), 도착한 에이전트 제거]
evacuation-simulation -m map -f 2 -s 2 -gf 0.01 -akr 0.9

# 3층 1번 시나리오 [frequency: 0.01, 아이3:7어른, 도착한 에이전트 제거]
evacuation-simulation -m map -f 3 -s 1

# 3층 2번 시나리오 [frequency: 0.01, 아이3:7어른, 도착한 에이전트 제거]
evacuation-simulation -m map -f 3 -s 2

```

## Result
### 2F 시나리오 2
|병목현상 히트맵|시뮬레이션|
|---|---|
|![image](https://github.com/dh031200/evacuation-simulation/assets/66017052/78717e91-a2c9-4880-9279-b6546396512a)|![image](https://github.com/dh031200/evacuation-simulation/assets/66017052/1bac3bc6-e5b3-45f4-bfe4-402c65fff941)|

|결과값|그래프|
|---|---|
|![2F_S_2_data](https://github.com/dh031200/evacuation-simulation/assets/66017052/2326b4f0-2ae3-48fd-be11-9667519f9808)|![2F_S_2_plot](https://github.com/dh031200/evacuation-simulation/assets/66017052/451514b0-20cb-4d08-abd2-0f7ed2af3818)|

## License

`evacuation-simulation` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## todo

1. In order to calculate the space occupancy rate, the ratio of the total number of spaces (0) that can be moved every
   30 seconds (150 frames) is obtained, and the graph representation and the result value are derived in the form of a
   result. (occupancy_rate.jpg, occupancy_rate.csv)
   1.1 공간 점유율을 계산하기 위해 30초(150frame)마다 전체 이동할 수 있는 공간 수(0)중에서 실제 공간이 점유 된 공간(2)의 비율을 구하고 그래프 표현, 결과값을 형태로 도출한다.(
   occupancy_rate.jpg, occupancy_rate.csv )

2. Save the simulation video (Simulation_scen1_2f, Simulation_scen1_3f, Simulation_scen2_2f, Simulation_scen2_3f)
   2.1 시뮬레이션 동영상을 저장한다.(Simulation_scen1_2f,Simulation_scen1_3f,Simulation_scen2_2f,Simulation_scen2_3f)

3. During the simulation, a heat map is displayed on the simulation screen showing cases where it is impossible to move
   due to a large crowd (except when it arrives at the destination).
   3.1 시뮬레이션 중 사람이 많이 몰려 이동이 불가능한 경우(도착지에 도착한 경우 제외)를 보여주는 히트맵을 시뮬레이션 화면에 표시한다.
