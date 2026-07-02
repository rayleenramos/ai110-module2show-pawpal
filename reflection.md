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

- What constraints does your scheduler consider (for example: time, priority, preferences)? The scheduler considers three constraints: the owner's total available time, task priority (HIGH, MEDIUM, LOW), and whether a task is recurring.

- How did you decide which constraints mattered most? Priority mattered most because a pet owner should always handle urgent tasks like medication before optional ones like grooming, regardless of how much time is left.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes. The scheduler uses a greedy approach, it picks tasks in priority order and stops when time runs out, which means a long HIGH priority task could use all the available time and knock out several shorter MEDIUM tasks.

- Why is that tradeoff reasonable for this scenario? This is reasonable because for pet care, doing the most important things completely is better than partially fitting in everything.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)? I used AI for design brainstorming (identifying missing relationships and bottlenecks in my UML), implementing new features like conflict detection and recurring task logic, and refactoring display_schedule to produce cleaner terminal output.
- What kinds of prompts or questions were most helpful? The most helpful prompts were specific ones that included the actual code and asked for a concrete improvement, like "suggest logic improvements for sorting and filtering" followed by "now implement the sorting and filtering features."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is. When AI suggested storing available_time as a copy in Plan, I didn't accept it because I realized it would go stale if the owner updated their time later.
- How did you evaluate or verify what the AI suggested?I verified the suggestion by tracing through what would happen if update_available_time() was called after the plan was created, and confirmed the copy would be out of sync.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? I tested task completion status changes, pet task count after adding tasks, chronological time slot sorting, recurring task cloning after completion, and conflict detection for overlapping tasks.
- Why were these tests important? These tests were important because they cover the core behaviors the scheduler depends on, if any of these break, the whole schedule output would be wrong.

**b. Confidence**

- How confident are you that your scheduler works correctly? I'm confident the scheduler handles the scenarios I built and tested, since all 5 tests pass and the terminal output matches expected behavior.
- What edge cases would you test next if you had more time? Next I would test what happens when available time is 0, when two pets have tasks at the exact same start time, and when a recurring task has no recurrence interval set.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with? I'm most satisfied with the conflict detection and recurring task logic because they added real functionality beyond basic scheduling and required me to think carefully about how the classes interact.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign? I would redesign display_schedule to be separate from the scheduler logic so formatting and scheduling aren't mixed in the same class, making it easier to swap out the display without touching the core logic.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project? Working with AI taught me that generated code needs to be traced through manually, it can look correct but break under real usage, so treating it like any other code that needs testing is the right approach.

