# BahiaRT-GYM
 The BahiaRT-GYM is a toolkit for developing OpenAI-Gym environments that can be directly used alongside the RCSSSERVER3D simulator with NAO agents.
 We primarily aim to ease the development of machine learning solutions for all the teams participating on the RoboCup 3D soccer league by creating a tool that can be used with any type of coding language, since all of the connections here are TCP-based. Albeit, this toolkit can be easily adapted to work with any other type os simulator, as long as it sends and receives messages through TCP sockets.

## Processes architecture example

![Processes Architecture](./img/Processes_Architecture.png)

Here is a quick demonstration of what the processes architecture look like. As you can see by the green box, the BahiaRT-Gym is composed of an environment, either yours or the demo one already present on this repository, and a proxy. The latter is responsible to connect the agents to the server and relay the perceptions sent back from the server to the gym environment, besides returning those to the agents as expected.

## Requirements

 **1. Ubuntu 18.04**
 
 **2. Python 3.7**
 
 **3. OpenAI Gym package**
 
 **4. PyTorch**
 
 **5. Stable-Baselines3**

## Requirements details
 Stable-Baselines3 requires Python 3.7+ and PyTorch >= 1.8.1.
 As of today(April 5th, 2022), the most recent PyTorch version (1.11.0) does not support Python 3.8+, so we recommend keeping on Python 3.7.

## Python 3.7 installation and Virtual Environment(venv) creation
 To install the environment, we recommend using a python virtual environment(venv) in order to avoid any possible conflicts between libraries. The following tutorial explains how to install it using python 3.7

 1) Add python official repository and install 3.7:
   ```bash
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt install python3.7
   ```
 2) Create virtual environment:
   ```bash
   python3.7 -m venv venv
   ```

   This will create a 'venv' folder on the current path. If you want to change the folders name, simply alter the second "venv" on the command.

 3) Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

   Now you're in the python 3.7 venv. If you want to leave, simply type:
   ```bash
   deactivate
   ```
 4) Update pip inside the venv.
   ```bash
   pip install --upgrade pip
   ```
From now on, every pip or python command should be used inside the venv. This way, any installed library won't cause any conflicts with your system.

## Installing PyTorch

PyTorch's installation depends on your system's specifications.

If you use CUDA cores, the following command will install Torch 1.11.0 with support to CUDA 10.2 on linux using PiP:
```bash
   pip install torch torchvision torchaudio
```
If you use CPU only, the command to install the same Torch version is the following:
```bash
   pip install torch==1.11.0+cpu torchvision==0.12.0+cpu torchaudio==0.11.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
```
If you're interested in Torch for different specifications, check the official website: https://pytorch.org/get-started/locally/

## Installing Gym and Stable-Baselines3

To install gym, use the following command:
```bash
   pip install gym
```
To install Stable-Baselines3, use the following command:
```bash
   pip install stable-baselines3[extra]
```
The [extra] version is quite usefull since it allows us to use things like tensorboard to monitor and evaluate the trained models.

## Cloning and installing the BahiaRT-Gym

### Option 1: Using PiP

To install the toolkit using pip simply make sure you have your venv activated and type the following on your terminal:
```bash
   pip install bahiart_gym
```

### Option 2: Using the source from the repository
To clone the repository, go to the same path where your 'venv' folder is located, then use the following command:
```bash
   git clone https://bitbucket.org/bahiart3d/bahiart-gym.git
```
Now your directory should look like this:
```
   your-folder/
    venv/
    bahiart-gym/
```
Now, inside the bahiart-gym folder, use the following command to install the package:
```bash
   pip install -e .
```
Now BahiaRT-Gym's package is installed and ready to use on your python's virtual environment.

## Testing the BahiaRT-GYM demo environment.
 On the "demo_test.py" file you can check an example script to test the toolkit using a demonstration environment, along with explanations of every line of code.

 Always remember to initiate the RCSSSERVER3D before running this script.

 Feel free to explore and modify those lines as you wish to experiment on the toolkit.

# Authors
 Gabriel Mascarenhas, Marco A. C. Simões, Rafael Fonseca

# Contact
teambahiart@gmail.com
