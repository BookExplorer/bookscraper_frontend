FROM mateusoliveira43/poetry:1.4-python3.10-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy your project files (pyproject.toml and poetry.lock) to the container
COPY pyproject.toml poetry.lock /app/

# Disable Poetry's virtual environment creation because the container itself provides an isolated environment
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Install Chrome for Selenium
RUN apt-get update && apt-get install -y wget gnupg2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Expose debug port, adjust this to match the port in VSCode.
EXPOSE 5679
# Copy the rest of your application's code to the container
COPY . /app
# Command to run the Dash app
CMD ["python", "app.py"]