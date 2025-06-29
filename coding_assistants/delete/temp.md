<thinking>
Initiating Mode Planning

I'm currently working on a plan for a fundamental terminal-based coding assistant. The initial focus is on the crucial "mode" selection feature. I'm thinking through how to structure this to offer a flexible and user-friendly experience right from the start. Based on the selected mode, a system prompt will be applied. This seems straightforward, but I want to make sure it's robust and expandable.

Outlining the Core Features

I've sketched out the initial feature set. It will involve a mode selection, system prompts based on the mode, terminal interaction, user input processing, and LLM response handling. Next, I'm digging into the codebase to see how things are currently structured and figure out the best place to add these new features. I'm going to start by listing the existing files to get a lay of the land.
</thinking>

I need to develop a plan for a basic, terminal-based coding assistant.

Here are the core requirements:

Mode Selection: Users must be able to choose a "mode" for each interaction.
System Prompt: The selected mode will determine the system prompt for the Large Language Model (LLM).
Terminal Interface: The assistant will operate as a continuous loop within the terminal.
User Input: The assistant will accept a string input from the user.
LLM Response: It will provide an LLM-generated response based on the user's input.
I will begin by examining the existing codebase to understand its structure and determine the most effective way to implement these features. My first step is to list the files in the current directory.

<list_files>
<path>coding_assistants/</path>
</list_files>






-----

<switch_mode>
<mode_slug>code</mode_slug>
<reason>The user has approved the plan and wants to start implementation. I will now switch to code mode to create the necessary files and write the application code.</reason>
</switch_mode>