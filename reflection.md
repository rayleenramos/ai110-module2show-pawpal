# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. My initial UML design consists of four classes: Owner, Pet, Task, and Plan.
- What classes did you include, and what responsibilities did you assign to each?
Owner is responsible for representing the pet owner. It holds the owner's name, available time for the day, and a list of their pets. It can add or update pets and update available time.
Pet holds basic information about the pet: name, breed, and species, it and can return a readable summary of itself.
Task represents a single care activity such as a walk, feeding, or grooming session. It stores the task type, priority, duration and whether it recurs daily. It can update its own priority and duration.
Plan is the core of the system. It belongs to an Owner and a Pet, holds the full task list, and is responsible for scheduling, sorting tasks by priority, filtering out tasks that exceed available time, generating the final schedule, and displaying it.

**b. Design changes**

- Did your design change during implementation? Yes, the design changed during implementation.
- If yes, describe at least one change and why you made it. Originally, Plan stored a copy of the owner's available time when it was created, but that copy would go stale if the owner updated it later. The fix was to read self.owner.available_time directly so it always stays current.
Also, Task priority started as a plain string with no rules, which meant typos could break sorting silently. Switching to an Enum made the allowed values explicit and sorting reliable.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
