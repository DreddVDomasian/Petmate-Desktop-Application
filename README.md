
#  Petmate Web Appointment (Dockerized)

This project contains the **Petmate Animal Clinic Web Appointment System**.  
We are using **Docker + Nginx** so everyone in the group can run the same setup without issues.

---
### 1. Install Requirements
- [Docker Desktop]


### 2. Build the Docker Image

Open **PowerShell / Terminal** inside the `Web Appointment` folder:  
```bash

    # SYNTAX TO OH
    #ETO YUNG IMAGE ( BLUEPRINT )
cd "C:\Users\<YOUR_USERNAME>\Documents\Petmate-Management\Web Appointment"
docker build -t petmate-web .


    # RUN THE CONTAINER
docker run -d -p 8080:80 --name petmate-container petmate-web
    #PAG DI GUMANA CLICK MO NALANG SA DOCKER DESKTOP


# STOP AND REMOVE CONTAINER ( CMD )
docker stop petmate-container
docker rm petmate-container



🔄 Updating the App
    # 1 Pull latest changes from GitHub (GitHub Desktop → Fetch/ Pull).

    # 2 Rebuild the image:
docker build -t petmate-web .

    # 3 Stop the old container:
docker stop petmate-container
docker rm petmate-container




# Petmate Desktop Application (Dockerized)


