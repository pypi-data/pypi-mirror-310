import os

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from openai import OpenAI
from pinecone import Pinecone


class DsTomato:
    def __init__(self, api_key: str, pinecone_api: str, index_pinecone: str) -> None:
        os.environ['PINECONE_API_KEY'] = pinecone_api
        os.environ['OPENAI_API_KEY'] = api_key
        self.client = OpenAI(api_key=api_key)
        Pinecone(api_key=pinecone_api)
        self.embedding = OpenAIEmbeddings( model='text-embedding-3-small' )
        self.vstore = PineconeVectorStore.from_existing_index(index_name=index_pinecone, embedding=self.embedding)

    def translate_text(
        self,
        text: str,
        lng: str
    ):
        response = self.client.chat.completions.create(
            model = 'gpt-4o-mini-2024-07-18',
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f'Traduce el siguiente texto, el que está en comillas, a {lng} y responde solo con el texto traducido: "{text}"'
                        }
                    ]
                }
            ]
        )
        
        response_translated = response.choices[0].message.content.replace('"', '')
        
        return response_translated

    def send_message( self, prompt: str, url_image = None, id_chat = None, with_memory: bool = False ) -> str:
        
        messages = []
        if with_memory:
            messages = self.get_memory_model(question=prompt, id_chat=id_chat, url_image=url_image)
        
        question_traduction = self.translate_text( text=prompt, lng="inglés" )
        
        if url_image is not None:
            
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question_traduction
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url_image,
                                "detail": "low"
                            }
                        },
                    ]
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question_traduction
                        },
                    ]
                }
            )
            
        response = self.client.chat.completions.create(
            model='ft:gpt-4o-2024-08-06:personal::APjkVqPn',
            messages=messages
        )
        response_traduction = self.translate_text( text=response.choices[0].message.content, lng="español" )
        
        return response_traduction
    
    def get_memory_model(self, question: str, id_chat= None, url_image = None) -> list:
        messages_vectorial = self.vstore.similarity_search( filter={'id_chat': id_chat}, query=question, k=10 )
        
        message_image = None
        messages = []
        
        if url_image is None:
            messages_vectorial_images = self.vstore.similarity_search( filter={ "image": {"$exists": True, "$ne": ""} }, query='' )
            message_image = messages_vectorial_images[-1] if len( messages_vectorial_images ) > 0 else None
            messages.append({
                "role": message_image.metadata['role'],
                "content": [
                    {"type": "text", "text": message_image.metadata['text_en']},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": message_image.metadata['image'],
                            "detail": "low"
                        },
                    },
                ]
            })
        
        for message_data in messages_vectorial:
            messages.append({
                "role": message_data.metadata['role'],
                "content": [
                    {"type": "text", "text": message_data.metadata['text_en']}
                ]
            })
        return messages