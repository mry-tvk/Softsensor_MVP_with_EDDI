Placeholder for using azua code base for multivariate timeseries missing value imputation/preprocessing.

# Preparation
- The first step is to clone the azua package using the following command in notebook:

!git clone https://github.com/microsoft/project-azua.git

or without "!" on your terminal.

- In terminal, change your directory to project-azua if you are not there already, and follow these steps to create an environment with the proper dependencies:

A) Run these commands:

conda env create -f environment.yml

conda activate project-azua

conda install -y pip

conda install -y ipykernel

B) if you are on Azure notebook run the following command, too:

python -m ipykernel install --user --name project-azua --display-name "(project-azua)"

- On your Azure notebook, on the kernel list, you can now see the (project-azua) name. Select that as your kernel.
[read more: https://medium.com/analytics-vidhya/how-to-create-virtual-environments-in-azure-ml-workspace-in-azure-portal-39245a34b370#:~:text=Step%201%3A%20Login%20to%20Azure%20ML%20studio%20and,following%20to%20create%20a%20new%20environment%20called%20newenvtf.]