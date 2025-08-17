FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG id_ID.UTF-8
ENV LANGUAGE id_ID:id
ENV LC_ALL id_ID.UTF-8

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# id_ID.UTF-8 UTF-8/id_ID.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -c "from deepface import DeepFace; DeepFace.build_model('SFace')"

COPY . .

RUN mkdir -p /app/uploads/photos

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]