#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --mem=10GB
#SBATCH --gres=gpu
#SBATCH --job-name=oracle

module purge

singularity exec --nv \
            --overlay /scratch/yl5680/uncentainty-driven.ext3:rw \
            /scratch/work/public/singularity/cuda11.6.124-cudnn8.4.0.27-devel-ubuntu20.04.4.sif \
            /bin/bash -c "source /ext3/env.sh; conda activate uncentainty-driven; cd Uncertainty-Driven-Active-Vision/2D; git pull; python train.py --reset --config ../configs/ABC_2D.yml"

