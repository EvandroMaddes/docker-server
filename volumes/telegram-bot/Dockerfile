FROM python:3.9
RUN mkdir -p src
RUN echo ${PWD}
WORKDIR /src
# Or any preferred Python version.
COPY /src /src
RUN pip3 install python-telegram-bot python-dotenv python-telegram-bot[job-queue]
CMD ["python3", "/src/TelegramNotifierBot.py"]
# Or enter the name of your unique directory and parameter set.