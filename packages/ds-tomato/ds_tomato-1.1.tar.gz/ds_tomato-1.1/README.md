# DsTomato
Librería para el consumo de un modelo entrenado es decir que se le realizo un Fine Tunning, el modelo es multimodal, por lo que procesa imagenes y texto.
El modelo esta especializado en reconocer imagenes del tomate y dar diagnostico requerido.

```
dstomato = DsTomato(
    api_key='API_KEY',
    index_pinecone='index_pinecone',
    pinecone_api='api_secret_pinecone'
)

text = dstomato.send_message(
    prompt='Que logras observar en la imagen',
    url_image='https://upload.wikimedia.org/wikipedia/commons/2/29/Jon_Snow_and_Ghost.jpg'
)

print(text)
```