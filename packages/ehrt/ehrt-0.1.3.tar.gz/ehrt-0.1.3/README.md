# ehrt

`ehrt` is a set of foundational tools and pipelines for processing EHR data to create research ready datasets. TETHER is a learning library designed to help analysts and healthcare professionals familiarize themselves with EHR processing.

## Installation

```bash

pip install ehrt
```

## Usage

```python
from ehrt import Text2Cui

# Dictionary is a csv file with string and corresponding cui. Eg: asthma, C0004096
t2c = Text2Cui("sample_dict.csv")


# Convert a text to list of cuis
cuis = t2c.traverse("Patient presents with a history of asthma and reports worsening asthma symptoms over the past")

print(cuis)  # cuis: "C0004096,CUI54321"
```