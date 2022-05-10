# KEPIA_2576183S

## About

Kidney Exchange Programs (KEP) are part of the healthcare system that finds allocations of kidney donors to a pool of patients and increases the rate of living- donor kidney transplantations. The kidney patient or recipient is part of an incompatible donor-recipient pair and can find a suitable match from the pairwise exchange or an altruistic donor. A KEP instance contains medical data of donors, recipients, and clinically approved donor- recipients matchings. These instances are input to the kidney exchange allocator that returns the set of exchanges (transplantations) that should take place. However, given how direct this entire process seems, learning about the multiple data sets is usually not straightforward. A web-based application, Kidney Exchange Program Instance Analyser (KEPIA), was built to statistically analyse KEP instances sets. This automated, exploratory data analysis tool caters to identifying potentially correlated variables or parameters within the instances sets. Doing so can both deliver insights into the properties of real-world programs and improve the generation and simulation of random KEP instances by more accurately modelling said real-world programs.



## Project Structure and setup

There are two folders and two .ipynb files

1. Data Folder contains the file require to execute the analysis
-> single_instance.json to run single instance analysis
-> multiple_instance.zip to run multiple analysis

2. KEPIA_code
It contains the source code for the execution of the application in local, the README file in the folder has an explanation of how to setup the code in local and execute it

Apart from this it contains, two Colab notebooks, which contains all the analysis for single instance and multiple instances respectively. These notebooks are pre executed and presented.
3. single_instance.ipynb
4. multiple_instance.ipynb

However  to run these notebooks mocked data is required, Please upload the folder(given in the shared link below) in your 'MyDrive' directory of Google Drive

https://drive.google.com/drive/folders/1yLSyI-KRi9SBjt7B8rwcOHmfx3pygEvM?usp=sharing

Please verify the folder structure should be as follows when uploaded to Drive -
 /content/drive/MyDrive/KEPIA_2576183S/Data/
