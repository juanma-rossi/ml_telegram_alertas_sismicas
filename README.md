# ETL and Machine Learning Project

This repository contains the code and documentation for a Machine Learning project focused on earthquake classification. The project involves data extraction, transformation, and loading (ETL) processes from various websites in real-time and historical data. Additionally, it includes the implementation of classification models for earthquake prediction and the deployment of the models on Amazon Web Services (AWS) for remote access.

## Data Sources

The earthquake data for this project was collected from the following websites in real-time and historical formats:

1. Mexico (BeautifulSoup) - [Servicio Sismológico Nacional, UNAM](http://www.ssn.unam.mx/)
2. USA (GeoJson) - [US Geological Survey (USGS)](https://www.usgs.gov/)
3. Japan (GeoJson) - [US Geological Survey (USGS)](https://www.usgs.gov/)

## Classification Models

For each country, a specific classification model was chosen based on its historical data. The models were trained and saved in .PKL format for later use. The chosen models and their performance metrics are as follows:

### Mexico:
- Model: Decision Tree Classifier (dt)
- Accuracy: 1.0000
- AUC (Area Under the Curve): 0.8000
- Recall: 1.0000
- Precision: 0.9999
- F1 Score: 0.9999
- Kappa: 0.9997
- Matthews Correlation Coefficient (MCC): 0.9997
- Time taken for training (TT): 0.5260 seconds

### USA:
- Model: Support Vector Machine with Linear Kernel (svm)
- Accuracy: 0.9877
- AUC (Area Under the Curve): 0.0000
- Recall: 0.9877
- Precision: 0.9871
- F1 Score: 0.9869
- Kappa: 0.9103
- Matthews Correlation Coefficient (MCC): 0.9141
- Time taken for training (TT): 0.6210 seconds

### Japan:
- Model: K Neighbors Classifier (knn)
- Accuracy: 0.9860
- AUC (Area Under the Curve): 0.9845
- Recall: 0.9860
- Precision: 0.9813
- F1 Score: 0.9835
- Kappa: 0.9613
- Matthews Correlation Coefficient (MCC): 0.9616
- Time taken for training (TT): 0.6700 seconds

## Data Scraping and Error Validation

The project includes the implementation of web scraping in real-time using Python, with a focus on ensuring data congruence and detecting duplicates. The process includes loading the data incrementally to maintain data integrity.

## Model Execution

The trained machine learning models for each country are executed on their respective datasets. The classification results are added to each dataset as a new column named "Earthquake Classification."

## Streamlit Application

A Streamlit application has been created to enable users to remotely run the trained earthquake classification models. The application provides an interactive interface for users to input data and obtain earthquake predictions.

## AWS Deployment

The project files, including the trained models and the Streamlit application, are loaded into an AWS S3 bucket. Subsequently, the models are deployed on an Amazon EC2 virtual machine running Ubuntu. An elastic IP is integrated into the VM to allow continuous remote access to the earthquake prediction information.

Please feel free to explore the code and data in this repository for more details about the ETL process, machine learning models, and the Streamlit application.

**Note:** This README file provides an overview of the project. For detailed instructions on how to run the code and deploy the models on AWS, please refer to the relevant documentation in the repository.

## Contact
If you have any questions or comments, feel free to contact me at juancho.256.8@gmail.com or at [Linkedin](https://www.linkedin.com/in/juan-manuel-rossi-77b578264)
