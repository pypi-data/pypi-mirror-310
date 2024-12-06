# dv-normalize

A Python library for normalizing Dhivehi text by converting numbers to Dhivehi and standardizing sentence endings.

## Features

- Converts numbers to Dhivehi text (both written and spoken forms)
- Handles years (when followed by ވަނަ)
- Handles decimal numbers
- Normalizes formal sentence endings to colloquial form
- Preserves proper spacing and punctuation

## Installation

```bash
pip install dv-normalize
```

## Usage

There are two main functions in this library:

1. `int_to_dv` - This function converts numbers to Dhivehi text in written form.
2. `spoken_dv` - This function converts dhivehi text to spoken form.

### Written form

```python

## test case for int_to_dv

from dv_normalize.dv_num import int_to_dv

def main():
    while True:
        try:
            num = input("Enter a number (0 to trillion) or 'q' to exit: ")
            if num.lower() == 'q':
                break
                
            num = int(num)
            if num < 0:
                print("Please enter a non-negative number")
                continue
                
            print(f"{num:,} in Dhivehi:")
            written = int_to_dv(num, is_spoken=False)
            spoken = int_to_dv(num, is_spoken=True)
            year = "Not a valid year format" if num < 1000 or num > 9999 else int_to_dv(num, is_year=True)
            
            print(f"Written form: {written}")
            print(f"Spoken form: {spoken}")
            print(f"Year form: {year}")
            
        except ValueError:
            print("Please enter a valid number")

if __name__ == "__main__":
    main()
```

### Spoken form

```python
from dv_normalize.dv_sentence import spoken_dv

# Test cases
test_cases = [
    "މިއަދު ވަރަށް ފިނިވެއެވެ.",  # Verb ending
    "މިއީ ރީތި ފޮތެކެވެ.",        # Noun ending
    "އޭނާ ދަނީ ސްކޫލަށެވެ.",      # Direction ending
    "1955 މީހުން ތިބެއެވެ.",      # Number with ending
    "2024 ވަނަ އަހަރު",            # Year
    "12.5 ރުފިޔާ",                # Decimal
    "1000 މީހުން",                # Regular number
    "މިއީ ރީތި ފޮތެކެވެ.",          # Sentence ending
    "އޭނާ ގެއަށެވެ.",              # Sentence ending
    "ހާއްސަ އެއްބަސްވުމުގެ ދަށުން އިންޑިއާއިން ރާއްޖެއަށް ވިއްކާ ހަކުރު އޮޅުވާލައިގެން ލަންކާއަށް!", # test sentence
    "އެ އިދާރާއިން ބަލަމުން އަންނަނީ މިދިޔަ މަހުގެ 25 ގައި އެގައުމުން ބޭރު ކުރި 64 ހާސް ޓަނުގެ ހަކުރުގެ ޝިޕްމެންޓެއްގެ މައްސަލަ އެވެ. އެ ޝިޕްމެންޓް އެގައުމުން ބޭރުކުރީ ރާއްޖެ އާއި އިންޑިއާ އާ ދެމެދު ވެފައިވާ ވިޔަފާރީގެ ހާއްސަ އެއްބަސްވުމުގެ ދަށުން ކަނޑައަޅާފައިވާ އަގުތަކުގައި ނަމަވެސް، އެއިން ބައެއް ލަންކާއަށް އެތެރެކުރިން ފަޅާއަރާފައިވާ ކަމަށް އިންޑިއާގެ ބައެއް ނޫސްތަކުގައި ރިފޯޓުކޮށްފައިވެ އެވެ." # test long sentence
]

for test in test_cases:
    print(f"Original: {test}")
    print(f"Normalized: {spoken_dv(test)}\n")

```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.