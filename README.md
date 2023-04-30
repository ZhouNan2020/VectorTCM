# Vector-TCM
# Readme

👋 Welcome to Vector-TCM, a powerful platform for traditional Chinese medicine (TCM) data mining! 🌿📊

Vector-TCM uses text vectors as the basic data form and natural language processing (NLP) technology for TCM data mining. This desktop version of Vector-TCM is perfect for data mining in traditional Chinese medicine. However, if you prefer to access the WebAPP directly, you can click on this link [https://vector-tcm.streamlit.app/](https://vector-tcm.streamlit.app/).

## Original Data Form

The original data must be submitted as a text vector, as shown in the following example:

| index | text |
| --- | --- |
| Prescription name | herb name1, herb name2, herb name3, ... |

Note the following:

- Only .xlsx format worksheets are supported. 🖥️
- The interval between herb names must be commas in English format. If your original data is not like this, it is recommended to use regular expressions to adjust it. 🧐
- There is no limit to the naming of the title row of the worksheet, but there must be this row. 📑
- You need to clean the data yourself, using regular expressions, manual or any other method you are familiar with. 🧹
- We provide sample data for download. You can use it to arrange your own data. 📂

## Analysis Modules

This software includes the following modules: Descriptive statistics, Prescription similarity, General analysis, LSA topic distribution, LDiA topic distribution, and Word2Vec model. Each module performs different analysis tasks respectively. 📈

### Descriptive Statistics

Descriptive statistics is used in the same sense as descriptive statistics in any other analytical context, presenting the researcher with the most immediate information in the data set. It is a good starting point for any analysis. 📊

### Prescription Similarity

Prescription similarity is used to calculate the similarity between prescriptions. Two vector distance calculation methods are mainly used here, dot product value and cosine similarity. The dot product value reflects the absolute quantity of the same herbal medicine used in different prescriptions, and the cosine similarity reflects the relative similarity of different prescriptions. The maximum value is 1, which means they are exactly the same, and the minimum value is 0, which means they do not use any of the same herbs. 🌿

### General Analysis

General analysis is a method of calculating rare herbal medicines and common herbal medicines in the data set based on the TF-IDF value. The average TF-IDF value of each prescription is obtained by calculating the TF-IDF value of each herb. We can use it to tell whether a prescription's herbal composition is extremely rare or very common. And further learn in this data set, what is the mainstream prescription composition. 🧐

### LSA Topic Distribution and LDiA Topic Distribution

LSA topic distribution and LDiA topic distribution are two topic classification methods commonly used in Natural Language Processing (NLP) to divide text into different categories. We still use them here to perform classification tasks, the purpose is to provide more alternative methods for the classification of TCM datasets (different from traditional two-step clustering and system clustering). 📑

We hope you enjoy using Vector-TCM for your TCM data mining needs! 🌿🔎
 
