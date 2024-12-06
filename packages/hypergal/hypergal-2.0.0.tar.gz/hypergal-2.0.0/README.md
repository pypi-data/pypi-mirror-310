# HyperGal

Pipeline for supernovae extraction and classification within the SEDm/ZTF project. Please have a look at [the _HyperGal_ paper](https://arxiv.org/abs/2209.10882).

HyperGal is a fully chromatic scene modeler, which uses pre-transient photometric images to generate a hyperspectral model of the host galaxy; it is based on the CIGALE SED fitter used as a physically-motivated spectral interpolator. The galaxy model, complemented by a point source and a diffuse background component, is projected onto the SEDm spectro-spatial observation space and adjusted to observations

## Acknowledgement

This project has received funding from the Project IDEXLYON at the University of Lyon under the Investments for the Future Program (ANR-16-IDEX-0005), and from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement n°759194 - USNAC).

## References
If you are using HyperGal or a supernova spectrum obtained from it, please cite [the _HyperGal_ paper](https://arxiv.org/abs/2209.10882).
***

# Installation

Hypergal requires Cigale. Since you cannot simply `pip install cigale`
(but almost). Please follow these few lines of instruction.

1. Create a dedicated environment

```bash
conda create -n hypergal python=3.11
```
and "log" in.
```bash
conda activate hypergal
```

2. Install the basic python packages
```bash
conda install numpy scipy pandas matplotlib dask
```

3. Install the forge dependencies (sep may downgrade numpy < v.2, that is ok).
```bash
conda install -c conda-forge sep sncosmo astropy
```

4. Download Cigale and install it.

In doubt, please follow the specified Cigale instructions: [https://cigale.lam.fr/](cigale.lam.fr)
- Download the latest cigale from
  [here](https://gitlab.lam.fr/cigale/cigale/-/archive/v2022.1/cigale-v2022.1.tar.gz)
- uncompress the .tar.gz and go inside the cigale repo
```bash
pip install 
```
- and run (takes some time)
```bash
python setup.py build
```
and 
```bash
pip install .
```

5. Install hypergal
```bash
pip install hypergal
```

***
WARNING FOLLOWING INSTRUCTIONS ARE BEING UPDATED
***
instructions below could be deprecated. More to come

# Main script: ```run_hypergal.py```

### Target

One mandatory argument : the target (supernova) ``` -t``` .  
You can use the target name, for instance ```-t ZTF20abhrmxh``` : the corresponding data cube will be automatically downloaded if not available. 
Otherwise, you can directly give a cube path:
```-t /sps/ztf/data/sedm/redux/20200703/e3d_crr_b_ifu_20200703_09_58_56_ZTF20abhrmxh.fits```.

### Cluster environment

By default, a Dask ```LocalCluster``` is created with 10 workers, for a local use. If you use this pipeline with a specific job scheduler such as SGE or SLURM, you have to set the argument ``` --env SGE``` (or ``` --env SLURM```).
Number of workers can be set with ```-w```.

:warning: To submit a job in a SLURM or SGE environment, the **bash** script should be used. Please don't forget to change the ```run_hypergal.py``` absolute path in the ```run_hypergal.sh``` bash script.

### Some arguments

Many arguments can be added such as:
- the redshift ``` --redshift```, otherwise the one from Fritz is used;
- xy target position in the IFU ``` --xy```, otherwise an estimation is derived from the guiding camera data;
- If you only want to model the host component ``` --host_only```;
- If you only want to model the supernova ``` --sn_only```;
- (... see ```run_hypergal.py -h```)

### Run examples

Local:
``` 
run_hypergal.py -t ZTF20abhrmxh -w 6 --redshift 0.066 --xy 2.9 0.8
```
SLURM
``` 
sbatch run_hypergal.sh -t ZTF20abhrmxh --env SLURM -w 20 --redshift  0.066 --xy 2.9 0.8
```
SGE
``` 
qsubrun_hypergal.sh -t ZTF20abhrmxh --env SGE -w 20 --redshift  0.066 --xy 2.9 0.8
```
***
# From notebook
### Create the cluster
```python
# Local cluster
from dask.distributed import Client, LocalCluster

cluster = LocalCluster(n_workers=10, threads_per_worker=1)
client = Client(cluster)
```
```python
# SGE cluster
from dask.distributed import Client
from dask_jobqueue import SGECluster

cluster = SGECluster(name="dask-worker", walltime="12:00:00",
					 memory="4GB", death_timeout=240, project="P_ztf",
					 resource_spec="sps=1", local_directory="$TMPDIR",
					 cores=1, processes=1)
					 
cluster.scale(10) # How many workers?
client = Client(cluster)
```
```python
# SLURM cluster
from dask.distributed import Client
from dask_jobqueue import SLURMCluster

cluster = SLURMCluster(name="dask-worker", walltime="12:00:00",
					 memory="4GB", death_timeout=240, project="P_ztf",
					 log_directory="/sps/ztf/users/jlezmy/dask/logs", local_directory="$TMPDIR",
					 cores=1, processes=1, job_extra=["-L sps"])
					 
cluster.scale(10) # How many workers?
client = Client(cluster)
```

### Run
```python
from hypergal.script import daskbasics,scenemodel
to_stored = scenemodel.DaskScene.compute_targetcubes(name="ZTF20abhrmxh", client=client)
future = client.compute(to_stored)
```
> Note: By calling ```client```, you can access to the dask dashboard and check for the computation progress.
> Main results (model cubes, supernova+host spectra, fitted params) are stored in the same directory of the input cube file. Plots and ```logfile.yml``` are stored in ```cubepath/hypergal/targetname/```.

***
# Main HyperGal steps:

See library details [here](hypergal)
  
![](examples/Dag_hypergal.png)
***
# Dependencies

The following dependencies are automatically installed:

- _numpy_, _scipy_, _pandas_, _matpotlib_, _astropy_ (basic anaconda)
- _pysedm_ and its own dependencies (```pip install pysedm``` , see https://github.com/MickaelRigault/pysedm) 
- _ztfquery_ (```pip install ztfquery``` AND see https://github.com/MickaelRigault/ztfquery for path configuration) 
- _dask_ (```python -m pip install "dask[complete]"    # Install everything``` see https://docs.dask.org/en/stable/install.html) 
- _geopandas_ (```pip install geopandas``` ) 
- _iminuit_ (version<2.0 ```pip install iminuit<=2.0``` ) 
- _ztfimg_ (```pip install ztfimg``` see https://github.com/MickaelRigault/ztfimg)
- _Cigale_ (version 2020. The 2022 version should work too, but has not been tested. See https://cigale.lam.fr/download/ for installation)
