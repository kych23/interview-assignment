# Your code here
# Python Libraries
from dotenv import load_dotenv
import pymupdf4llm
from openai import OpenAI
from pydantic import BaseModel
import os
import json
import csv
from pathlib import Path
import re 

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

STOPWORDS = {"submittal", "review", "approved", "office", "project", "date", "prepared by", 
    "transmitted", "remarks", "submitted by", "engineer", "architect",
    "contractor", "revision", "item number", "item description", "status", "address", "phone", "fax", "email", "website", "www.", "suite", "dr.", 
    "st.", "road", "avenue", "drive", "p.o.", "street", "contact", "tel", "copyright", "reserved", "warning", "disclaimer", "liability", "responsibility", "relieve", "does not", "shall", "subject to change", "page", "sheet", "printed on", "cover sheet", "table of contents", "section", "notes", "drawing", "job", "unit tag", "order number", "comments", "description", "quantity", "qty", "submitted", "delivered via",
    "transmitted to", "transmitted by", "mstr", "pk", "disc", "code", 
    "file", "location", "note:", "revision", "system service information"
}

def preprocess_text(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip().lower()
        if not line or any(sw in line for sw in STOPWORDS):
            continue
        line = re.sub(r"\s{2,}", " ", line)
        cleaned.append(line)
    return "\n".join(cleaned)

def extract_text(filepath):
  """
  Given a PDF filepath, return a list of dicts containing page numbers and its extracted text
  """
  text = pymupdf4llm.to_markdown(filepath, page_chunks=True)
  return text
  
def extract_properties(page_texts):
  """
  Given a list of dicts with keys 'metadata' and 'text', prompt the OpenAI API
  to extract a JSON array of product entries, each containing:
    - product_name: str
    - manufacturer: str
    - pages: [int]
  Returns a list of those JSON objects as dictionaries.
  """
  extractions = []
  
  for page_text in page_texts:
      page = page_text['metadata']["page"]
      text = page_text["text"]
      text = preprocess_text(text)

      prompt = (
        "You are given the Markdown-formatted text of **one page** from a construction product submittal. "
        "Your task is to extract **the most important product entries** and return them as a **JSON array**. "
        "Each entry must be an object with **exactly** the following keys:\n\n"
        "  • product_name   - The product's full model number or part number (if listed), and a full descriptive name\n"
        "  • manufacturer   - The manufacturer's name. If it's not clearly listed near the product, infer it from surrounding context or headers. You must put a manufacturer, unknown is not an option\n"
        "  • pages          - A list of page numbers (integers) where the product appears. Include the current page number at minimum.\n\n"
        
        "Products may be listed in paragraph form or in tabular form (e.g., rows like `EGC5 - AL - ½\" Eggcrate Grid ...`). "
        "For these, treat the first field (before the dash or delimiter) as the `product_name`. "
        "Use the rest of the line as the description only if it helps disambiguate the product.\n\n"
        "Manufacturers may only appear once at the top or bottom of the document—carry this name to all products if no other manufacturer is clearly indicated.\n\n"
        "Ignore administrative content like submittal forms, contact info, page numbers, and section headings unless they help establish the manufacturer.\n\n"
        "Try to include only the main products in the text, not components or parts of a product\n\n"
        "If a page doesn't seem to have a product listed, you may skip this page\n\n"
        "**Output only the JSON array. Do not include any explanatory text, headers, or markdown.**\n\n"
        "Example output:\n"
        "[\n"
        "  {\"product_name\": \"45MAHAQ18XA3 High Wall Heat Pump Ductless System (Indoor Unit)\", \"manufacturer\": \"Carrier Corporation\", \"pages\": [2]},\n"
        "  {\"product_name\": \"5HCF23 Hard Ceiling Frame, Adapts F23 to F22, Aluminum\", \"manufacturer\": \"Krueger\", \"pages\": [16]}\n"
        "]\n\n"
        f"Now extract from this text:\n\"\"\"{text}\"\"\""
    )

      response = client.chat.completions.create(
          model="gpt-4o-mini-2024-07-18",
          messages=[{
            "role": "user", 
            "content": prompt
          }],
      )
      
      raw = response.choices[0].message.content
      try:
          data = json.loads(raw)
      except json.JSONDecodeError:
        continue

      for data in data:
          data.setdefault("pages", []).append(page)
          extractions.append(data)
          
  return extractions
    
def data_to_csv(csv_path, products):
    """
    Write all products to one CSV. `pages` is serialized as JSON.
    """
    fieldnames = ["product_name", "manufacturer", "pages"]
    unique_products = dedupe(products) 
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for prod in unique_products:
            writer.writerow({
                "product_name": prod["product_name"],
                "manufacturer": prod["manufacturer"],
                "pages": json.dumps(prod.get("pages", []))
            })
    
          
def dedupe(records: list[dict]) -> list[dict]:
    """
    Combines rows that describe the same product and merge their page lists.
    """
    merged: dict[str, dict] = {}
    for rec in records:
        key = re.sub(r"[^a-z0-9]", "", (rec["product_name"]).lower())
        if key not in merged:
            merged[key] = {**rec, "pages": set(rec["pages"])}
        else:
            merged[key]["pages"].update(rec["pages"])
            if merged[key]["manufacturer"].lower() == "unknown" and \
               rec["manufacturer"].lower() != "unknown":
                merged[key]["manufacturer"] = rec["manufacturer"]

    for rec in merged.values():
        rec["pages"] = sorted(rec["pages"])
    return list(merged.values())
  
if __name__ == "__main__":
  input_pdfs = [
      "input/230000-001 HVAC Submittal.pdf",
      "input/283100-001 Fire Alarm Shops and PD Submittal.pdf",
      "input/KP OLAB 220523-001 Plumbing Piping Valves FA.pdf",
  ]

  out_dir = Path("output")
  out_dir.mkdir(exist_ok=True)

  for filepath in input_pdfs:
      print("Processing "+ filepath)
      pages = extract_text(filepath)
      products = extract_properties(pages)

      base = Path(filepath).stem         
      out_csv = out_dir / (base+"_products.csv")
      data_to_csv(str(out_csv), products)


    