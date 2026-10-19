# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Add a pet and enter its details
Manage tasks by adding, editing, or removing them
Generate and view daily schedule by automatically building an automized daily plan

Owner: Manages information such as contact details and collecion of pets. Responsible for adding pets as well as care preferences
Pet: Represents a pets attributes such as name and age. Provides methods to add or remove task
CareTask: the attributes of care task
Scheduler: filters by time constraints and priority


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
We took into account the time and how certain times could match
- How did you decide which constraints mattered most?
I decided based on what I felt was a more realistic conflict pet owners face

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It only looks for exact time matches, rather than checking if tasks overlap in duration
- Why is that tradeoff reasonable for this scenario?
Checking for exact time matches is fast and easy to read
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
Used it to help figure out errors and to brainstorm pieces of code
- What kinds of prompts or questions were most helpful?
I found a lot of error prompts helpful as I would paste an error I don't understand and ask for a fix or explanantion and usually get one that makes sense to me.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
There was one time when the AI made a code in explain_plan that confused me a bit, I initially took it before realizing it had a few errors and decided to fix it up and change it a bit
- How did you evaluate or verify what the AI suggested?
I usually tested it or looked it over to see if it made sense.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
some behaviors I tested were conflict detection, completion, and task addition
- Why were these tests important?
Its important as these things need to work to ensure the code is running to completion and that time conflicts are being detected

**b. Confidence**

- How confident are you that your scheduler works correctly?
Very confident
- What edge cases would you test next if you had more time?
I guess if task can be properly removed 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I think my initial work on pawpal_system.py went well

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would maybe redesign some of the app to make it more clean.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned how to better apply and rely on AI for error handeling especially if I don't understand the error.
