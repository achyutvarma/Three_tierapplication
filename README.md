# ✅ Documented Three-Tier Architecture with ALB for Backend Tier

---

## ✅ 1️⃣ High-Level Architecture Recap

### Tier Components:

- **Presentation Tier:**  
  Frontend EC2 (Nginx/HTML)

- **Application Tier:**  
  Backend EC2 (Flask app) — Behind ALB

- **Database Tier:**  
  RDS (MySQL) — In private subnet

- **Flow:**  
  ALB forwards requests → Backend EC2 on port 80  
  Frontend talks to backend via ALB DNS Name

---

## ✅ 2️⃣ Infra Build Process Summary (Adjusted for Backend ALB)

### VPC & Subnets:

- **Public Subnets:**  
  For ALB and Frontend EC2

- **Private Subnets:**  
  For Backend EC2 and RDS

- **NAT Gateway:**  
  For Backend EC2 internet access if required (for updates or pip installs)

---

## ✅ Backend ALB Configuration (Key Detail)

### 1️⃣ Create Target Group:

- Protocol: **HTTP**
- Port: **80**
- Health Check Path: `/health`
- Target Type: **Instance** → Register Backend EC2 instances on port 5000

### 2️⃣ Create ALB:

- Internet-facing: **Yes**
- Listeners:
  - **HTTP 80** → Forward to target group

### 3️⃣ Security Groups:

- **ALB Security Group:** Allow HTTP 80 from anywhere
- **Backend EC2 Security Group:** Allow HTTP 80 from ALB security group only

---

## ✅ 3️⃣ Backend EC2 Flask Configuration

- Flask app should listen on:  
  **0.0.0.0:80**

- Add `/health` route as described before.

- Set environment variables for RDS connection:
  ```bash
  export DB_HOST=<RDS-ENDPOINT>
  export DB_USER=admin
  export DB_PASSWORD=<password>
  export DB_NAME=three_tier_db

Important:
Do not expose Backend EC2 public IP.
Only ALB DNS Name is used to access it.

Set env variables: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
Install Python and requirements

Make sure you have nat gateway:

NAT Gateway: In public subnet, attached to Elastic IP.
Route Table: Private subnet route → 0.0.0.0/0 via NAT Gateway.

## ✅ 4️⃣ Frontend EC2 Configuration
Host static HTML or JS page.

Replace backend endpoint in frontend script with Backend ALB DNS Name:
<script>
    fetch("http://<backend-alb-dns>/data")
</script>

Frontend EC2 Security Group:
Allow HTTP (80) from anywhere.

Install Nginx, place index.html under /var/www/html/

Update the <backend-ip> in index.html to your backend private IP

## ✅ 5️⃣ Validation Process
Check ALB Target Group Health:
Should show healthy targets.

Open Frontend EC2 Public IP or Domain:
Should display message fetched from backend via ALB.

## ✅ If You See:

- Blank Page / 404:

Frontend server might not be running or configured incorrectly.
Check frontend app logs and verify service is running.

- 502/504 Gateway Timeout:

Likely frontend can’t reach backend or backend can’t reach database.
check security groups, VPC settings, and internal DNS resolution.

- Connection Refused:

Firewall/Security group/Listener missing or port not exposed.

## No data from backend
Welcome to the Three-Tier App!
Loading data from backend...
But no message from backend. That means the fetch() call in your frontend is failing.

# ✅ How to Fix It

- 1️⃣ Update the Fetch URL to Point to the Backend ALB DNS Name
Instead of:
fetch('http://<backend-ip>:5000/data')
Use:
fetch('http://alb-backend-xyz.us-east-1.elb.amazonaws.com/data')
Make sure this backend ALB is accessible from the internet (or at least from wherever you’re opening the frontend).

- 2️⃣ Ensure Backend ALB Listener Is on Port 80 or 443
If the backend ALB only listens on port 80 or 443, do not try to fetch on port 5000 directly. Use only:

http://alb-backend-xyz.us-east-1.elb.amazonaws.com/data
- 3️⃣ Ensure CORS Settings Allow Frontend Requests
If the backend is Flask, you need CORS headers.
Install Flask-CORS in your backend:

pip install flask-cors
In app.py:

from flask_cors import CORS
app = Flask(__name__)
CORS(app)
That allows browsers to fetch from different origins without blocking.

## Mysql commands:
Connect to 
mysql -h rds-endpoint -u admin -p
Step-by-Step SQL Command:
- 1️⃣ Log in to MySQL:
mysql -u <username> -p

- 2️⃣ Select your database:
  USE three_tier_db;
  
- 3️⃣ Insert a new row:
INSERT INTO messages (message) VALUES ('This is a new message!');

- 4️⃣ Verify it was added:
SELECT * FROM messages;

# Note:
- To connect to ec2 in private subnet use ssh -i "keypair.pem" ubuntu@privateip from public subnet make sure the backensg have access from frontend-sg from 22.

- Also make sure the rdsg has inbound access port 3306 from backend-sg


