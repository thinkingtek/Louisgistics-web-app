1. Project Overview

   - Project Name: Louisgistics Web App.
   - Description: This is a Logistics Web App, Django-based application designed to streamline logistics and supply chain management. It provides tools for managing inventory, orders, shipments, and delivery schedules, making it easier for businesses to operate efficiently.
   - Purpose: Its main purpose is to make sure ordinary users can track their shipments.
   - Link to Demo: My github link ( https://github.com/thinkingtek/Louisgistics-web-app.git )

2. Installation

   - Clone the repository:
     git clone https://github.com/thinkingtek/Louisgistics-web-app.git

   - Change directory:
     cd yourproject

   - Create a virtual environment
     python -m venv env
   - Activate the virtual environment
     .\env\Scripts\activate (for windows)
     source env/bin/activate (for Mac)

   - Install dependencies:
     pip install -r reqs.txt

   - Set up the database:
     python manage.py migrate

3. Usage

   - Run "python manage.py runserver" to run the project

4. Instructions

   - After setup make you create three groups (customer, staff and admin), although not functions for admin yet.
   - Staffs can be manually added through the Django admin page.

5. Features

   - Web page responsive for both mobile, and desktop screens
   - Styled Django admin panel in css only
   - User creation, authentication, password reset
   - Users can enter their tracking ID to see the status of their package or shipment.
   - Any staff is allowed to update any shippment, but cannot delete any shipment he didn't register, except for the admins. This is done to prevent other staffs from full manipulation of other staffs records.
   - Staffs can see the last person who updated a shipment and time of update in the update form.
   - Tracking: Monitor the movement of goods with detailed tracking and status updates.
   - Contact form page for users to communicate or send emails to the company
   - small letter case is enforced for email while title case for first & last name in login and signup page, done in both frontend and backend
   - Registered users can see all their shipments made with the company (this feature can be added later)
   - Unit testing can be added later

6. Testing

   - "python manage.py test"

7. Created Accounts

   -------- ACCOUNTS -----------
   username: testuser
   email: testuser@gmail.com
   password: mypass123

   username: superuser
   email: superuser@gmail.com
   password: mypass123

   testuserpass (password for all ordinary user accounts)
