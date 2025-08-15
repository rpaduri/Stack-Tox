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

### Usage

Run the script with a single SMILES input:
```bash
python stack-tox.py "CCO"
```

Example:
```
python stack-tox.py "C1=CC=CC=C1"
```

Here, "C1=CC=CC=C1" is the SMILES string for benzene.

### Output

The script will display predicted labels (e.g., Toxic or Non-Toxic) for each molecule.

### Example Run
```bash
python stack-tox.py "O=C=O"
```

Output:
``` bash
Molecule: O=C=O → Prediction: Non-Toxic
```
### Notes

- Ensure your SMILES input is valid.
- The model is pre-trained; no training is required by the user.
- Prediction speed depends on the number of molecules.
-  If you are facing problems with rdkit installation, refer to https://pypi.org/project/rdkit-pypi/
