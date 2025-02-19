# Customer Service Response Evaluator

This project evaluates customer service responses using OpenAI's GPT models, analyzing both content quality and formatting aspects of customer service interactions.

## Features

- Evaluates customer service responses based on content and format
- Processes CSV files containing ticket-response pairs
- Generates detailed evaluation reports with scoring and explanations
- Uses OpenAI's GPT models for intelligent analysis

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini  # or your preferred OpenAI model
```

## Input Data Format

The input CSV file should be semicolon-separated (;) and contain two columns:
- `ticket`: The customer's inquiry
- `reply`: The customer service response

Example:
```
ticket;reply
"Hi, I'd like to check my order status";"Your order #1234 will arrive tomorrow"
```

## Usage

1. Place your input CSV file in the `docs` directory

2. Run the evaluator:
```bash
python src/main.py
```

The script will:
- Process all tickets in the input file
- Evaluate each response for content and formatting
- Generate a `tickets_evaluated.csv` file with the results

## Output

The program generates a CSV file (`tickets_evaluated.csv`) containing:
- Original ticket and reply
- Content score (1-5) and explanation
- Format score (1-5) and explanation

## Dependencies

- openai>=1.0.0
- python-dotenv>=0.19.0
- pandas>=1.3.0
- pytest>=7.0.0
- pydantic>=2.0.0