FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
	git \
	curl \
	sudo \
	libwebp-dev \
	redis \
	neofetch \
	libssl-dev \
	libjpeg-dev \
	jq \
	pv

ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
CMD ["bash","./init/start.sh"]
