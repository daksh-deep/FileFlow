# FileFlow : The File Sharing App
Seemless file sharing web application that enables the user to upload, store, preview and download files from the server.
## Getting Started
### Features
- Home Page: The home page welcomes users to the FileFlow web-application. Offers quick links to upload page, download page and about page.
- Upload Page: Lets the user upload there files on server
- Download/document Page: Displays a table of uploaded files with details and actions
- About Page: Provides information about the project, technologies used, and the author.
- Error Handling Page(404): This provides a custom error handler designed specially for Page Not Found Errors.
### Prerequisites
- Python
```
https://www.python.org/downloads/
```
- Flask
```
pip install Flask
```
- Werkzeug
```
pip install Werkzeug
```
- Jinja2
```
pip install Jinja2
```
### Running the Application
As of now, the application is configured to only run on the localserver at port 5000. If 
connected to a wi-fi, all the devices connected to the same network can access the 
application by going on http://localhost:5000/ while the server runs on the machine 
(here refer to desktop / laptop)
- Step 1: Go to the directory where all required files, templates, statics are saved.
- Step 2: Run Command Prompt in that directory
- Step 3: Type the following code to run the python development server
```
>>> python app.py --host=0.0.0.0 --port=5000
```
### Versioning
First number in the version denotes the current iteration of Major Release. Second 
Number denotes the iteration of Minor Release. The third is an alphabet denoting the 
month of release.

```v1.4.D```
- Major Release: 1
- Minor Release: 4
- Month of publish: December (D)
In case of overriding of month alphabets, proper name will be used.
For publishes in June, July: v1.4.June or v1.4.July will be used.

### Additional Information
Dive into the detailed documentation to grasp the intricacies of the project. From routes to templates, it's all there!
```
Check ProjectDocumentation.pdf in project files (v1.1.D) 
```

### Conclusion
Thank you for exploring our File Sharing Web Application. If you have any questions 
or encounter issues, feel free to reach out. We strive to provide a seamless and 
user-friendly experience for file transfer and storage. Your feedback is valuable to us. 
Happy sharing!

### Authors
* **Daksh Deep Saxena** - *Project Developer* - [LinkedIn](https://www.linkedin.com/in/daksh-deep-791a1a298/) - [GitHub](https://github.com/DakshSaxena)

### Copyrights
Idea, code & logic of this project belong to the author. Copy of any of these thing will be considered a copyright infringement.  
© All rights reserved by the author. 
