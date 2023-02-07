## Trajectory Policy Guidances for NeRF Rendering

This repository contains the code for implementing trajectory policy for 2D NeRF rendering. The baseline codes are from Uncertain-Driven Active Vision, and we have add trajectory policy as our main contribution. 

### Reconstruction Model

#### Inputs: around 1k objects with 1-5 views each, plus voxels for validation, configs

#### Outputs: an oracle model that predicts the occupancy of object views

With regards to how to train a reconstruction model as an oracle, please refer to the original repository and follow the README.md instructions there. 

For a quick example, you can train a 2D reconstruction model by calling 
```
$ python train.py --reset --config ../configs/ABC_2D.yml
```
where the config file provided can be updated to specify further training and model details. By default this trains with 1 to 5 input images. But we are trying to grow the number of input images to 10.

### Trajectory Policy

1. this line generates the guided trajectory under the folder '{object_name}_{today}', this data is sufficient for task/motion planner

Inputs: configs, oracle model, object filepath

Outputs: {object_name}_{today}

```
python policy_evaluator.py --policy_config ../configs/ABC_2D_NBV.yml
```


2. this line import/render the actual model and interpolate the trajectory to generate data for training NeRF

Inputs: {object_name}_{today}, the object filepath '*.obj'. 

Outputs: nerf_data_{today}

```
python trajectory_data_gen.py
```

3. Optional: this line plot the trajectory and visualize in matplotlib

Inputs: {object_name}_{today}

Outputs: matplotlib plot

```
python trajectory_plot.py
```