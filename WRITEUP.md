# Project Writeup

## Approach & Assumptions

[Describe your overall approach to solving this problem. What was your thought process? What were the key challenges you identified?]

After reading the background and task information, I split the task into workable chunks. I sectioned it off into four parts: one, to extract the text from the input pdf files; second, to divide the entire text into it's corresponding pages; third, to prompt OpenAI's LLM to create JSON objects with properties of the product name, manufacturer's name, and the current page; fourth, combine any duplicate JSON object products and create the output CSV file. I define a product to be an item that has a unique model ID number, so this includes the main products as well as its subparts.

To complete the first part and second part, I did some research on different python libraries such as PyMuPDF and pdfplumber and stumbled across a library called pymupdf4llm. I chose this one because it aimed to extract PDF information that is more easily digestible for LLMs. This library had a function where I could extract the data from the pdf into markdown text and categorize the text by page, which was perfect for the second part of my task.

To complete the third part, I learned how to use OpenAI API key to utilize their LLM and prompt it to return a dictionary of the important properties such as product name, manufacturer name, and page number for a text. I mainly used OpenAI documentation to learn and tested out different models and prompts. I specifically designed the prompt such that it would always return a JSON type that could be processed by my other functions and added other notes to better identify products.

Then finally for the final part, I postprocessed the data by combining duplicate product entries and converted the list of dictionaries holding each pages product name and manufacturer name into a csv file.

Some syntax challenges that I was having was using the OpenAI API key. At first I was getting an error saying the client I created didn't have an api_key passed to it. Luckily this was a quick fix, where I had to remove the quotes around the key in the .env file. Another challenge I had was understanding the object types returned by each function for library-specific functions such as pymupdf4llm.to_markdown(), client.chat.completions.create(), and csv.DictWriter(). I had to search up documentation and create in-line print statements to view the return types of these functions.

Some semantic challenges I faced was the effectiveness of the LLM model. At the first runthrough, the model seemed to pick up the subcontractor and the item descriptions on the first page rather than the products themselves. I figured this was caused by one of two things: either the text extraction was failing or the prompt wasn't strict enough. I first checked if the text extraction was working correctly, printing out the pages text property and manually checking if the printed text was the same text on the pdf file. This was working correctly, so the issue was a matter of tweaking the prompt such that it focused on the right parts of the text. I considered running the API multiple times and creating a list of the reoccurring products to remove any noise/products that don't consistently appear, however this is not cost-effective. In the end, I tweaked my prompt based on the previous outputs and preprocessed the extracted PDF text such that it removed non-relevant words.

Another challenge was that sometimes the products wouldn't have any manufacturers listed. This was a major inconsistency where on multiple executions, sometimes the manufacturer was listed and other times it said "unknown". Unfortunately, I didn't have time to fix this issue.

## Limitations & Future Improvements

[If you had more time, what would you improve?]

A limitation in my script is in the chance multiple products are listed on the same page in the pdf. Since I segment each page as its own stand-alone text to be prompted on, if a page has two products on it, my code will only pick one of them as the "product_name" for that page. This could miss out on potential key products listed in the documents and also lead to confusion like mixing up the manufacturers and the product names for both products on that page.

I would also have liked to consolidate similar products under one category. For example, my output would list every type of "Circuit Setter Plus Calibrated Balance Valves" when instead I could've just grouped them into "Circuit Setter Plus Calibrated Balance Valves" like in the sample output.

Other things I would have liked to improve is ensuring none of the products have an unknown manufacturer, optimizing the pre and postprocessing functions to better filter the products that get returned in the final csv, and more accurately consolidating similar products in the output CSV.
