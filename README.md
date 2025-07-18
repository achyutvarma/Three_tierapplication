# Three_tierapplication

✅ Documented Three-Tier Architecture with ALB for Backend Tier

✅ 1️⃣ High-Level Architecture Recap
Tier	Components
Presentation Tier	Frontend EC2 (Nginx/HTML)
Application Tier	Backend EC2 (Flask app) — Behind ALB
Database Tier	RDS (MySQL) — in private subnet

ALB forwards requests → backend EC2 on port 80

Frontend talks to backend via ALB DNS Name

✅ 2️⃣ Infra Build Process Summary (Adjusted for Backend ALB)
✅ VPC & Subnets
Public Subnets → For ALB and Frontend EC2

Private Subnets → For Backend EC2 and RDS

NAT Gateway → For backend EC2 internet access if required (for updates or pip installs)

✅ Backend ALB Configuration (Key Detail)
1️⃣ Create Target Group

Protocol: HTTP

Port: 80

Health check path: /health

Target Type: Instance → Register backend EC2 instances on port 5000

2️⃣ Create ALB

Internet-facing: Yes

Listeners:

HTTP 80 → Forward to target group

3️⃣ Security Groups

ALB Security Group: Allow HTTP 80 from anywhere

Backend EC2 Security Group: Allow HTTP 5000 from ALB security group only

✅ 3️⃣ Backend EC2 Flask Configuration
Flask app should listen on 0.0.0.0:80

Add /health route as described before

Set environment variables for RDS connection via:


export DB_HOST=<RDS-endpoint>
export DB_USER=admin
export DB_PASSWORD=<password>
export DB_NAME=three_tier_db
Do not expose backend EC2 public IP. Only ALB DNS Name is used to access it.

✅ 4️⃣ Frontend EC2 Configuration
Host static HTML or JS page

Replace backend endpoint in frontend script with Backend ALB DNS Name
Example:
<script>
fetch("http://<backend-ALB-DNS-Name>/data")
Frontend EC2 Security Group: Allow HTTP (80) from anywhere


  ✅ 5️⃣ Validation Process
Check ALB Target Group health → Should show healthy targets.

Open Frontend EC2 public IP or domain → Should display message fetched from backend via ALB.
