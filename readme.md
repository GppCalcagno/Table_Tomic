# ⚽ Table-Tomic
Welcome to our Foosball Tracker project! Designed for a friendly competition, this project celebrates our office foosball table and the vibrant culture it inspires.

<div align="center">
  <img src="media\icon.jpg" alt="App Icon" width="200"/>
</div>

We’re dedicated to keeping track of our game records and sharing the fun moments that bring our team together. Inspired by [Playtomic](https://playerhelp.playtomic.com/hc/en-gb), we’ve developed a ranking algorithm to mimic their system and monitor our matches effectively. 
Tournaments are on the horizon, so get ready to play, compete, and have a blast!

The project allows you to:
- 📝 Register users and assign them a rank from 0 to 10.
- 🎮 Record matches and update each player's rank based on the results.
- 🏆 View rankings of the top-performing players.


## 📱 Media Gallery
Here are some screenshots of TableTomic in action:

<div align="center" style="display: flex; justify-content: space-around; flex-wrap: wrap;">
  <img src="media\homepage.jpeg" alt="Match 1" width="200"/>
  <img src="media\result.jpeg" alt="Match 2" width="200"/>
</div>

<br><br>

<div align="center" style="display: flex; justify-content: space-around; flex-wrap: wrap;">
  <img src="media\registration.jpeg" alt="Match 3" width="200"/>
  <img src="media\ranking.jpeg" alt="Match 4" width="200"/>
</div>

<br><br>

# 📐 Technical Structure
The project's infrastructure includes:
- 🗄️ Database: PostgreSQL is used to store users and match data.
- 🖥️ Back-End: Built with Python Django. To keep things simple, the front-end relies on Django's HTML templates (I'm not a front-end developer. If a form is showed, [LGTM](https://knowyourmeme.com/memes/lgtm)!).
- 📦 Docker: The entire project is containerized using a Docker Compose structure for maximum portability.

## 🏆Ranking Algorithm Explanation

#### Table Football Rating Adjustment System
This document explains the methodology behind a rating update system for table football matches. The system adjusts individual player ratings (scaled from 0 to 10) based on match outcomes and individual performance relative to the team average.

---

### 1. Team Average Calculation
For each team, compute the **team average rating** using the ratings of the goalkeeper and attacker:

$$TeamAvg = \frac{\text{Rating}_{\text{goalkeeper}} + \text{Rating}_{\text{attacker}}}{2}$$

---

### 2. Expected Outcome Calculation
Using the team average ratings, calculate the **expected win probability** for each team with a logistic function (similar to the Elo rating system).

For Team A:

$$E_A = \frac{1}{1 + 10^{\frac{R_B - R_A}{d}}} $$

Where:
- $R_A$ and $R_B$ are the average ratings for Team A and Team B.
- $d$ is a scaling factor adjusting the sensitivity to rating differences.

For Team B, the expected outcome is:

$$ E_B = 1 - E_A $$

---

### 3. Actual Match Outcome and Goal Margin
#### Actual Outcome
Determine the actual match outcome ($S$) from the scores:
- **Win:** $S = 1$
- **Loss:** $S = 0$
- **Tie:** $S = 0.5$ for both teams

#### Goal Difference
Calculate the **goal difference**:

  $$ \text{Goal Difference} = |\text{score}_A - \text{score}_B| $$

#### Margin Multiplier
Compute the **margin multiplier ($M$)** using the logarithm of the goal difference plus one:

$$M = \ln(\text{Goal Difference} + 1)$$

This logarithmic function dampens the impact of large goal differences. For a tie ($\text{Goal Difference} = 0$), set $M = 1$ to avoid a zero multiplier.

---

### 4. Team-Level Rating Change
Calculate a **base rating change** for the entire team:

$$\Delta R_{\text{team}} = K \times M \times (S - E)$$

Where:
- $K$ is a constant that controls the maximum rating change.
- $M$ is the margin multiplier.
- $S$ is the actual match outcome.
- $E$ is the expected win probability.

---

### 5. Individual Rating Adjustment
To reflect differences among team members, adjust the team delta for each player based on the difference between their individual rating and the team average.

#### 5.1. Adjustment Factor
Calculate an **adjustment factor** for each player:

$$\text{Adjustment Factor} = 1 + \beta \times (\text{TeamAvg} - \text{PlayerRating})$$

- **$\beta$** is a tuning parameter controlling the sensitivity of the adjustment.
- If a player's rating is **below** the team average ($\text{TeamAvg} - \text{PlayerRating} > 0$), the factor is **greater than 1**. On a winning team, this player gains more points.
- Conversely, if a player's rating is **above** the team average, the factor is less than 1 (or more negative on a losing team), causing a larger point loss.

#### 5.2. Role Weight and Rating Update
Each player's new rating is updated as follows:

$$\text{NewRating} = \text{OldRating} + \Delta R_{\text{team}} \times \text{Adjustment Factor} \times w_{\text{role}}$$

Where:

- $w_{\text{role}}$ is a weight factor specific to the player's role (e.g., goalkeeper or attacker).

#### 5.3. Clipping the Rating
Ensure the updated rating stays within the 0 to 10 range:

$$\text{NewRating} = \max(0, \min(10, \text{NewRating}))$$

---

This methodology ensures that within the same team, players with different initial ratings will have their adjustments tailored to better reflect their relative performance compared to the team’s overall strength.


<br><br>

# 🏷️ Contribution 
Of course, there’s still plenty of room for improvement in this project, such as:

- Refining the ranking system to ensure greater accuracy and fairness.
- Enhancing the UI and developing a proper front-end for a smoother user experience.
- Improving the registration process to make it more intuitive and user-friendly.

Feel free to fork, contribute, or use this project however you like—every contribution is highly appreciated! The ultimate goal is to make lunch breaks more enjoyable for office workers everywhere.


 This whole project came together in under 50 hours (or 100 🍅), thanks to [Toggl Track](https://toggl.com/track/pomodoro-timer-toggl/). 
 
 Not bad for a bunch of tomatoes! 🍅😄 
 
## 🏛️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```markdown
MIT License

Copyright (c)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS
