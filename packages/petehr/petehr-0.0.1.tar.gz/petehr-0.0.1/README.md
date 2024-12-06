# petehr

`petehr` is your Personal Assistant for Creating Research-Ready EHR Data. A Python Toolkit for EHR Processing.

## Features
- **Text-to-Code Mapping**: Convert medical text to standardized medical codes.
- **Custom Dictionary Support**: Integrate your own medical concept dictionary. For string to medical codes, we recommend using UMLS.
- **Lightweight and Efficient**: Designed for simplicity and speed in processing EHR data. 
*Note*: Negation detection is not available in this version.

## Installation

```bash
pip install petehr
```

## Usage

```python
from petehr import Text2Code

# Dictionary is a two column CSV file with strings and their corresponding codes.
# Example of a sample String-CUI dictionary:

'''
str,code
Asthma,C0004096
Tuberculosis,C0041296
Tylenol,C0699142
Spinal fusion,C3278509
'''

mapper = Text2Code("sample_dict.csv")

# Convert text to a string of codes
codes = mapper.convert("Patient presents with a history of asthma and reports worsening asthma symptoms over the past.")

print(codes)  # Output: "C0004096,C0041296,C0699142,C3278509"

```