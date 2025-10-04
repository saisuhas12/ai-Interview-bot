# 🎯 AI Interview Q&A Bot

A powerful Streamlit application that generates personalized interview questions and sample answers based on job descriptions. Perfect for job seekers preparing for interviews or HR professionals creating interview materials.

## ✨ Features

- **Smart Question Generation**: Creates tailored interview questions based on job descriptions
- **Sample Answers**: Generates high-quality sample answers for each question
- **Answer Evaluation**: Get AI-powered feedback on your own answers with scoring
- **File Upload Support**: Upload PDF, DOCX, or TXT job descriptions
- **Customizable Settings**: Choose number of questions and question types
- **Fast & Optimized**: Parallel processing and caching for quick responses
- **Modern UI**: Clean, user-friendly interface with sidebar controls

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saisuhas12/ai-interview-bot.git
   cd ai-interview-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL_ID=gemini-1.5-flash
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 Usage Guide

### 1. Input Job Description
- **Paste directly**: Copy and paste the job description into the text area
- **Upload file**: Upload PDF, DOCX, or TXT files using the sidebar uploader
- **Tips**: Include key responsibilities, required skills, and qualifications for best results

### 2. Configure Settings
Use the sidebar to customize:
- **Number of questions**: 3-20 questions
- **Question types**: Behavioral/HR questions and technical questions
- **Generate**: Click either the sidebar or main button to start

### 3. Review Generated Content
- **Questions**: View the generated interview questions
- **Sample Answers**: Read AI-generated sample answers for each question
- **Download**: Export all Q&A pairs as JSON

### 4. Practice & Evaluate
- **Select a question**: Choose from the generated questions
- **Type your answer**: Practice answering in your own words
- **Get feedback**: Receive AI evaluation with scores and improvement suggestions

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **AI Model**: Google Gemini 1.5 Flash (configurable)
- **Processing**: Parallel answer generation with ThreadPoolExecutor
- **Caching**: Streamlit cache_data for performance optimization

### Performance Optimizations
- **Generation Config**: Token limits and temperature control
- **Parallel Processing**: Concurrent answer generation (up to 4 workers)
- **Smart Caching**: Avoids recomputation on UI reruns
- **Efficient Parsing**: Optimized text extraction from uploaded files

### File Structure
```
ai-interview-bot/
├── app.py              # Main Streamlit application
├── prompts.py          # AI prompts for questions and answers
├── utils.py            # Utility functions for file processing
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env               # Environment variables (create this)
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL_ID`: Model to use (default: gemini-1.5-flash)

### Model Options
- `gemini-1.5-flash`: Fast, cost-effective (recommended)
- `gemini-1.5-pro`: More capable but slower
- `gemini-1.0-pro`: Alternative option

## 📊 Features Breakdown

### Question Generation
- Analyzes job description context
- Creates behavioral and technical questions
- Tailored to specific roles and requirements
- Configurable question count and types

### Answer Generation
- High-quality sample answers
- Role-specific examples and scenarios
- Concise and actionable responses
- Parallel processing for speed

### Answer Evaluation
- **Scoring**: 1-10 scale for overall performance
- **Category Scores**: Content, structure, relevance, clarity
- **Feedback**: Actionable improvement suggestions
- **Improved Answer**: AI-generated better version

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Google Gemini](https://ai.google.dev/) for the AI capabilities
- [PyPDF2](https://pypdf2.readthedocs.io/) and [docx2txt](https://github.com/ankushshah89/python-docx2txt) for file processing

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/saisuhas12/ai-interview-bot/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Future Enhancements

- [ ] Voice input/output support
- [ ] Multiple language support
- [ ] Interview simulation mode
- [ ] Resume analysis integration
- [ ] Company-specific question databases
- [ ] Advanced analytics and insights

---

**Made with ❤️ for job seekers and interviewers everywhere**
