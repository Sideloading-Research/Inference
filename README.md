# Inference

Project for automatic semantic, emotional, and sentimental analysis tool for data augmentation in text behavior for sideload.

## System Requirements

This software has been tested on:
- Operating System: Linux (Debian/Ubuntu) 6.1.0-37-amd64
- Python: 3.8+
- RAM: Minimum 16GB recommended
- Storage: At least 10GB free space for model downloads

## Project Structure

```
Inference/
├── ARCHITECTURE.md            # Detailed architecture documentation
├── CHANGELOG.md               # Version history and changes
├── COGNITIVE_SYSTEM_README.md # Cognitive system documentation
├── README.md                  # Main documentation (this file)
├── requirements.txt           # Project dependencies
├── emotional_analyzer.py      # Emotional analysis module
├── engine.py                  # Core inference engine
├── integrated_system.py       # Main system integration
├── nlp_to_inference.py        # NLP processing module
├── simple_example.py          # Usage examples
└── test.inf                   # Test cases and examples
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sideloading-Research/Inference.git
cd Inference
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install Ollama:
```bash
# For Linux
curl -fsSL https://ollama.com/install.sh | sh

# For Windows
# Download from https://ollama.com/download/windows
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Download and setup Gemma 2B model:
```bash
# Start Ollama service first
ollama serve

# In a new terminal, pull the model
ollama pull gemma:2b
```

## Model Setup

### Gemma 2B
This project uses Google's Gemma 2B model through Ollama. Important considerations:

- Model Size: ~4GB
- RAM Usage: ~8GB during inference
- First run will download the model
- Subsequent runs will use the cached model

### Configuration
The model can be configured through environment variables or a `.env` file:

```env
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=gemma:2b
```

## Usage

1. Ensure Ollama is running:
```bash
ollama serve
```

2. Run the inference system:
```bash
python integrated_system.py
```

## Features

- Semantic analysis of text input
- Emotional state detection
- Sentiment analysis
- Data augmentation capabilities
- Sideloading research integration

## Development Guidelines

1. Always create and use a virtual environment
2. Do not commit the following to the repository:
   - Virtual environment directories (venv/, .env/)
   - Python cache files (__pycache__/)
   - Local configuration files (.env)
   - Large model files or cached data
3. Keep dependencies updated in requirements.txt

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes        (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch         (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support, please open an issue in the GitHub repository.

## Author

2025/10/15 Marco Baturan Garcia 