# Reinforcement Learning Navigation and Mixed Reality Operation for Magnetic Micro-Robots

**MSEI Lab:** [Website](https://zhangrobotics.com/msei_website/) · [Website on GitHub](https://github.com/dianzdd123/msei_website)

## Start here

**Repository:** [dianzdd123/DRL-MR-Microrobot](https://github.com/dianzdd123/DRL-MR-Microrobot)

This repository is a fork of [YudongMao/DRL-MR-Microrobot](https://github.com/YudongMao/DRL-MR-Microrobot). Original authorship, citations and upstream notices are retained. Changes here apply to this fork.

**Scope:** Research scripts across Unity, Isaac Sim and image-based environments; there is no single installation command.

| Need | Where to start |
|---|---|
| Setup, file map, inputs/outputs and troubleshooting | [Reuse guide](docs/REUSE.md) |
| Local structural validation | `python scripts/check_repository.py` (Python 3.10+) |
| Proposed fixes and reproducibility details | [Contributing](CONTRIBUTING.md) |

The structural check does not run experiments or certify hardware, model accuracy or dependency compatibility. Reuse permissions need clarification: this checkout has no repository-wide licence file.


This repository contains the code for remote operation of micro-robots using HOLOLENS 2, developed on the Unity platform, as well as reinforcement learning navigation code for micro-robots in Isaac Sim and custom simulation environments.

# Overview

Magnetic micro-robots have demonstrated immense potential in biomedical applications such as in vivo drug delivery, non-invasive diagnostics, and cell-based therapies, owing to their precise maneuverability and small size. However, current micromanipulation techniques often rely solely on a limited two-dimensional (2D) microscopic view as sensory feedback. Traditional control interfaces do not provide an intuitive means for operators to manipulate micro-robots. 

To address these challenges, we propose a Deep Reinforcement Learning-Based Semi-Autonomous Control (DRL-SC) framework for magnetic micro-robot navigation in a simulated microvascular system. The operator is augmented with immersive teleoperation to enhance the efficiency of control and reduce operator workload. Our framework integrates Mixed Reality (MR) to provide immersive visualization, thereby enhancing situational awareness and control precision. 

# Installation

1. This experiment is developed based on the Unity Mixed Reality Toolkit. The official website provides detailed installation guidance
   https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/?view=mrtkunity-2022-05

2. The Micro-manipulator uses Sensapex devices  
   `pip install sensapex`

   Other installation links can be found on Sensapex's GitHub  
   https://github.com/sensapex/sensapex-py.git

3. Magnetic field and force calculations in this experiment use the Magpylib library  
   `pip install magpylib`

4. The reinforcement learning navigation task implemented in the Isaac Sim environment uses PyTorch 1.12.1, including DQN and DDPG

   `pip install torch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 --index-url https://download.pytorch.org/whl/cpu`

   Additional algorithms are implemented with Stable Baselines3 2.3.2, including PPO, A2C, SAC, and TD3  
   `pip install stable-baselines3==2.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple`

# Mixed Reality Teleoperation
This experiment uses Hololens 2 for immersive teleoperation, with TCP communication protocol for inter-device communication.

## Hololens 2 Reads Finger Position and Sends Incremental Positions to Micro-manipulator

`./Mixed Reality/Unity/TCPSend.cs` is a script for sending hand tracking data from Microsoft Mixed Reality Toolkit (MRTK). It sends cumulative displacement data of the fingertip of the index finger via TCP protocol to a specified IP address and port. Suitable for real-time transmission of hand tracking data in mixed reality applications.

Features  
- Real-time tracking of the position of the right-hand index fingertip.  
- Calculates displacement increments of the fingertip and accumulates total displacement.  
- Sends cumulative displacement data via TCP protocol at fixed intervals (default 0.1 seconds).  
- Supports MRTK's hand joint event handling.

2. Run  
Add the script to the GameObject, and when the Unity project is started, the script will automatically connect to the specified TCP server.

3. The Sensapex Micro-manipulator accepts the position increment and controls the micro-robot's movement via the magnetic field, implemented in 
`./Mixed Reality/Sensapex`

## Microscope Identifies Micro-Robot Position and Performs Image Processing

Using HSV thresholding to identify the micro-robot and perform positional transformations to get the robot's location  
`./Mixed Reality/Unity/camera_image_processing/small_maze.py` is an OpenCV-based sphere detection and position mapping program.  
It captures video frames in real-time through the camera, detects the position of the spheres in the frame, and maps the pixel coordinates of the spheres to spatial coordinates. Suitable for applications that need real-time detection and mapping of spheres to actual space.

Features  
- Sphere detection:  
  Uses HSV color space and contour detection algorithms to identify spheres in the frame.  
  Filters out contours that do not meet circularity criteria.  
  Draws bounding boxes and contours of spheres in the frame.  

- Position mapping:  
  Maps the pixel coordinates of the sphere to spatial coordinates.  
  Supports customizable mapping areas and spatial ranges.  

- Position jump filtering:  
  Filters out detection results with excessive positional jumps, ensuring the stability of position data.

## Build Digital Twin of the System in Unity

The recognized position of the micro-robot, along with the current micro-manipulator information, is sent back to Unity via TCP and used to build the system's digital twin with C# scripts.  
This is implemented with the following scripts  
`./Mixed Reality/Unity/MoveX_RealRobot.cs`  
`./Mixed Reality/Unity/MoveY_RealRobot.cs`  
`./Mixed Reality/Unity/MoveZ_RealRobot.cs`  
`./Mixed Reality/Unity/BallPositionReceiver.cs`

# Isaac Sim-based Reinforcement Learning Navigation 
The paper uses a custom environment based on images, but the process is the same and will not be repeated

## Standalone Environment Design
The maze environment based on Omniverse Isaac Sim is used for reinforcement learning tasks. The environment includes a controllable magnet (Agent) and a micro-robot (Target). The agent must use continuous actions to control the micro-robot and push it to a designated position. The environment supports GPU-accelerated physics simulation and provides rich observation and reward signals.

Features  
- Physics Simulation:  
  High-precision physics simulation with Omniverse Isaac Sim.  
  GPU-accelerated dynamics and collision detection.

- Action Space:  
  The agent controls the movement of the micro-robot via a 2D action space.

- Observation Space:  
  The observation space includes the positions of the agent and the micro-robot.

- Reward Mechanism:  
  Rewards are calculated based on the distance between the agent and the target, collision count, and step count.

- Task Goal:  
  Push the micro-robot to a specified region.

## Model Training
For example, using the PPO algorithm in Isaac Sim:  
This is a reinforcement learning project that uses the Proximal Policy Optimization (PPO) algorithm to train the maze environment. The project is based on Stable-Baselines3, supports GPU-accelerated training, and provides rich callback functionalities, including dynamic entropy coefficient adjustment, model saving, training log recording, and training result visualization.

```python
policy_kwargs = {
    'net_arch': [256, 128, 128, 16],  # Hidden layers architecture
    'activation_fn': nn.Tanh,         # Activation function
    'ortho_init': True,               # Orthogonal initialization
    'log_std_init': -10,              # Initial log standard deviation
    'full_std': True,                 # Full standard deviation
    'use_expln': False,               # Do not use exponential linear unit
    'squash_output': False,           # Do not squash output
    'normalize_images': True,         # Normalize input images
    'features_extractor_kwargs': {},  # Additional parameters for the feature extractor
    'share_features_extractor': True, # Share the feature extractor
    'optimizer_kwargs': {}            # Additional parameters for the optimizer
}

ppo_params = {
    'learning_rate': 3e-4,  # 可以尝试降低学习率，例如1e-4
    'n_steps': 2048,  # 可以减少步数，例如2048
    'batch_size': 128,  # 可以尝试减小批量大小，例如512
    'n_epochs': 10,  # 可以减少训练的epoch数，例如10
    'gamma': 0.99,
    'gae_lambda': 0.95,
    'clip_range': 0.2,  # 可以尝试减小clip范围，例如0.1
    'clip_range_vf': None,
    'normalize_advantage': True,
    'ent_coef': 0.001,  # 可以减小熵系数，例如0.01
    'vf_coef': 0.5,
    'max_grad_norm': 0.5,
    'use_sde': False,
    'sde_sample_freq': 4,
    'rollout_buffer_class': None,
    'rollout_buffer_kwargs': None,
    'target_kl': None,
    'stats_window_size': 100,
    'tensorboard_log': tensorboard_log,
    'policy_kwargs': {
        'net_arch': [256,128,128,16],
        'activation_fn': nn.Tanh,
        'ortho_init': True,
        'log_std_init':-10,
        'full_std': True,
        'use_expln': False,
        'squash_output': False,
        # 'features_extractor_class': FlattenExtractor,
        'features_extractor_kwargs': {},
        'share_features_extractor': True,
        'normalize_images': True,
        # 'optimizer_class': torch.optim.Adam,
        'optimizer_kwargs': {}
    },
    'verbose': 1,
    'seed': None,
    'device': 'cuda',
    '_init_setup_model': True
}
```

Training  
Run from the algorithm directory after configuring its scene paths:

```bash
cd "Reinforcement Learning/Isaac Sim/PPO"
python ppo.py
```

# Future Work

The DRL-SC framework has considerable limitations. The navigation experiments for magnetic micro-robots were conducted in a 2D environment, and further testing is required to evaluate the framework’s applicability and effectiveness in more complex three-dimensional environments and under real physiological conditions. Additionally, the small number of participants limited the sample size, so expanding the sample size is necessary to validate the generalizability of the current findings.

Future work will focus on extending the DRL-SC framework to 3D microfluidic systems with more complex microvascular structures. Additionally, its performance will be assessed in biofluidic environments to further validate its effectiveness and adaptability.
