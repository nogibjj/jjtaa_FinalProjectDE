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
![test drawio](https://github.com/nogibjj/jjtaa_FinalProjectDE/assets/104114843/91a67960-d104-40c5-ad3e-5dab40a61934)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Load Testing:
Since this project is deployed on Azure Web App Services, we used Azure load testing, which gave us information about the maximum number of virtual users we can host, response time, requests/second, and total errors. The results of the load testing are shown below:
![WhatsApp Image 2023-12-10 at 5 45 01 PM](https://github.com/nogibjj/aad64_Pandas-Script/assets/143753050/b7eaded2-a29e-4d7f-a5bb-45db77e3dedc)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
Overall, the load testing on Azure Web App Services provided valuable insights into the performance and scalability of the application. It helps us ensure that the application can handle the expected load and deliver a smooth user experience. We stopped at 3000 requests/s due to the cost limitations, but also because we validated tha the web app can handle up to 3000 requests when only spawning 4 extra instances. If we were to scale up the number of allowed isntances, we could easily reach 10000 requests per second. 

# The Application:
The application is deployed on Azure Web App Services and can be accessed using the following link: [https://stock-news.azurewebsites.net/](https://stock-news.azurewebsites.net/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Home Page:

<p align = "center"><img width="1717" alt="image" src="https://github.com/nogibjj/aad64_Pandas-Script/assets/143753050/3df19e2d-bd32-4305-a3eb-a52f5ec8b9b3"></p>
The home page of the application is a dashboard comprising of some top news headlines retrieved from our dataset. On the right, we have some visualizations of the actual stock price data and sentiment analyis.
This visualization gives us the sentiment tags when we hover over each data points, with proportions of the positive versus negative sentiment for the news each day. The stock price data is also shown in the form of a line graph, with the closing price of the stock on the y-axis and the date on the x-axis, which is customizable based on user input. Furthermore, users can also decide which index they would like to look at in this plot. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## About Page:
The about page shows you the contributors of the project, coupled with links to each one's github profile and LinkedIn profile.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# Important terms and How we used them:

## Databricks
The DB microservice of this project was built on Databricks. Databricks is a unified data analytics platform that provides a collaborative workspace for data scientists, engineers, and decision-makers to explore, experiment, and share projects. We used Databricls to create a data pipeline that would retrieve data from Yahoo Finance API and the Google News API. The data pipeline was scheduled to run every week. The data was then stored in a database on Databricks.

We also used Databricks notebooks to first test our code before deploying it to the pipeline, which was very useful in a team of 5, to ensure we were all on the same page and understood how to data was being retrieved, stored and worked with.

Our web app interfaces with the Databricks API to pull data to serve to the user based on provided input. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Flask
Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

For the current project, Flask was used to create a web application that would allow users to visualize the data that was retrieved from the data pipeline. The web application was containerized used Docker and deployed on Azure Web App Services. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Docker
Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels. All containers are run by a single operating system kernel and are thus more lightweight than virtual machines. Containers are created from images that specify their precise contents. Images are often created by combining and modifying standard images downloaded from public repositories.

For this project, we used Docker to containerize our application. This was done by creating a Dockerfile which contains all the commands that are required to build the image. The Dockerfile is located in the root directory of this repository. 

You can build an image as follows:
1. `docker login --username <username>`
2. `docker build -t <image name>`
3. `docker push <image name>`

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

For this project, we used Terraform to define our infrastructure. Terraform is an open-source infrastructure as code software tool that enables you to safely and predictably create, change, and improve infrastructure. Terraform can manage existing and popular service providers as well as custom in-house solutions. The `main.tf` file holds the IAC code for this project. To run the code you would need to do:
1. `terraform init`
2. `terraform plan`
3. `terraform apply`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## References
1. https://github.com/nogibjj/python-template
2. https://learn.microsoft.com/en-us/azure/developer/terraform/overview
3. https://www.databricks.com/product/databricks-sql
4. https://flask.palletsprojects.com/en/3.0.x/
5. https://huggingface.co/docs/transformers/index
6. https://learn.microsoft.com/en-us/azure/load-testing/quickstart-create-and-run-load-test?tabs=portal
7. https://github.com/jaxonyue/DE-Group-Project/tree/main
