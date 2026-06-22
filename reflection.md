# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
I see a game with instructions to enter a number from 1 to 100, a kind of guessing game. There's a field where I can enter this number, some options to click on like difficulty selection and such. I can also decide whether I want hints or not, and to start a new game.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1. When I enter a number and press enter (like the field hint says), nothing happens.
2. I typed in 100, it says go lower. I typed in a very large number like 100000, it says go higher. It doesn't make sense.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Clicking on "New Game" |Should reset the game |Doesn't clear entries from debug console |None |
|Enter 1000000 | "Go lower" | Says "Go higher" |None |
|Changed difficulty, range changes |Guess instructions should reflect this |Does not, still says "1 and 100" |None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
One suggestion was for a bug I reported that some hints didn't seem to correctly compare the guess with the secret. It correctly found the code block which was the issue and I verified by entering a couple text cases for those scenarios.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Yes, I asked the AI "when I select a different difficulty under the "Difficulty" field on the UI, the "Range" value changes but the instructions still read to enter a number from 1 to 100. is this the intended functionality". This correctly told me where these values are hardcoded, but the programmer might not realize that the actual range values will have to be updated elsewhere too. For instance, because the 'Secret' value will have to be within this range.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
