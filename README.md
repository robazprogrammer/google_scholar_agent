# Google Scholar Agent (AAEL Research Tool)

This project is a Python-based research agent designed to process Google Scholar alert emails, extract articles, rank their relevance, and generate structured daily briefings.

It was developed as part of ongoing work in **AI-Augmented Exploratory Learning (AAEL)**, which examines how professionals learn, adapt, and solve unfamiliar problems using AI tools.

---

## 🚀 What This Tool Does

1. Connects to Gmail securely via OAuth
2. Pulls Google Scholar alert emails
3. Extracts article titles, links, and summaries
4. Deduplicates results
5. Scores articles based on AAEL relevance
6. Generates:

   * Daily SitRep (DOCX)
   * CSV dataset of articles
   * NotebookLM-ready briefing packet

---

## 🧠 Why This Exists

Most AI-in-education research focuses on outcomes and performance.

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

```
email_extractor.py   # Gmail integration (OAuth)
scholar_parser.py    # Extracts articles from emails
aael_ranker.py       # Scores relevance to AAEL
sitrep_writer.py     # Generates reports and outputs
```

---

## 🔐 Authentication (Required)

This project uses Google OAuth to access Gmail.

You must provide your own credentials:

1. Go to Google Cloud Console
2. Enable Gmail API
3. Create OAuth client credentials
4. Download `credentials.json`

A placeholder file is included for reference.

---

## ⚠️ Security Notes

* No personal credentials are included in this repository
* Do NOT upload your real `credentials.json` or `token.json`
* Use `.gitignore` to prevent accidental exposure

---

## 🧪 Example Output

* 100+ articles processed per run
* Deduplicated and ranked
* Daily research briefing generated automatically

---

## 🔭 Future Direction

This tool is part of a broader research agenda exploring:

**AI-Augmented Exploratory Learning (AAEL)**

Future work includes:

* Prompt tracking and iteration analysis
* Workflow capture and behavioral patterns
* Integration into professional training environments

---

## 🤝 Contributions / Interest

If you're working in:

* AI in education
* EdTech research
* Human-AI interaction
* Professional learning

Feel free to connect or reach out.

---

## 📬 Contact

Robert Foreman
Doctoral Student, Educational Technology (CMU)
Email: [forem1r@cmich.edu](mailto:forem1r@cmich.edu)

---

## 📄 License

MIT License

