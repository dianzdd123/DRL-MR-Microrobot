# Reusing DRL-MR-Microrobot

Magnetic microrobot navigation and mixed-reality teleoperation.

**Current scope:** Research scripts across Unity, Isaac Sim and image-based environments; there is no single installation command.

This repository is a fork of [YudongMao/DRL-MR-Microrobot](https://github.com/YudongMao/DRL-MR-Microrobot). Original authorship, citations and upstream notices are retained. Changes here apply to this fork.

## Choose a component first

| Component | Location | Extra requirements |
|---|---|---|
| Mixed-reality interface | `Mixed Reality/Unity/` | Unity, MRTK, HoloLens 2; supplied scene and C# assets |
| Manipulator communication | `Mixed Reality/Sensapex/` | Sensapex devices, driver and calibrated travel limits |
| Camera feedback | `Mixed Reality/Unity/camera_image_processing/` | OpenCV, camera and pixel-to-world calibration |
| Isaac Sim navigation | `Reinforcement Learning/Isaac Sim/` | Matching Isaac Sim runtime, scene assets and algorithm dependencies |
| Image-based navigation | `Reinforcement Learning/image-based/` | Grid maps, algorithm dependencies; some scripts also connect to hardware |

## Local inspection

```bash
python scripts/check_repository.py
```

This checks Python syntax without importing simulator packages or opening devices. There is no complete pinned environment in the public snapshot. The README records historical dependency versions; it does not establish compatibility with a current Isaac Sim installation. Use the simulator's Python environment for its scripts and retain a record of the exact working versions.

Paths contain spaces: quote them in shell commands. The PPO training file is `Reinforcement Learning/Isaac Sim/PPO/ppo.py`. Its sibling imports resolve when run from its own directory, but scene, output and network paths still require configuration.

## Inputs, outputs and adaptation

Inspect `TCPSend.cs`, the receiver/sender scripts and the selected algorithm's environment before running. Set matching host addresses, ports, units and coordinate conventions on both ends. Replace experiment-specific paths with local scene, map and checkpoint paths. The supplied `discrete_grid_map.npy` files are environment inputs; they do not encode your camera calibration.

Learning scripts produce models, logs and plots according to their embedded paths. The real-environment and Sensapex scripts can move hardware; a syntax check is not a dry run. Establish a calibrated workspace and a stop procedure before enabling device communication.

## Reproducibility

Record scene/map version, algorithm, seed, reward definition, simulator version, action scaling and camera calibration. Evaluate navigation separately from the mixed-reality interface before combining them. Unity project settings and all external simulator assets are not supplied as a complete turnkey project. The reported research setup needs reconstruction and validation on the target system.

## Attribution and reuse permissions

No repository-wide licence file is included in this checkout. Confirm reuse and redistribution permissions with the relevant rights holders; this maintenance update does not add a licence or relicense upstream code, data or assets.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the local workflow and what to include with a proposed change.
