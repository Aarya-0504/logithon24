from langchain.llms import OpenAI
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
import pandas as pd
import re
#import replicate
from langchain.prompts import PromptTemplate

#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



#Function to extract data from text
# def extracted_data(pages_data):

#     template = """Extract all the following values : invoice no., Description, Quantity, date, 
#         Unit price , Amount, Total, email, phone number and address from this data: {pages}

#         Expected output: remove any dollar symbols {{'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00','Amount': '2200.00','Total': '2200.00','Email': 'Santoshvarma0988@gmail.com','Phone number': '9999999999','Address': 'Mumbai, India'}}
#         """
#     prompt_template = PromptTemplate(input_variables=["pages"], template=template)

#     llm = OpenAI(temperature=.7)
#     full_response=llm(prompt_template.format(pages=pages_data))
#     return full_response
import openai

# Assuming you have set up your OpenAI API key
openai.api_key = "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"

def extracted_data(pages_data):
    template = f"""
        Extract all the following values: invoice no., Description, Quantity, date, 
        Unit price, Amount, Total, email, phone number, and address from this data: {pages_data}

        Expected output: remove any dollar symbols {'{'}'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00','Amount': '2200.00','Total': '2200.00','Email': 'Santoshvarma0988@gmail.com','Phone number': '9999999999','Address': 'Mumbai, India'{'}'}
    """

    response=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": template},        
    ]
)

    return response.choices[0]['message']['content']


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    
    df = pd.DataFrame({'Invoice no.': pd.Series(dtype='str'),
                   'Description': pd.Series(dtype='str'),
                   'Quantity': pd.Series(dtype='str'),
                   'Date': pd.Series(dtype='str'),
	                'Unit price': pd.Series(dtype='str'),
                   'Amount': pd.Series(dtype='int'),
                   'Total': pd.Series(dtype='str'),
                   'Email': pd.Series(dtype='str'),
	                'Phone number': pd.Series(dtype='str'),
                   'Address': pd.Series(dtype='str')
                    })

    data_list = []  # Create an empty list to store extracted data
    for filename in user_pdf_list:
        print(filename)
        raw_data = get_pdf_text(filename)
        llm_extracted_data = extracted_data(raw_data)
        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            data_dict = eval('{' + extracted_text + '}')
            data_list.append(data_dict)  # Append extracted data to the list
        else:
            print("No match found.")

    print("********************DONE***************")
    df = pd.DataFrame(data_list)  # Create DataFrame from accumulated data
    df.head()
    return df
    