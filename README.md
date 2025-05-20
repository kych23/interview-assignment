# Spect AI - Take-Home Interview Project

Welcome! This is a 48-hour take-home interview project for candidates applying to the Summer Software Engineering / Data Science Internship at Spect AI.

---

## 🧠 Background

At Spect AI, we work with 1000s of construction submittal PDFs submitted by contractors and subcontractors. These documents include technical product data for materials and equipment used in construction projects. As an intern, your first task will likely involve building a script that can extract structured information from these PDFs and generate a usable product database.

This take-home interview project is designed to simulate that work on a smaller scale.

---

## 📌 Your Task

You are given 3 sample construction submittal PDFs (in the `input/` folder). Your goal is to write a Python script that can automatically extract the products from a given PDF. For each PDF, you should output a single CSV file where each row is a unique product that has a Product Name and Manufacturer Name extracted. Your script should take the PDF path as input and should create the CSV file as output. The script should be generalizable, meaning you should use the same script for each PDF and your script will be tested on 1 additional hidden submittal PDF that is similar in nature but unseen to you.

Feel free to use any libraries, packages, or approach you think would work best. If you want to use language models or vision models in your approach, you can use OpenAI's models - we'll provide an API key for this purpose.

### 🔁 Bonus (optional):

Generate an additional column in the CSV titled "pages" where you provide a list of page numbers that each product is on.

---

## 📊 Sample Outputs

In the `sample_output/` folder, you'll find example CSV files showing how the output data could be structured. These are just examples - your output does **not** need to have an exact match for the product names and manufacturer names.

---

## 🛠️ Setup Instructions

1. Fork this repo to your GitHub account:

   - Click the "Fork" button in the top right of this repository
   - Clone your forked repo:
     ```bash
     git clone https://github.com/YOUR-USERNAME/interview-assignment.git
     cd interview-assignment
     ```

2. If you choose to use the OpenAI API:
   - You will receive an OpenAI API key from us. Save it in a `.env` file in the repo:
     ```
     OPENAI_API_KEY="your-key-here"
     ```
   - Please be mindful of API usage - while you can freely use the key for this project, avoid excessive calls or sharing the key.
   - **IMPORTANT**: Do not commit the `.env` file or include the API key in your submission. Add `.env` to your `.gitignore` file.

---

## 🚀 Submission Instructions

1. Fork this repo or create your own GitHub repo with your solution.

2. Make sure your repo includes:

   - Your full working code
   - A `requirements.txt` file that contains all the packages you used so that we can run your code ourselves
   - Your CSV output files in a folder called /output
   - A short write-up (`WRITEUP.md`) with:
     - Your approach and assumptions
     - Limitations or things you'd improve with more time

3. Email us the GitHub repo link (or zipped folder if needed)

---

## 🧠 Notes

- You're encouraged to use any tools, libraries, or AI coding assistants like ChatGPT, Cursor, Windsurf. We use Cursor as our IDE.
- This task is meant to be open-ended and realistic. We want to make sure you know how to programmatically work with PDFs, use Git, and use Python.
- Be prepared to explain your approach and code in a following interview.
- If you have any questions, feel free to reach out at sheel@getspect.ai.

Good luck! We're excited to see your work 🚀

---

## 🔒 Confidentiality Notice

This project and all its contents (including but not limited to PDFs, API keys, and code) are confidential and intended solely for your use in this interview process. Please do not share any part of this project, including the API key, with anyone else. Any unauthorized sharing or distribution of these materials is strictly prohibited.
