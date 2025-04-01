# DailyAI News Reporter

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An automated system that collects AI-related news from various sources, generates comprehensive reports, and delivers them via email.

## Features

- Automated news collection from multiple sources
- AI-powered news categorization and analysis
- Beautiful HTML report generation
- Scheduled email delivery
- Support for immediate report generation

## Prerequisites

- Python 3.8 or higher
- Gmail account for sending emails
- DeepSeek API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kororu-lab/DailyAI.git
cd DailyAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the root directory with the following content:
```
DEEPSEEK_API_KEY=your_api_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

4. Configure email recipients:
Edit `config/email_list.txt` to add recipient email addresses.

## Usage

### Scheduled Execution
To run the scheduler that automatically collects news and sends reports at midnight:
```bash
./start.sh
```

### Immediate Execution
To immediately collect news, generate a report, and send it via email:
```bash
./start.sh --now
```

## Project Structure

```
DailyAI/
├── config/
│   └── email_list.txt    # Email recipient list
├── data/                 # Collected news data
├── logs/                 # Log files
├── reports/             # Generated HTML reports
├── src/
│   ├── collect_news.py  # News collection script
│   ├── generate_report.py # Report generation script
│   ├── send_report.py   # Email sending script
│   └── scheduler.py     # Scheduler script
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── start.sh            # Start script
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 