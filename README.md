# Bangladeshi Taka Note Prediction System

An end-to-end, highly scalable Machine Learning Web Application and REST API designed to detect and classify Bangladeshi Banknotes. This project leverages an advanced Computer Vision model served through a robust, containerized backend infrastructure with an interactive and user-friendly frontend.

**Author:** Soumit Dey

---

## 📸 Live Interactive UI
Users can easily upload banknote images and instantly get predictions along with confidence scores directly from the web interface. 

![Live Demo UI](sample_images\UI_10.png)

---

## 🚀 Features & Technologies
* **Interactive Frontend UI:** A beautifully designed HTML/CSS interface allowing users to test the model seamlessly without needing third-party tools.
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

### Prerequisites
Before running this project, ensure you have the following installed on your machine:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)


**Step 1: Clone the Repository**
Open your terminal and clone the repository from GitHub:
```bash
git clone https://github.com/soumit02/Bangladeshi-Taka-Note-Detection-.git
cd Bangladeshi-Taka-Note-Detection-
```

**Step 2: Start the Containers**
Use Docker Compose to build the images and start all the services (Nginx, Redis, and FastAPI servers) in the background.
```bash
docker compose up -d --build
```

**Step 3: Access the Web App & API**
Once the containers are running, open your browser:
👉 **Web Application UI:** [http://127.0.0.1:8080](http://127.0.0.1:8080)  
👉 **Developer API Docs (Swagger UI):** [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

---

## 🌐 Live Cloud Deployment (Try it now!)

The System is publicly deployed and accessible 24/7 via Render. You do not need to install Docker or run any code to test it.

👉 **Live Web Application:** [https://bangladeshi-taka-note-detection-mchz.onrender.com](https://bangladeshi-taka-note-detection-mchz.onrender.com)

> **⚠️ Note Regarding First-Time Loading (Cold Start):**
> Because this application is deployed on Render's free tier, the web service automatically spins down (goes to sleep) after a period of inactivity. As a result, **accessing the live link for the first time may take around 30 to 60 seconds to respond** while the server wakes up. Once the server is fully active, it will work instantly.

### Developer API Testing
If you want to interact with the raw `/predict` API endpoint instead of the UI, you can use the following methods:

**Method 1: Using Postman**
1. Open Postman and create a new **`POST`** request.
2. Enter the Live URL: `https://bangladeshi-taka-note-detection-mchz.onrender.com/predict`
3. Under the **Body** tab, select **form-data**.
4. Set the Key as `file` (change type to **File**) and upload your image.
5. Click **Send**.

**Method 2: Using cURL**
```bash
curl -X POST "[https://bangladeshi-taka-note-detection-mchz.onrender.com/predict](https://bangladeshi-taka-note-detection-mchz.onrender.com/predict)" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```