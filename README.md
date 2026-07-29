# Bangladeshi Taka Note Detection API

An end-to-end, highly scalable REST API designed to detect and classify Bangladeshi Banknotes. This project leverages an advanced Computer Vision model served through a robust, containerized backend infrastructure.

**Author:** Soumit Dey

## 🚀 Features & Technologies
* **Machine Learning Model:** Fine-tuned **YOLOv11n-cls** (Ultralytics) for high-speed image classification.
* **Backend Framework:** **FastAPI** for building a lightning-fast and asynchronous REST API.
* **Caching Layer:** **Redis** to cache image hashes. If the same image is uploaded again, the API returns the result instantly without re-running the ML model.
* **Load Balancing:** **Nginx** configured with a Round-Robin algorithm to distribute incoming traffic smoothly across multiple application servers.
* **Containerization:** **Docker & Docker Compose** for seamless deployment across any environment.

## 🌍 Real-World Applications
This project can be integrated into various real-world scenarios:
1. **Automated Banking & ATMs:** Verifying deposited banknote denominations automatically in cash deposit machines.
2. **Retail & Point of Sale (POS):** Assisting automated checkout systems in recognizing cash payments.
3. **Visually Impaired Assistance:** Powering mobile applications that help visually impaired individuals identify the value of the physical currency they are holding.
4. **Fintech Solutions:** Automating currency counting and sorting processes in financial institutions.

---

## 🛠️ How to Run This Project Locally

## Prerequisites
Before running this project, ensure you have the following installed on your machine:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)

## How to Run the Project Locally

**Step 1: Clone the Repository**
Open your terminal and clone the repository from GitHub:
```bash
git clone https://github.com/soumit02/FastAPI_Docker_MiniProject.git
cd FastAPI_Docker_MiniProject
```

**Step 2: Start the Containers**
Use Docker Compose to build the images and start all the services (Nginx, Redis, and FastAPI servers) in the background.
```bash
docker-compose up -d --build
```

**Step 3: Access the API**
Once the containers are running, open your browser and navigate to the Swagger UI:
👉 **[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)**