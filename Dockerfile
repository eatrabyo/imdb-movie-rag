FROM python:3.12

WORKDIR /imdb-movie-rag


COPY ./requirements.txt /imdb-movie-rag/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /imdb-movie-rag/requirements.txt


COPY . /imdb-movie-rag

EXPOSE 80
CMD ["uvicorn", "router:app", "--host","0.0.0.0","--port", "80"]