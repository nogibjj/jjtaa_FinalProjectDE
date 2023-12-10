# Data Engineering Final Project: Stock Price Visualization and Sentiment Analysis
[![Install](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/install.yml/badge.svg)](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/install.yml)
[![Format](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/format.yml/badge.svg)](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/format.yml)
[![Lint](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/lint.yml/badge.svg)](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/lint.yml)
[![Test](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/test.yml/badge.svg)](https://github.com/nogibjj/jjtaa_FinalProjectDE/actions/workflows/test.yml)

## Team Members:
- Javier Cervantes
- Aarya Desai
- Tianji Rao
- Jeremy Tan
- Adler Viton


# Overview
<a name="readme-top"></a>

## Project Description:
This project was aimed at incorporating all the skills we learned over this semester in Data Engineering (IDS 706) with Professor Noah Gift. We decided to create a dashboard that would allow users to visualize stock price data and sentiment analysis from news headlines every week. This was done using a data pipeline which was scheduled to retrieve data on a weekly basis from Yahoo Finance API and the Google News API. For this project, we used the following technologies:
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) 
- ![CSS](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
- ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) with DataBricks
- ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
- ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
- CI/CD Pipelines
- IaC (Infrastructure as Code)
In the following sections, we will go through each of these components in detail.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Project Architecture:
<p align = "center"><img width="803" alt="Screenshot 2023-12-10 at 10 51 44 AM" src="https://github.com/nogibjj/aad64_Individual_Project_4/assets/143753050/87e424cc-ca48-4ff3-b23b-9fd8ceddcd60"></p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Load Testing:
Since this project is deployed on Azure Web App Services, we used Locust to perform load testing. Locust is an open-source load testing tool that is used to test the performance of web applications. It is very easy to use and can be run from the command line. The code for the load testing is located in the `locustfile.py` file. The results of the load testing are shown below:

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# The Application:
The application is deployed on Azure Web App Services and can be accessed using the following link: [https://stockpricevisualization.azurewebsites.net/](https://stockpricevisualization.azurewebsites.net/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Home Page:

<img src = ""></img>
The home page of the application is a dashboard comprising of some top news headlines retrieved from our dataset. On the right, we have some visualizations of the actual stock price data and sentiment analyis.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## About Page:

<img src = ""></img>
The about page shows you the contributors of the project, coupled with links to each one's github profile and LinkedIn profile.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# Important terms and How we used them:

## Databricks
The foundation of this project was built on Databricks. Databricks is a unified data analytics platform that provides a collaborative workspace for data scientists, engineers, and decision-makers to explore, experiment, and share projects. We used Databricls to create a data pipeline that would retrieve data from Yahoo Finance API and the Google News API. The data pipeline was scheduled to run every week. The data was then stored in a database on Databricks.

We also used Databricks notebooks to first test our code before deploying it to the pipeline, which was very useful in a team of 5, to ensure we were all on the same page and understood how to data was being retrieved, stored and worked with.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Flask
Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

For the current project, Flask was used to create a web application that would allow users to visualize the data that was retrieved from the data pipeline. The web application was containerized used Docker and deployed on Azure Web App Services. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Docker
Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels. All containers are run by a single operating system kernel and are thus more lightweight than virtual machines. Containers are created from images that specify their precise contents. Images are often created by combining and modifying standard images downloaded from public repositories.

For this project, we used Docker to containerize our application. This was done by creating a Dockerfile which contains all the commands that are required to build the image. The Dockerfile is located in the root directory of this repository. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Azure Web App Services
Azure App Service is a fully managed web hosting service for building web apps, mobile back ends, and RESTful APIs. It provides out-of-the-box authentication and authorization support, lets you easily add push notifications to your app, and provides production debugging tools. Azure App Service enables you to build and host web apps, mobile back ends, and RESTful APIs in the programming language of your choice without managing infrastructure. It offers auto-scaling and high availability, supports both Windows and Linux, and enables automated deployments from GitHub, Azure DevOps, or any Git repo.

For this project, we used Azure Web App Services to deploy our application. This was done by creating a resource group and a web app service on Azure. We then used the Azure CLI to deploy our application to the web app service. Furthermore, using IaC (Infrastructure as Code), we were able to automate the process of creating the resource group and web app service. The code for this is located in the `main.tf` file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## CI/CD Pipeline
CI/CD stands for Continuous Integration and Continuous Delivery. It is a set of practices that automates the process of building, testing, and deploying code changes. The goal of CI/CD is to enable rapid integration and testing of changes, and to enable continuous delivery of new versions of software.

This repository contains a CI/CD pipeline that is triggered by a push to the main branch. The pipeline is defined in `.github/workflows`. There are multiple files in this folder, each of which defines a different job in the pipeline, namely, installing packages and dependencies, linting, formating, and testing. The badges at the top of README show that all of the jobs are running successfully as well. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Infrastructure as Code
Infrastructure as Code (IaC) is the process of managing and provisioning computer data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. The IT infrastructure managed by this process comprises both physical equipment, such as bare-metal servers, as well as virtual machines, and associated configuration resources. The definitions may be in a version control system. It can use either scripts or declarative definitions, rather than manual processes, but the term is more often used to promote declarative approaches.

For this project, we used Terraform to define our infrastructure. Terraform is an open-source infrastructure as code software tool that enables you to safely and predictably create, change, and improve infrastructure. Terraform can manage existing and popular service providers as well as custom in-house solutions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
