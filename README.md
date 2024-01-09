## Sud.DL
This study successfully constructed a website using open-source tools, centered on simplifying the deployment of NLP deep learning tasks. While ensuring multifunctionality and user-friendliness, the platform also notably reduced user challenges both in terms of deployment functionality usage and its associated learning curve. 


### Content
In this project, Python Django, PyTorch, Transformers, JavaScript, Docker, and Alibaba Cloud are used to build the SUD.DL. Following the Django project structure, the detailed back-end code can be found in the 'deeplearningapp' file. In addition, the front-end code and related files can be found in the 'statics' and 'templates' files. Additionally, it is noted that all models in the 'model' file do not include the corresponding model bin file, as the size of these files is too large. If you want to use the model bin files, you can download them on the Hugging Face. If you want to learn how to use the Sud.DL from scratch, you can watch the 'showcase.mp4' stored in this GitHub repository.


### Experiment Result
By setting up Sud.DL, against the prevalent no-code deep learning deployment solution, Hugging Face, undertook comparative experiments and surveys. Data-driven analysis was employed to discern the
tangible advancements of Sud.DL over its counterpart. The results confirmed that SUD.DL has made significant strides in aesthetics, facilitating users to easily locate deployment-related functions and reducing the learning curve and comprehension difficulty associated with deployment tutorials. Although there’s room for further optimization in model deployment times and the complexity of the development process, Sud.DL achieved commendable outcomes in overall user satisfaction.


### As a user, how to run the Sud.DL? It is very simple!!!
First step: Open this link (http://8.208.32.153:8000/signup/) to register your account. eg: example@ucl.ac.uk.

Second step: On the Sud.DL, open the deployment functionality and follow the guidelines for model deployment (If you need detailed guidelines, you can click 'How To Deploy' functionality).

Third step:  Find and test your model on the Use Models Page.  


### As a developer, if you want to download this webapp and optimise it, please follow these steps
First step: Clone all code to your local environment and install relevant dependencies. Some important dependencies are mentioned below.
Python 3.9  
Django 4.2.1  
transformers 4.18.0  
werkzeug 2.3.6  
docker 6.1.3  

Second step: Download the Docker Desktop and open it (Make sure you have a virtual environment in docker before you run the project to ensure that python interacts correctly with the Docker Desktop).

Third step: In your Python environment, run the Sud.DL (type python manage.py runserver 0.0.0.0:8000 in CMD), and then you can open Sud.DL in your browser and upload your NLP model.


