# AutoTA-discord-bot

## Inspiration
Due to the COVID-19 pandemic, most educational institutions around the world have switched to online learning alternatives. We've read on the news about how difficult it is for young students to adjust to virtual learning because of how important social interaction and visual learning is for children. This is where our inspiration came from, to tackle the challenge of the online learning transition.

We wanted to focus on elementary and middle school children, in order to create a more interactive experience and simulate in-person schooling activities, such as: taking daily attendance, leaving the classroom to go into the hallway, earning recognition points for having good behaviour, and going to the teacher's desk to ask a question privately. Additionally, we wanted to make it more user-friendly for educators to have an easier time adjusting to online teaching as well. Using simple commands, educators can easily create text-channels for assignments, quizzes, and discussions, and take attendance daily.

 We chose a Discord Bot because Discord is available on all devices, making online learning more accessible to students and educators, regardless of socioeconomic status or circumstance.

## What it does
AuToTA is a Discord Bot available for all educators to implement in their virtual learning Discord server. The functionality includes:
- Easy commands to easily organize students in different spaces within the server (classroom, hallway, teacher's desk,...)
- Easy commands to easily create channel spaces for discussion and instruction (assignments, quizzes, discussion boards,...)
- Daily attendance and roll call (including data record to track progress)
- Points System to encourage good behaviour from students (including data record to track progress)
- Question board for students' questions to be highlighted and avoid from being lost in the chatroom
- Private channel for teacher to track progress and monitor student activity throughout the lesson

## Features:

- **Attendance:** 

  - Students record their attendance with emoji reactions to automated posts. 

  - Administrators can access students' attendance history.

    | Command   |                                                              | Permitted users |
    | --------- | ------------------------------------------------------------ | --------------- |
    | $attendance      | Creates a message for students to react to. | Administrator only        |
    | $here | Records user as present. | Everyone        |


  

- **Rewards:**

  - Administrators can reward students with points that can be redeemed for prizes of the administrators' choice.

    | Command           |                                                              | Permitted users    |
    | ----------------- | ------------------------------------------------------------ | ------------------ |
    | $setupclass       | Called with an integer. Creates blank points data for all server members with the role "Students". | Administrator only |
    | $resetrewardvalue | Called with an integer. Resets the point value of the prize. | Administrator only |
    | $getrewardvalue   | Sends message saying the point value of the prize.           | Everyone           |
    | $add              | Called with a mention of a user and an optional reason. Gives mentioned user 1 point. | Administrator only |
    | $remove           | Called with a mention of a user and an optional reason. Removes 1 point from mentioned user. | Administrator only |
    | $mypoints         | Sends a message with user's current number of points.        | Everyone           |
    | $pointsof         | Called with a mention of a user. Sends a message to a private text channel with the number of points the mentioned user currently has. | Administrator only |
    | $redeem           | Called with a mention of a user. Removes the value of a prize from mentioned user. | Administrator only |



- **"Hall pass" system:**

  - Avoid classroom distractions and unanswered questions from teachers.

  - Students can alert AuToTA when they are away from their device and when they return.

  - Administrators are notified privately when a student leaves and returns.

    | Command |                                                              | Permitted users |
    | ------- | ------------------------------------------------------------ | --------------- |
    | $away   | Moves user into 'hallway' voice channel and notifies administrators. | Everyone        |
    | $back   | Moves user into 'classroom' stage channel and notifies administrators. | Everyone        |

    

- **Question channel organization:**

  - AuToTA keeps class discussions productive and engaging by sorting out important questions from students.

    | Command   |                                                              | Permitted users |
    | --------- | ------------------------------------------------------------ | --------------- |
    | $new      | Called with category name and name of channel. Creates a channel in a category. | Everyone        |
    | $question | Called with a question. Repeats the question in a text channel. | Everyone        |

    





## How we built it
- Python for the Discord Bot programming
- JSON for the student data (points system, daily attendance,...)
- UptimeRobot to monitor the bot 24/7
- Replit for collaborative coding

## Challenges we ran into
Discord.py library experienced many updates in the past few years, making much of the documentation and resources online outdated. Implement the new version was a challenge, but we overcame it through problem solving. Also, given the constraints of time and number of members, we were unable to complete the backend data storage on a cloud database. In order to overcome this, AuToTA only is available for our Discord server at the moment.

## Accomplishments that we're proud of
We're so proud that we were able to make the bot work and complete most of the intended tasks, in such a small amount of time permitted. It was a big learning curve but we were able to overcome the challenges quickly. 

## What we learned
During this weekend, we attended the Discord Bot workshop and got inspired by the tutorials. We learned more about Discord Bot programming and the work that goes into making them function effectively. We also learned more about monitoring them on UptimeRobot so that they're monitored 24/7. Also, we used Replit for the first time, which was a super cool way to collaborate with coding teams.

## What's next for AuToTA
We hope to create a web-based platform  that is linked to the data collected by the Discord Bot. This way, educators can easily access combined data from the semester to evaluate progress.
