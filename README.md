# Chess Master
![AI Is a Master of Games, but How Does It Compare to the Human Mind](ChessAi.webp)

## Master the Chessboard: Play Against Friends or AI!
---

![Chess Master Demo](chess.gif)

# Table of Contents

1. [Introduction](#introduction)
2. [Run Instructions](#run-instructions)
3. [Team Members](#team-members)
4. [Technologies](#technologies)
5. [Alternate Technology Choices](#alternate-technology-choices)
6. [Challenge Statement](#challenge-statement)
7. [Risks](#risks)
8. [Infrastructure](#infrastructure)
9. [Existing Solutions](#existing-solutions)
10. [Chess Master MVP Specification](#chess-master-mvp-specification)
    - [Architecture](#architecture)
    - [Data Model](#data-model)
    - [User Stories for Chess Master MVP](#user-stories-for-chess-master-mvp)
11. [APIs](#apis)
12. [Mockups](#mockups)
13. [Usage Instructions](#usage-instructions)
14. [Contributing Guidelines](#contributing-guidelines)
15. [Related Projects](#related-projects)
16. [Licensing](#licensing)
17. [Installation Instructions](#installation-instructions)
18. [Screenshots/GIFs](#screenshotsgifs)

---

# Introduction
Welcome to Chess Master, a web application designed to bring the classic game of chess to life in the digital realm. Challenge your friends or test your skills against an AI opponent in this immersive gaming experience.

### Deployed Site:
[Chess Master Deployed Site](abdiwoli.tech)

### Final Project Blog Articles:
[Read Abdiwoli's Project Journey](https://www.linkedin.com/pulse/chess-master-where-passion-meets-code-unforgettable-abdiwoli-hassen-ycbof/)

[Read Muna's Project Journey](https://www.linkedin.com/pulse/chess-master-journey-strategy-innovation-muna-saeed-oeh4e/)

### Authors:
Connect with us on LinkedIn to stay updated on our latest projects and collaborations.
- [Abdiwoli Abdi](https://www.linkedin.com/in/abdiwoli)
- [Muna Said](https://www.linkedin.com/in/muna-saeedm)

---

## Run Instructions

To run the Chess Master project locally, follow these steps:

1. Make sure you have Python 3 installed on your system.

2. Run the following command to start the Flask application:
python3 -m game.app


### Team Members

1. **Abdiwoli Abdi**
   - **Role:** Lead Developer
   - **Why:** Abdiwoli has extensive experience in game development and will lead the technical aspects of the project.

2. **Muna Said**
   - **Role:** HTML, CSS, JavaScript
   - **Why:** Muna has a strong design background and will ensure an engaging and user-friendly game interface.

---

### Technologies

#### Languages:
- Python
- JavaScript

#### Framework:
- Flask

#### Database:
- MySQL and SQLite

#### Tools:
- Git
- GitHub

---

### Alternate Technology Choices

1. **Backend Framework:**
   - **Alternative:** Django
   - **Trade-offs:** Flask provides simplicity and flexibility, while Django offers a more extensive feature set. Chose Flask for its lightweight nature and better alignment with project needs.

2. **Database:**
   - **Alternative:** PostgreSQL
   - **Trade-offs:** MongoDB allows for flexible schema design, but PostgreSQL offers strong relational capabilities. Chose MongoDB for its scalability and ease of integration with a document-oriented game structure.

---

### Challenge Statement

#### Challenge:
- The project aims to create an engaging Chess game where users can play against each other or an AI opponent.
- The project will not solve broader chess-related challenges such as advanced chess strategies or deep chess theory.
- The project will help chess enthusiasts and casual players looking for an interactive and enjoyable chess-playing experience.
- The project is not dependent on a specific locale and is relevant to a global audience.

---

### Risks

#### Technical Risks:
- **Risk:** Integrating a complex AI algorithm may impact game performance.
- **Safeguard:** Implement iterative development, focusing on optimizing AI efficiency. Conduct extensive testing.

#### Non-Technical Risks:
- **Risk:** Lack of user engagement due to a poorly designed interface.
- **Strategy:** Prioritize User interface design, conduct user testing, and gather feedback for continuous improvement.

---

### Infrastructure

#### Branching and Merging:
- Follow GitHub Flow for branching and merging, creating feature branches for development and pull requests for code review.

#### Deployment Strategy:
- Utilize Fabric, a Python library, to streamline SSH-based tasks and deploy the game on remote servers. Execute deployment commands locally or remotely, with Fabric managing network connections. This approach offers flexibility for executing commands on servers maintained by the development team rather than relying on a cloud platform. The deployment will involve tasks such as uploading files, executing commands, and managing configurations using Fabric for efficient application deployment and systems administration.

#### Data Population:
- Use seed data for initial testing and development. Allow users to create accounts and save game progress.

#### Testing Tools:
- Implement unit testing using Jest for frontend and Pytest for backend. Conduct manual testing for user interaction scenarios.

---

### Existing Solutions

#### Similar Products:

1. **Chess.com:**
   - **Similarities:** Offers online chess gameplay against friends or AI.
   - **Differences:** Our project aims for a simpler and more user-friendly experience.

2. **Lichess:**
   - **Similarities:** Provides online chess gameplay.
   - **Differences:** Our project focuses on a more interactive and visually appealing interface.

#### Reimplementation Justification:
- Our project aims to provide a unique and user-centric chess gaming experience with a simplified interface, leading to a more engaging game compared to existing solutions.

# Chess Master MVP Specification

## Architecture

![Chess Master Architecture](architecture_diagram.PNG)

---

## Data Model

![Chess Master Data Model](data_model.PNG)

---

## User Stories for Chess Master MVP

### Sign Up to Play:
As a player, I want to sign up with a username and password so I can play chess online.
- **Criteria:** Easy registration with email verification.

### Play Against Computer:
As a player, I want to play against the computer at different difficulty levels for practice and fun.
- **Criteria:** Choose easy or hard difficulty with smart computer moves.

### Invite Friends to Play:
As a player, I want to invite my friends to play chess online and get notified when it's my turn.
- **Criteria:** Easy friend invitations and turn notifications.

---

## APIs

These API routes facilitate communication between the web client (frontend) and the web server (backend) of Chess Master.

1. `/api/users`
   - **Methods:**
     - GET: Retrieves user information based on a valid session ID (e.g., username or access token).
     - POST: Creates a new user account with username, password, and (optional) email address.
   - **Description:** This endpoint allows users to log in, retrieve their profile data, and potentially register for new accounts (depending on MVP scope).

2. `/api/games`
   - **Methods:**
     - GET: Retrieves a list of a user's past games (including filters for opponent, date range, etc.).
     - GET: /id: Retrieves information about a specific game by its ID (moves played, players involved, result).
     - POST: Starts a new game against the AI or invites a friend for a game (depending on MVP scope).
   - **Description:** This endpoint manages game data – fetching past games, accessing details of a specific game, and potentially initiating new games (vs AI or friend).

---

## Mockups

![Chess Master Data Model](Mockups.PNG)

---

## User Stories for Chess Master MVP

### Sign Up to Play:
As a player, I want to sign up with a username and password so I can play chess online.
- **Criteria:** Easy registration with email verification.

### Play Against Computer:
As a player, I want to play against the computer at different difficulty levels for practice and fun.
- **Criteria:** Choose easy or hard difficulty with smart computer moves.

### Invite Friends to Play:
As a player, I want to invite my friends to play chess online and get notified when it's my turn.
- **Criteria:** Easy friend invitations and turn notifications.

---

## APIs

These API routes facilitate communication between the web client (frontend) and the web server (backend) of Chess Master.

1. `/api/users`
   - **Methods:**
     - GET: Retrieves user information based on a valid session ID (e.g., username or access token).
     - POST: Creates a new user account with username, password, and (optional) email address.
   - **Description:** This endpoint allows users to log in, retrieve their profile data, and potentially register for new accounts (depending on MVP scope).

2. `/api/games`
   - **Methods:**
     - GET: Retrieves a list of a user's past games (including filters for opponent, date range, etc.).
     - GET: /id: Retrieves information about a specific game by its ID (moves played, players involved, result).
     - POST: Starts a new game against the AI or invites a friend for a game (depending on MVP scope).
   - **Description:** This endpoint manages game data – fetching past games, accessing details of a specific game, and potentially initiating new games (vs AI or friend).

---

## Mockups

![Chess Master Data Model](Mockups.PNG)

---

## Usage Instructions

### Starting a New Game
Once the application is running, users can:

1. Sign up or log in to their account.
2. Start a new game against the computer or invite friends to play. and make your first move.

### Making Moves
1. Click on the chess piece you want to move.
2. Click on the destination square to complete the move.
3. Repeat steps 1 and 2 for subsequent moves until the game is finished.

### Interacting with Features
- Use the navigation bar to access different sections of the application, such as user profile, game history, and settings.
- Customize game settings, such as board themes and piece styles, to personalize your gaming experience.

## Contributing Guidelines

### Bug Reports and Feature Requests
- If you encounter any bugs or have ideas for new features, please open an issue on GitHub with detailed information about the issue or request.

### Code Contributions
- Fork the repository and create a new branch for your contribution.
- Make your changes and submit a pull request, detailing the purpose of the changes and any relevant information for reviewers.

### Setting up the Development Environment
- Clone the repository to your local machine.
- Install dependencies using `pip install -r requirements.txt`.
- Set up the database by running migrations using `flask db upgrade`.
- Set environment variables for configuration, such as database connection details and secret keys.

## Related Projects

- [Stockfish Engine](https://stockfishchess.org/)
- [Chess.js](https://github.com/jhlywa/chess.js)

## Licensing

This project is licensed under the [MIT License](LICENSE).

## Installation Instructions

To run the Chess Master project locally, follow these steps:

1. Clone the Repository
	 ```
	git clone https://github.com/Muna-Saeed/Chess-Master-project.git
	 ```
2. Install Dependencies
	 ```
	pip install -r requirements.txt
	 ```
3. Setup Database
	 ```
	flask db upgrade
	 ```
4. Run the following command to start the Flask application
	 ```
	python3 -m game.app
	 ```
## Screenshots/GIFs
![chessboard](chessboard.JPG)

This README.md provides comprehensive information about the project, including team members, chosen technologies, challenge statement, risks, infrastructure details, and comparisons with existing solutions. It also outlines the MVP specification for Chess Master, including its architecture, data model, Mockups, user stories, API routes, usage instructions, contributing guidelines, related projects, licensing, installation instructions, and visual elements to showcase the user interface and gameplay. It provides a clear overview of the project's scope and functionality for both developers and stakeholders.It provides a clear overview of the project's scope and functionality for both developers and stakeholders. It serves as a guide for both team members and potential users or contributors.
