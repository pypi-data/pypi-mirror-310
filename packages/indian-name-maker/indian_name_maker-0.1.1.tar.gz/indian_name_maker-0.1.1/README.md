# Indian Name Maker

A Python package to generate Indian names. The package uses a synthetically generated dataset of Indian names created using state-of-the-art language models (Llama-3.2-11B-Vision-Instruct and OpenAI ChatGPT-4 v2.0).

## Installation

Install the package directly using pip:
```bash
pip install indian-name-maker
```

## Usage

### Python API
```python
from indian_name_maker import NameGenerator

# Create a name generator instance
generator = NameGenerator()

# Generate a random first name
first_name = generator.get_first_name()
print(f"First Name: {first_name}")

# Generate a random last name
last_name = generator.get_last_name()
print(f"Last Name: {last_name}")

# Generate a random full name
full_name = generator.get_full_name()
print(f"Full Name: {full_name}")

# Generate multiple full names
names = generator.get_multiple_names(count=5)
print(f"Multiple Names: {names}")

# Generate names with custom separator
custom_name = generator.get_full_name(separator="-")
print(f"Custom Separated Name: {custom_name}")
```

### Command Line Interface
```bash
# Generate a single full name
generate-indian-name

# Generate multiple names
generate-indian-name --count 5

# Generate first names only
generate-indian-name --first-only --count 3

# Generate with custom separator
generate-indian-name --separator "-"
```

## Features

- Generate random Indian first names
- Generate random Indian last names
- Generate random full names (combination of first and last names)
- Generate multiple names at once
- Command-line interface for easy access
- Based on a synthetically generated dataset of Indian names

## Dataset

The name dataset is synthetically generated using:
- Llama-3.2-11B-Vision-Instruct model (Hugging Face)
- OpenAI ChatGPT-4 (v2.0)

This ensures:
- Diverse name combinations
- Culturally appropriate naming patterns

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license.

For more details, see the [LICENSE](LICENSE) file or visit [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
