# ECE-49595-Project Spring 2024
Ty Runner, Jungwoo Kwon, Michael Ross
## Football film analysis tool

Goals: 

* Develop a program that significantly reduces the time coaches spend on analyzing football game film. 

* Automate the identification and categorization of key plays and strategies from game footage. 

* Implement intuitive, graphical visualization of game data for easier analysis and strategy development. 

* Design a user-friendly interface suitable for coaches at all technology skill levels. 

* Ensure scalability of the tool for different levels of football, from high school to college leagues. 

Use Cases:

* Use Case 1: Film Package Upload
* * Description: Coaches initiate the process by uploading a package of game film into the local BallHawk application. This is done through a simple, minimalistic interface that facilitates the selection and submission of video files from local storage.
* * Functionality: The application acknowledges the upload and stores the film package locally, preparing it for analysis.

* Use Case 2: Player Team Identification
* * Description: Once the film is uploaded, BallHawk processes the footage to identify which players belong to which team, based on the colors of their jerseys. 
* * Functionality: The application utilizes OpenCV's color detection capabilities to distinguish between the two teams, establishing a foundational understanding of the players' distribution on the field.

* Use Case 3: Trend Extraction
* * Description: After identifying the teams, BallHawk analyzes the plays in the film package to extract key trends and patterns, such as common offensive or defensive strategies used by each team. 
* * Functionality: The software automatically reviews the footage, identifying and cataloging significant plays, formations, and tactics employed by both teams.

* Use Case 4: Trend Reporting and Play Referencing
* * Description: Following the analysis, BallHawk compiles a report of the identified trends and specific examples of these trends (e.g., game 2, play 4) for further review.
* * Functionality: The application generates a summary of findings with references to specific game footage, allowing coaches and players alike to easily access and review crucial plays. 

* Use Case 5: Community-Driven Feedback and Enhancement
* * Description: Recognizing the open-source nature of BallHawk, the coaching and developer communities actively contribute to its development. Coaches, analysts, and developers can provide feedback, suggest features, and contribute code to enhance the software's capabilities. 
* * Functionality: The application is designed to evolve through community contributions. Feedback from users, coupled with developments from the open-source community, informs continuous improvement and feature updates, ensuring the software remains adaptable and up-to-date with the latest in football analysis techniques. 