FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# NTLK data for Rake
RUN python -m nltk.downloader stopwords punkt punkt_tab averaged_perceptron_tagger_eng -d /usr/share/nltk_data
ENV NLTK_DATA=/usr/share/nltk_data

CMD ["bash"]