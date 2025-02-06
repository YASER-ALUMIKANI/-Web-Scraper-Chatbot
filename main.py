from scraper.crawler import crawl_and_scrape
from scraper.embeddings import store_embeddings
from chatbot.chat import chat_with_gpt

# Scrape website and store embeddings
website_data = crawl_and_scrape("https://botpenguin.com/", max_pages=5)
chunks, faiss_index = store_embeddings(website_data)

#TODO: Add more websites to crawl and store embeddings

#TODO: Add more websites to crawl and store embeddings

# Chat loop
while True:
    user_input = input("Ask me anything: \n")
    if user_input.lower() == "exit":
        break
    answer = chat_with_gpt(user_input, chunks, faiss_index)
    print("Chatbot:\n", answer)
    print("----------------------")
