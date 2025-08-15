# Stack-Tox: Molecular Toxicity Prediction

Stack-Tox is a machine learning-based tool for predicting the toxicity of molecules from their SMILES notation using a stacking ensemble model.

## Requirements
- Python 3.8+
- Git
- pip (Python package manager)

## Installation

### 1. Clone the Repository
Open a terminal/command prompt and run:
```bash
git clone https://github.com/rpaduri/Stack-Tox.git
cd Stack-Tox
```
### 2. Install requirements
```bash
pip install -r requirements.txt
```
### 3. Install RDKit

RDKit is essential for calculating molecular descriptors. You can do this in the following ways:

Using pip

```bash
pip install rdkit-pypi
```
Altenatively use conda environment

```bash
conda create -n moldesc python=3.9 -y
conda activate moldesc
conda install -c conda-forge rdkit -y
```
### Usage
#### Option 1: Predict from a SMILES String

Run the script with a single SMILES input:
```bash
python stack-tox.py "CCO"
```

Example:
```
python stack-tox.py "C1=CC=CC=C1"
```

Here, "C1=CC=CC=C1" is the SMILES string for benzene.

#### Option 2: Predict from a .smi File

You can also provide a file containing SMILES strings (one per line):
```bash
python stack-tox.py molecules.smi
```

Example molecules.smi file:
```txt
CCO
C1=CC=CC=C1
O=C=O
```
### Output

The script will display predicted labels (e.g., Toxic or Non-Toxic) for each molecule.

If using a .smi file, it will output predictions for all molecules in the file.

### Example Run
```bash
python stack-tox.py "O=C=O"
```

Output:
``` bash
Molecule: O=C=O → Prediction: Non-Toxic
```
#### Notes

Ensure your SMILES input is valid.

The model is pre-trained; no training is required by the user.

Prediction speed depends on the number of molecules.
