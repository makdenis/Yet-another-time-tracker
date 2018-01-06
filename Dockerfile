FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r bot_requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV BOT_ENV prod
ENV TZ=Europe/Moscow

# Setting up correct datetime for moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Run app.py when the container launches
CMD ["python3", "bot.py"]