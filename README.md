# Data Engineering Final Project: Stock Price Visualization and Sentiment Analysis
## Team Members:
- Javier Cervantes
- Aarya Desai
- Tianji Rao
- Jeremy Tan
- Adler Viton

## Project Description:
This project was aimed at incorporating all the skills we learned over this semester in Data Engineering (IDS 706) with Professor Noah Gift. We decided to create a dashboard that would allow users to visualize stock price data and sentiment analysis from news headlines every week. This was done using a data pipeline which was scheduled to retrieve data on a weekly basis from Yahoo Finance API and the Google News API. For this project, we used the following technologies:
- Python, HTML, CSS, JavaScript
- Databricks
- Flask
- Docker
- Azure Web App Services
- Github Actions
- CI/CD Pipelines
- IaC (Infrastructure as Code)
In the following sections, we will go through each of these components in detail.

## Structure of the Repository:

# Important terms and How we used them:

## Databricks
The foundation of this project was built on Databricks. Databricks is a unified data analytics platform that provides a collaborative workspace for data scientists, engineers, and decision-makers to explore, experiment, and share projects. We used Databricls to create a data pipeline that would retrieve data from Yahoo Finance API and the Google News API. The data pipeline was scheduled to run every week. The data was then stored in a database on Databricks.

We also used Databricks notebooks to first test our code before deploying it to the pipeline, which was very useful in a team of 5, to ensure we were all on the same page and understood how to data was being retrieved, stored and worked with.

## Flask
Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

For the current project, Flask was used to create a web application that would allow users to visualize the data that was retrieved from the data pipeline. The web application was containerized used Docker and deployed on Azure Web App Services. 

## Docker
Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels. All containers are run by a single operating system kernel and are thus more lightweight than virtual machines. Containers are created from images that specify their precise contents. Images are often created by combining and modifying standard images downloaded from public repositories.

For this project, we used Docker to containerize our application. This was done by creating a Dockerfile which contains all the commands that are required to build the image. The Dockerfile is located in the root directory of this repository. 

## Azure Web App Services
Azure App Service is a fully managed web hosting service for building web apps, mobile back ends, and RESTful APIs. It provides out-of-the-box authentication and authorization support, lets you easily add push notifications to your app, and provides production debugging tools. Azure App Service enables you to build and host web apps, mobile back ends, and RESTful APIs in the programming language of your choice without managing infrastructure. It offers auto-scaling and high availability, supports both Windows and Linux, and enables automated deployments from GitHub, Azure DevOps, or any Git repo.

For this project, we used Azure Web App Services to deploy our application. This was done by creating a resource group and a web app service on Azure. We then used the Azure CLI to deploy our application to the web app service. Furthermore, using IaC (Infrastructure as Code), we were able to automate the process of creating the resource group and web app service. The code for this is located in the `main.tf` file.

## CI/CD Pipeline
CI/CD stands for Continuous Integration and Continuous Delivery. It is a set of practices that automates the process of building, testing, and deploying code changes. The goal of CI/CD is to enable rapid integration and testing of changes, and to enable continuous delivery of new versions of software.

This repository contains a CI/CD pipeline that is triggered by a push to the main branch. The pipeline is defined in `.github/workflows`. There are multiple files in this folder, each of which defines a different job in the pipeline, namely, installing packages and dependencies, linting, formating, and testing. The badges at the top of README show that all of the jobs are running successfully as well. 


## Infrastructure as Code
Infrastructure as Code (IaC) is the process of managing and provisioning computer data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. The IT infrastructure managed by this process comprises both physical equipment, such as bare-metal servers, as well as virtual machines, and associated configuration resources. The definitions may be in a version control system. It can use either scripts or declarative definitions, rather than manual processes, but the term is more often used to promote declarative approaches.

For this project, we used Terraform to define our infrastructure. Terraform is an open-source infrastructure as code software tool that enables you to safely and predictably create, change, and improve infrastructure. Terraform can manage existing and popular service providers as well as custom in-house solutions.







[![CI](https://github.com/nogibjj/python-ruff-template/actions/workflows/cicd.yml/badge.svg)](https://github.com/nogibjj/python-ruff-template/actions/workflows/cicd.yml)
## Template for Python projects with RUFF linter



## References

![1 1-function-essence-of-programming](https://github.com/nogibjj/python-ruff-template/assets/58792/f7f33cd3-cff5-4014-98ea-09b6a29c7557)

![1 15_rust_built_python_tools](https://github.com/nogibjj/python-ruff-template/assets/58792/db5f7bda-a977-4c67-acbe-a70fe034fbdf)


