# xBRL Forge

![xBRL Forge Logo](path/to/logo.png)

## Overview

**xBRL Forge** is an open-source software solution designed to streamline the process of creating final XBRL (eXtensible Business Reporting Language) and iXBRL (Inline XBRL) reports by integrating data from multiple software applications. With xBRL Forge, users can effortlessly generate XBRL taxonomies and compile comprehensive reports using a simple JSON structure for integration.

## Features

- **Multi-Source Integration**: Seamlessly gather data from various software solutions and compile them into a unified XBRL or iXBRL report.
- **XBRL Taxonomy Generation**: Create customizable XBRL taxonomies to meet your reporting needs.
- **Easy JSON Structure**: Integrate data using an intuitive and straightforward JSON format.
- **Open Source**: Contribute to the community and enhance the functionality of xBRL Forge.

## Getting Started

### Prerequisites

- **Node.js** (version 14 or higher)
- **npm** (Node Package Manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/xbrl-forge.git
   cd xbrl-forge
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Usage

1. Prepare your data in the JSON structure according to [the documentation](docs/JSON_INPUT.md).

2. Pass the data to the generation function defined [here](xbrl_generation/__init__.py).

### Example

```python
from xbrl_generation import generate, File

with open("examples/stylesheet.css", "r") as f:
    style_data = f.read()
with open("examples/ESEF-ixbrl.json", "r") as f:
    data = json.loads(f.read())

results: File = generate(data, styles=style_data)
results.save_file("examples/result", True)
```

## Documentation

For detailed documentation on how to use xBRL Forge, including API references and examples, please refer to the [docs](docs/) folder.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Make your changes and commit them: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Create a pull request.

Please ensure your contributions align with the project guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue in the GitHub repository or reach out via [email](mailto:anton.j.heitz@gmail.com).

---

Thank you for using xBRL Forge! We look forward to your feedback and contributions!