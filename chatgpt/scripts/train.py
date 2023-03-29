import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM
import re
import PyPDF2
import nltk
from nltk import sent_tokenize
nltk.download("punkt")
import openai

# Load the pre-trained GPT2 model and tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# model = GPT2LMHeadModel.from_pretrained('gpt2')

# tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
# model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

file_path = '/home/palash/Documents/python-learnings/django-celery/chatgpt/scripts/dm2.pdf'



pdf_file = open(file_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
print(len(pdf_reader.pages))

TEXTS=[]
# get texts
for page in range(4):#len(pdf_reader.pages)
    page_obj = pdf_reader.pages[page]
    TEXTS+=[page_obj.extract_text()]

pdf_file.close()




def get_transcript_as_sentences(paragraphs):
    
##################################################
    num=0 #set
    texts=[]
    for p in paragraphs[num:]:
        text = p.strip()
        texts+=[text]
##################################################

    transcript = ' '.join([string for string in texts])
    transcript = re.sub(r"http\S+", "", transcript)
    transcript = re.sub(r"\S*@\S*\s?", "", transcript)
    sentences = sent_tokenize(transcript)    

    return sentences


sentences0 = get_transcript_as_sentences(TEXTS)
sentences = sentences0[0:50]
# print(len(sentences0),len(sentences))


def how_many_tokens(text):
# Returns size of text in terms of number of tokens
    num_chars = len(text)
    num_tokens = round(num_chars/4)
    return num_tokens
    
transcript = " ".join(sentences)

# print("Transcript size: {} Tokens".format(how_many_tokens(transcript)))



# Define a number of chunks
num_chunks = 2
chunk_size = round(len(sentences)/num_chunks)

# Initialise a list to store chunks
chunks = []

for i in range(num_chunks):
    if i == num_chunks - 1:
        # For the last chunk, get all remaining sentences
        chunks.append(" ".join(sentences[chunk_size*i:]))
    else:
        # Otherwise, get only sentences for current chunk
        chunks.append(" ".join(sentences[chunk_size*i:chunk_size*(i+1)]))
    
# Check how many tokens in each chunk
# for i, chunk in enumerate(chunks):
#     print("Chunk {}: {} Tokens".format(i+1, how_many_tokens(chunk)))





def get_summaries_from_transcript(transcript_chunk, prompt, is_test=True):
# Returns GPT-3's response for a given chunk of transcript and prompt
    
    if is_test:
        return ""
    
    openai.organization = 'org-key'
    openai.api_key = 'key'

    # Join together the transcript chunk with a specific prompt / task
    transcript_with_prompt = transcript_chunk + "\n" + prompt
    
    output = openai.Completion.create(engine="text-davinci-003",
                                      prompt=transcript_with_prompt,
                                      temperature=0.3,
                                      max_tokens=1024,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0
                                      )
    
    return output["choices"][0]["text"].strip()

# for chunk in chunks:
#     print(chunk)



# prompt = "Explain briefly for begginners."

# prompt = "what is DM2 numerator criteria and denominator criteria"

prompt = "what is demoinator exclusion and what are denominator excusion criteria for DM2 measure"

for chunk in chunks:
    print(get_summaries_from_transcript(chunk, prompt, is_test=False), "\n")