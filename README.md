# Google Scholar Agent (AAEL Research Tool)

A Python-based research agent that processes Google Scholar alert emails, extracts articles, ranks their relevance, and generates structured daily briefings.

Developed as part of ongoing doctoral research in:

**AI-Augmented Exploratory Learning (AAEL)**

---

## 🚀 What This Tool Does

This agent automates your research intake pipeline:

1. Connects to Gmail via OAuth
2. Pulls Google Scholar alert emails
3. Extracts article titles, links, and summaries
4. Deduplicates results
5. Scores articles based on AAEL relevance
6. Generates outputs:

   * 📄 SitRep (DOCX)
   * 📊 CSV dataset
   * 🧠 NotebookLM-ready packet

---

## 🧠 Why This Exists

Most AI-in-education research focuses on:

* Performance
* Outcomes
* Efficiency

This tool supports a different question:

> How do humans actually *learn* with AI?

The ranking system prioritizes:

* Metacognition
* Self-regulated learning
* Human-AI interaction
* Exploratory learning
* Neurodiversity and special education

---

## 📂 Project Structure

```plaintext
google_scholar_agent/
│
├── src/
│   ├── email_extractor.py
│   ├── scholar_parser.py
│   ├── aael_ranker.py
│   └── sitrep_writer.py
│
├── credentials.example.json
├── token.example.json
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## ⚙️ Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Set up Google OAuth

1. Go to Google Cloud Console
2. Enable Gmail API
3. Create OAuth credentials
4. Download your file and rename it:

```
credentials.json
```

---

### 3. Generate token

Run the script once:

```bash
python src/email_extractor.py
```

This will:

* Open a browser for authentication
* Generate `token.json` locally

---

## ▶️ How to Run

```bash
python src/email_extractor.py
```

---

## 📊 Example Output

Each run produces:

* **AAEL_SitRep_YYYY-MM-DD.docx**
* **AAEL_articles_YYYY-MM-DD.csv**
* **NotebookLM_packet_YYYY-MM-DD.txt**

---

## 🔐 Security Notes

* No real credentials are included in this repository
* Example credential files are placeholders only
* Never upload your actual:

  * `credentials.json`
  * `token.json`

---

## 🔭 Research Context

This tool supports doctoral research in:

**AI-Augmented Exploratory Learning (AAEL)**

**Research Focus:**

* How professionals approach unfamiliar tasks using AI
* Iterative prompting and problem-solving behavior
* Development of self-efficacy in AI-supported environments
* Human-AI collaboration as a learning process

---

## 🏫 Academic & Professional Contact

**Robert Foreman**
Doctoral Student, Educational Technology
Central Michigan University

📧 Email: [forem1r@cmich.edu](mailto:forem1r@cmich.edu)

🌐 NhanceData (Consulting & Research):
https://nhancedata.com

---

## 🚧 Future Development

* Prompt tracking and iteration analysis
* Workflow behavior logging
* Visualization dashboards
* Integration into professional training environments

---

## 🤝 Collaboration / Interest

If you're working in:

* AI in education
* EdTech research
* Human-AI interaction
* Professional learning

Feel free to connect.

---

## 📄 License

MIT License


