# LinkED

LinkED is a feature-rich social media web application built with Flask, allowing users to connect, share posts with images, like and comment on content, and manage their profiles seamlessly. The application leverages Flask-SocketIO for real-time interactions and Cloudinary for image uploads, ensuring a dynamic and responsive user experience.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **User Authentication**
  - Sign up with username, password, and optional profile picture.
  - Secure login/logout functionality.

- **User Profiles**
  - View and edit personal profiles.
  - Display user information, connections, posts, likes, and comments.

- **Posts**
  - Create posts with text and image uploads.
  - View a feed of posts from connections.
  - Like, comment, and share posts.

- **Connections**
  - Add and manage connections with other users.
  - View a list of connections with their profiles.

- **Real-Time Interactions**
  - Utilize Flask-SocketIO for real-time updates and notifications.

- **Image Handling**
  - Upload and store images using Cloudinary.

- **Responsive Design**
  - User-friendly interface optimized for various devices.

## Demo

![LinkED Screenshot]()

*Replace the above URL with an actual screenshot of your application.*

## Technologies Used

- **Backend**
  - [Flask](https://flask.palletsprojects.com/) - Web framework
  - [Flask-SocketIO](https://flask-socketio.readthedocs.io/) - Real-time communication
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Database migrations
  - [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
  - [Cloudinary](https://cloudinary.com/) - Image upload and management

- **Frontend**
  - HTML5 & CSS3
  - JavaScript (ES6)
  - [Font Awesome](https://fontawesome.com/) - Icons
  - [jQuery](https://jquery.com/) - DOM manipulation

- **Database**
  - SQLite

## Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/)
- [Cloudinary Account](https://cloudinary.com/) for image uploads

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/LinkED.git
   cd LinkED
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add the following:

   ```env
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
   CLOUDINARY_API_KEY=your_cloudinary_api_key
   CLOUDINARY_API_SECRET=your_cloudinary_api_secret
   ```

   *Replace the placeholders with your actual Cloudinary credentials and a strong secret key.*

5. **Initialize the Database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the Application**

   ```bash
   flask run
   ```

   The application will be accessible at `http://localhost:5000`.

## Configuration

- **Cloudinary**

  Ensure you have a Cloudinary account and replace the placeholder values in the `.env` file with your actual Cloudinary credentials.


## Usage

1. **Sign Up**

   - Navigate to the [Sign Up](http://localhost:8080/signup) page.
   - Enter a unique username, password, and an optional URL for your profile picture.
   - Submit the form to create a new account.

2. **Login**

   - Navigate to the [Login](http://localhost:8080/login) page.
   - Enter your credentials to access your dashboard.

3. **Home Feed**

   - View posts from your connections.
   - Scroll to load more posts dynamically.
   - Interact with posts by liking, commenting, or sharing.

4. **Profile**

   - Access your profile to view your posts, connections, likes, and comments.
   - Edit your profile information if it's your own profile.

5. **Connections**

   - Add new connections by se1ing for usernames.
   - View and manage your list of connections.

6. **Likes and Comments**

   - Like posts to show appreciation.
   - Comment on posts to engage with content.

## Folder Structure

```
LinkED/
├── main.py
├── models.py
├── routes.py
├── socket_handler.py
├── requirements.txt
└── /templates/
   ├── layout.html
   ├── index.html
   ├── login.html
   ├── signup.html
   ├── profile.html
   ├── post.html
   └── likes.html
```

- **main.py**: Initializes the Flask application and sets up configurations.
- **models.py**: Defines the database models using SQLAlchemy.
- **routes.py**: Contains all the route definitions and view functions.
- **socket_handler.py**: Manages real-time socket connections.
- **templates/**: Holds all HTML templates for rendering views.
- **static/**: Contains static assets like CSS, JavaScript, and images.

*Note: Adjust the folder structure as per your actual project setup.*

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**



## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [Cloudinary](https://cloudinary.com/)
- [Font Awesome](https://fontawesome.com/)
- [jQuery](https://jquery.com/)

---

Feel free to customize this README to better fit your project's specifics and add any additional sections or information as needed.
