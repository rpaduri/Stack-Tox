#!/usr/bin/env python3
"""
stack-tox.py

Classify molecules as Toxic or Non-Toxic from SMILES notation.

Files required in working directory:
    model.pkl           : Trained stacking classifier
    scaler.pkl          : Fitted scaler
    imputer.pkl         : Fitted imputer
    descriptor_list.txt : Names of the 61 descriptors used in training (one per line)
"""

import sys
import joblib
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors


# ----------------------------
# Validate SMILES
# ----------------------------
def is_valid_smiles(smiles):
    return Chem.MolFromSmiles(smiles) is not None


# ----------------------------
# Calculate descriptors
# ----------------------------
def calculate_descriptors_verbose(smiles, descriptor_list):
    """Calculate RDKit descriptors with progress and warnings."""
    print("Parsing SMILES...")
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES provided.")

    print(f"Calculating {len(descriptor_list)} descriptors...")
    calculator = MoleculeDescriptors.MolecularDescriptorCalculator(descriptor_list)
    descriptors = list(calculator.CalcDescriptors(mol))

    # Find missing or infinite values
    missing_indices = [i for i, val in enumerate(descriptors)
                       if pd.isna(val) or np.isinf(val)]
    if missing_indices:
        print(f"Warning: {len(missing_indices)} descriptors could not be calculated: {missing_indices}")
    else:
        print("All descriptors calculated successfully.")

    # Small molecule warning
    atom_count = mol.GetNumAtoms()
    if atom_count <= 3:
        print(f"Warning: Molecule is very small ({atom_count} atoms). Prediction may be unreliable.")

    return descriptors, missing_indices


# ----------------------------
# Load model, scaler, imputer
# ----------------------------
def load_pipeline():
    try:
        model = joblib.load("stacking_clf_model.pkl")
        scaler = joblib.load("scaler.pkl")
        imputer = joblib.load("imputer.pkl")
        with open("descriptor_list.txt") as f:
            descriptor_list = [line.strip() for line in f]
        return model, scaler, imputer, descriptor_list
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Pipeline component missing: {e}")


# ----------------------------
# Preprocess descriptors
# ----------------------------
def preprocess_descriptors(descriptors, missing_indices, imputer, scaler):
    """Handle missing/inf values, impute, scale."""
    descriptors = np.array(descriptors, dtype=float).reshape(1, -1)
    descriptors = np.where(np.isinf(descriptors), np.nan, descriptors)

    if missing_indices:
        if len(missing_indices) > descriptors.shape[1] // 2:
            print("More than 50% descriptors missing — setting missing values to 0.")
            for idx in missing_indices:
                descriptors[0, idx] = 0
        else:
            print("Imputing missing descriptors...")
            descriptors = imputer.transform(descriptors)
    else:
        print("No missing descriptors, skipping imputation.")

    print("Scaling descriptors...")
    descriptors = scaler.transform(descriptors)
    return descriptors


# ----------------------------
# Predict toxicity
# ----------------------------
def predict_toxicity(descriptors_scaled, model):
    prediction = model.predict(descriptors_scaled)[0]
    label = "Toxic" if prediction == 1 else "Non-Toxic"

    if hasattr(model, "predict_proba"):
        confidence = max(model.predict_proba(descriptors_scaled)[0])
        return label, confidence
    return label, None


# ----------------------------
# CLI Entry
# ----------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python stack-tox.py 'SMILES_STRING'")
        sys.exit(1)

    smiles = sys.argv[1]

    # Step 1: Validate SMILES
    if not is_valid_smiles(smiles):
        print("Invalid SMILES notation.")
        sys.exit(1)

    # Step 2: Load pipeline
    print("Loading model and preprocessing pipeline...")
    model, scaler, imputer, descriptor_list = load_pipeline()

    # Step 3: Calculate descriptors with verbose output
    descriptors, missing_indices = calculate_descriptors_verbose(smiles, descriptor_list)

    # Step 4: Preprocess descriptors
    descriptors_scaled = preprocess_descriptors(descriptors, missing_indices, imputer, scaler)

    # Step 5: Predict toxicity
    label, confidence = predict_toxicity(descriptors_scaled, model)
    if confidence is not None:
        print(f"Prediction: {label} (Confidence: {confidence:.2f})")
    else:
        print(f"Prediction: {label}")


if __name__ == "__main__":
    main()
