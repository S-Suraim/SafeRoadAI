<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/2eed8fbf-125c-4517-b2c3-7f1d06755f43" />

# 🚧 SafeRoad AI – Intelligent Road Safety Intervention System

**SafeRoad AI** is an intelligent system that analyzes road safety reports and automatically recommends relevant **IRC-based safety interventions**.  
It leverages **AI (Gemini)** to generate meaningful explanations that help **engineers and authorities** make data-driven decisions for safer roads.

---

## 🌍 Problem Statement
Manual analysis of road safety reports is time-consuming and prone to human oversight.  
There is a lack of automated tools to extract key issues and map them to standard **IRC safety interventions** efficiently.

---

## 💡 Solution
SafeRoad AI uses **AI-powered text understanding** to:
- Extract key road issues from uploaded **PDF reports** or manual text.
- Match them with predefined **IRC interventions**.
- Generate a professional **AI summary** explaining the rationale behind each recommendation.

---

## 🧠 Technologies Used
| Technology | Purpose |
|-------------|----------|
| **Python** | Core development |
| **Streamlit** | Web interface |
| **Pandas** | Data processing |
| **PyPDF2** | PDF text extraction |
| **Google Gemini API** | AI-based report generation |
| **CSV Dataset** | IRC Interventions reference |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/S-Md-Suraim/SafeRoad-AI.git
cd SafeRoad-AI
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Your Gemini API Key

```bash
set GOOGLE_API_KEY=your_api_key_here
```

*(or use `.env` file for security)*

### 5️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📊 Dataset Used

| File                           | Description                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **data/irc_interventions.csv** | Contains predefined IRC-based safety interventions           |
| **data/irc_costs.csv**         | (Optional) Can be extended to include intervention cost data |

---

## 🧩 Features

✅ Extracts key road issues from text or PDF
✅ Suggests matching interventions based on **IRC standards**
✅ Generates AI-powered explanations for each intervention
✅ Simple and elegant **Streamlit UI**
✅ Exportable results and summaries

---

## 👩‍💻 Team Members

* **S. Md. Suraim**
* **Hema Pravallika**

---

## 🏁 Outcome

SafeRoad AI helps field engineers and authorities:

* Save analysis time
* Improve consistency in report interpretation
* Get intelligent summaries ready for official documentation

---

## 🎯 Future Enhancements

* Integrate cost estimation (from `irc_costs.csv`)
* Add geospatial visualization for accident-prone zones
* Deploy online using **Streamlit Cloud** or **Hugging Face Spaces**

---

## 🙏 Thank You

> Building safer roads, one AI insight at a time 🛣️
> *Developed for Hackathon 2025*

---

# 🚧 SafeRoad AI – Intelligent Road Safety Intervention System

**SafeRoad AI** is an intelligent system that analyzes road safety reports and automatically recommends relevant **IRC-based safety interventions**.  
It leverages **AI (Gemini)** to generate meaningful explanations that help **engineers and authorities** make data-driven decisions for safer roads.

---

## 🌍 Problem Statement
Manual analysis of road safety reports is time-consuming and prone to human oversight.  
There is a lack of automated tools to extract key issues and map them to standard **IRC safety interventions** efficiently.

---

## 💡 Solution
SafeRoad AI uses **AI-powered text understanding** to:
- Extract key road issues from uploaded **PDF reports** or manual text.
- Match them with predefined **IRC interventions**.
- Generate a professional **AI summary** explaining the rationale behind each recommendation.

---

## 🧠 Technologies Used
| Technology | Purpose |
|-------------|----------|
| **Python** | Core development |
| **Streamlit** | Web interface |
| **Pandas** | Data processing |
| **PyPDF2** | PDF text extraction |
| **Google Gemini API** | AI-based report generation |
| **CSV Dataset** | IRC Interventions reference |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/S-Md-Suraim/SafeRoad-AI.git
cd SafeRoad-AI
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Your Gemini API Key

```bash
set GOOGLE_API_KEY=your_api_key_here
```

*(or use `.env` file for security)*

### 5️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📊 Dataset Used

| File                           | Description                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **data/irc_interventions.csv** | Contains predefined IRC-based safety interventions           |
| **data/irc_costs.csv**         | (Optional) Can be extended to include intervention cost data |

---

## 🧩 Features

✅ Extracts key road issues from text or PDF
✅ Suggests matching interventions based on **IRC standards**
✅ Generates AI-powered explanations for each intervention
✅ Simple and elegant **Streamlit UI**
✅ Exportable results and summaries

---

## 👩‍💻 Team Members

* **S. Md. Suraim**
* **Hema Pravallika**

---

## 🏁 Outcome

SafeRoad AI helps field engineers and authorities:

* Save analysis time
* Improve consistency in report interpretation
* Get intelligent summaries ready for official documentation

---

## 🎯 Future Enhancements

* Integrate cost estimation (from `irc_costs.csv`)
* Add geospatial visualization for accident-prone zones
* Deploy online using **Streamlit Cloud** or **Hugging Face Spaces**

---

## 🙏 Thank You

> Building safer roads, one AI insight at a time 🛣️
> *Developed for Hackathon 2025*

---
