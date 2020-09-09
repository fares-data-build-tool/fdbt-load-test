# FDBT Load Test

This repo contains the code necessary to run load tests on the Fares Data Build Tool. It uses [locust](https://locust.io/), a Python-based tool. This can be ran locally or using a remote server if more load is needed than can be generated locally.

## Requirements

- Python 3
- [Locust](https://docs.locust.io/en/stable/installation.html)

## Running locally

- Create a user in Cognito to use for the load test
- Set the env vars `FDBT_LOAD_TEST_USERNAME` and `FDBT_LOAD_TEST_PASSWORD` with the appropriate values or pass them in directly to the following command
- Run `locust` in the folder with the `locustfile.py`, this will start up locust and will run the UI on `http://0.0.0.0:8089`
- Navigate to the local link and you will be asked to input total number of users, spawn rate and the domain, enter appropriate values for all of these and click `Start swarming` to begin the test
- When finished, click `Stop` in the top right corner, if you navigate to the `Download Data` tab, you will be able to retrieve a report for the test
