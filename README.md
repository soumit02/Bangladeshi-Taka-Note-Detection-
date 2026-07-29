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
git clone https://github.com/soumit02/Bangladeshi-Taka-Note-Detection-.git
cd Bangladeshi-Taka-Note-Detection
```

**Step 2: Start the Containers**
Use Docker Compose to build the images and start all the services (Nginx, Redis, and FastAPI servers) in the background.
```bash
docker-compose up -d --build
```

**Step 3: Access the API**
Once the containers are running, open your browser and navigate to the Swagger UI:
👉 **[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)**

##  How to Use the API Endpoint

Once the containers are running, the API is accessible via the Nginx load balancer at `http://localhost:8080`. You can interact with the `/predict` endpoint using Swagger UI (Browser), Postman, or cURL.

### Method 1: Using Swagger UI (Browser - Easiest)
1. Open your web browser and navigate to: `http://localhost:8080/docs`
2. Click on the green `POST /predict` endpoint to expand it.
3. Click the **"Try it out"** button on the right side.
4. In the `file` field, click **"Choose File"** and select a Bangladeshi Taka image from your computer.
5. Click the large blue **"Execute"** button.
6. Scroll down to the "Responses" section to see the JSON output.

### Method 2: Using Postman (GUI)
1. Open the Postman application and create a new request.
2. Change the HTTP method to **`POST`**.
3. Enter the endpoint URL: `http://localhost:8080/predict`
4. Go to the **Body** tab below the URL bar.
5. Select the **form-data** option.
6. In the **Key** column, type `file`. Hover over the right edge of this cell and change the type from `Text` to **`File`**.
7. In the **Value** column, click "Select Files" and choose an image.
8. Click the blue **Send** button.

### Method 3: Using cURL (Command Line)
If you prefer using the terminal, you can send an image directly using the `curl` command. Open your terminal and run the following command (make sure to replace `path/to/your/image.jpg` with the actual image path):

```bash
curl -X POST "http://localhost:8080/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"