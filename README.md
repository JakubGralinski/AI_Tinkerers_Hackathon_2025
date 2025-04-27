# CrunchByte - AI-Powered Health & Fitness Assistant

CrunchByte is an innovative AI-powered personal health and fitness assistant that leverages advanced reasoning models to provide personalized wellness recommendations. It integrates with multiple health and fitness platforms to provide holistic health management.

## Prerequisites

- Python 3.13
- Git
- Pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/crunchbyte.git
cd crunchbyte
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## API Keys Setup

CrunchByte requires several API keys to function. Here's how to obtain and configure each one:

### 1. OpenAI API Key
- Visit [OpenAI Platform](https://platform.openai.com/)
- Sign up or log in to your account
- Navigate to API Keys section
- Create a new API key
- Add to your environment variables:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 2. Google Calendar API
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the client configuration file
6. Save it as `client_secret.json` in the project root
7. On first run, follow the OAuth flow to generate `token.json`

### 3. Strava API
1. Visit [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application
3. Note down your Client ID and Client Secret
4. Add to your environment variables:
```bash
export STRAVA_CLIENT_ID='your-client-id'
export STRAVA_CLIENT_SECRET='your-client-secret'
```

### 4. MyFitnessPal Integration
MyFitnessPal integration requires your account credentials and uses browser automation to fetch data:

1. Create a MyFitnessPal account at [MyFitnessPal](https://www.myfitnesspal.com/)
2. Add your credentials to the `.env` file:
```bash
MFP_USERNAME='your-myfitnesspal-email'
MFP_PASSWORD='your-myfitnesspal-password'
```

Note: The MyFitnessPal integration uses browser automation to fetch your nutrition data. Make sure you have a stable internet connection when using this feature.

## Configuration

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add your API keys and configuration:
```env
OPENAI_API_KEY=your-openai-api-key
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
MFP_USERNAME=your-myfitnesspal-email
MFP_PASSWORD=your-myfitnesspal-password
```

## Running the Application

1. Start the Flask server:
```bash
python run.py
```

2. The application will be available at `http://localhost:5000`

## Testing the Application

1. **Initial Setup**
   - The first time you run the application, it will guide you through the OAuth setup for Google Calendar
   - Follow the prompts to authorize the application

2. **Testing Features**
   - **Activity Analysis**: Connect your Strava account and view your workout recommendations
   - **Nutrition Planning**: The app will automatically fetch your MyFitnessPal data using your credentials
   - **Schedule Optimization**: View your Google Calendar integration and receive optimal workout timing suggestions

3. **API Endpoints**
   - `/api/health`: Check API health status
   - `/api/activities`: Get workout recommendations
   - `/api/nutrition`: Get nutrition insights
   - `/api/schedule`: Get schedule optimization suggestions

## Project Structure

```
crunchbyte/
├── app/
│   ├── agents/
│   │   └── plan/
│   ├── routes/
│   ├── services/
│   ├── config.py
│   └── __init__.py
├── demo/
├── docs/
├── .env
├── requirements.txt
├── run.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.
