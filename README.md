# ECE-49595-Project Spring 2024
Ty Runner, Jungwoo Kwon, Michael Ross
## Football film analysis tool



Install dependancies using: "pip install -r requirements.txt"

Introduction:
* In the strategic landscape of football, the detailed analysis of game film is a fundamental aspect of preparation, yet it is historically burdened by its labor-intensive nature. Coaches and players often immerse themselves in extensive film study, attempting to identify and understand key trends and tactics from hours of footage. Our project introduces a groundbreaking solution aimed at streamlining this process. By employing advanced technology, our program efficiently sifts through vast amounts of film, pinpointing crucial trends and specific instances, such as a notable play in a particular game. This process not only accelerates the initial phase of film analysis but also eliminates the more laborious aspects of the task. The reduction of this initial workload brings a two-fold advantage. Firstly, it allows coaches and players to allocate more time to delve into the finer details of the game, focusing on in-depth strategic analysis and personalized coaching techniques. Secondly, by removing the more tedious elements of film study, our tool enhances the overall focus and engagement of the team with the material. Coaches can concentrate their efforts on developing sophisticated game plans and nuanced understanding of their opponents, while players can better absorb and apply the insights gained from a more targeted analysis. Ultimately, our aim is to revolutionize the approach to football film study, making it a more efficient, focused, and ultimately more effective tool in the arsenal of football teams striving for excellence.

Goals: 

* Develop a program that significantly reduces the time coaches spend on analyzing football game film. 

* Automate the identification and categorization of key plays and strategies from game footage. 

* Implement intuitive, graphical visualization of game data for easier analysis and strategy development. 

* Design a user-friendly interface suitable for coaches at all technology skill levels. 

* Ensure scalability of the tool for different levels of football, from high school to college leagues. 

Use Cases:

* Use Case 1: Film Package Upload
  * Description: Coaches initiate the process by uploading a package of game film into the local BallHawk application. This is done through a simple, minimalistic interface that facilitates the selection and submission of video files from local storage.
  * Functionality: The application acknowledges the upload and stores the film package locally, preparing it for analysis.

* Use Case 2: Player Team Identification
  * Description: Once the film is uploaded, BallHawk processes the footage to identify which players belong to which team, based on the colors of their jerseys. 
  * Functionality: The application utilizes OpenCV's color detection capabilities to distinguish between the two teams, establishing a foundational understanding of the players' distribution on the field.

* Use Case 3: Trend Extraction
  * Description: After identifying the teams, BallHawk analyzes the plays in the film package to extract key trends and patterns, such as common offensive or defensive strategies used by each team. 
  * Functionality: The software automatically reviews the footage, identifying and cataloging significant plays, formations, and tactics employed by both teams.

* Use Case 4: Trend Reporting and Play Referencing
  * Description: Following the analysis, BallHawk compiles a report of the identified trends and specific examples of these trends (e.g., game 2, play 4) for further review.
  * Functionality: The application generates a summary of findings with references to specific game footage, allowing coaches and players alike to easily access and review crucial plays. 

* Use Case 5: Community-Driven Feedback and Enhancement
  * Description: Recognizing the open-source nature of BallHawk, the coaching and developer communities actively contribute to its development. Coaches, analysts, and developers can provide feedback, suggest features, and contribute code to enhance the software's capabilities. 
  * Functionality: The application is designed to evolve through community contributions. Feedback from users, coupled with developments from the open-source community, informs continuous improvement and feature updates, ensuring the software remains adaptable and up-to-date with the latest in football analysis techniques. 
