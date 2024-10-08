import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    # Setup ChromeDriver
    options = webdriver.ChromeOptions()
    options.headless = True  # Run in headless mode
    driver = webdriver.Chrome(
        service=Service(chromedriver_autoinstaller.install()), options=options
    )
    yield driver
    driver.quit()


def test_profile_submission(driver):
    # Navigate to the Dash app
    driver.get("http://localhost:8050")

    # Wait for the input element to be ready
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "profile-url-input"))
    )

    # Find the profile URL input and submit button
    profile_input = driver.find_element(By.ID, "profile-url-input")
    submit_button = driver.find_element(By.ID, "submit-button")

    # Enter a URL and submit
    profile_input.send_keys(
        "https://www.goodreads.com/user/show/66681479-lucas-pavanelli"
    )
    submit_button.click()

    # Wait for the graph to become visible  
    WebDriverWait(driver, 1000).until(
        EC.visibility_of_element_located((By.ID, "visualization-output"))
    )

    # Check if the graph is displayed
    graph = driver.find_element(By.ID, "visualization-output")
    style = graph.get_attribute("style")
    assert "display: block" in style, "Graph should be visible after submission"

    # Optional: Check for additional details in the graph
    # For example, validate that the graph has expected data points or labels


def test_invalid_url(driver):
    # Navigate to the Dash app
    driver.get("http://localhost:8050")

    # Wait for the input element to be ready
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "profile-url-input"))
    )

    # Find the profile URL input and submit button
    profile_input = driver.find_element(By.ID, "profile-url-input")
    submit_button = driver.find_element(By.ID, "submit-button")

    # Enter an invalid URL (e.g., without "https://www.goodreads.com/user/show/")
    profile_input.send_keys("invalid_url")
    submit_button.click()

    # Wait for the message output to become visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message-output"))
    )

    # Check if the error message is displayed
    message = driver.find_element(By.ID, "message-output").text
    assert (
        "Status code: 422" in message
    ), "Error message should be displayed for invalid profile URL"


def test_invalid_goodreads_profile(driver):
    # Navigate to the Dash app
    driver.get("http://localhost:8050")

    # Wait for the input element to be ready
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "profile-url-input"))
    )

    # Find the profile URL input and submit button
    profile_input = driver.find_element(By.ID, "profile-url-input")
    submit_button = driver.find_element(By.ID, "submit-button")

    # Enter an invalid URL (e.g., without "https://www.goodreads.com/user/show/")
    profile_input.send_keys("https://www.youtube.com/watch?v=jRESgqJIsoo")
    submit_button.click()

    # Wait for the message output to become visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message-output"))
    )

    # Check if the error message is displayed
    message = driver.find_element(By.ID, "message-output").text
    assert (
        "Status code: 500" in message
    ), "Error message should be displayed for invalid profile URL"
