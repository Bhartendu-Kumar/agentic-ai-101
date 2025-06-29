from pathlib import Path
from src.mode_manager import ModeManager
from src.llm_service import LLMService

def run():
    """
    Main function to run the terminal-based coding assistant.
    """
    config_path = Path(__file__).parent.parent / "config" / "modes.json"
    mode_manager = ModeManager(config_path)
    llm_service = LLMService()

    print("Welcome to the Basic Coding Assistant!")

    while True:
        print("\nAvailable Modes:")
        modes = mode_manager.get_modes()
        for i, mode_name in enumerate(modes, 1):
            print(f"{i}. {mode_name}")

        try:
            choice = int(input("Select a mode (enter the number): "))
            if 1 <= choice <= len(modes):
                selected_mode_name = modes[choice - 1]
                mode_slug = mode_manager.get_mode_slug(selected_mode_name)
                system_prompt = mode_manager.get_system_prompt(mode_slug)

                user_prompt = input(f"\n[{selected_mode_name} Mode] You: ")
                if user_prompt.lower() in ['exit', 'quit']:
                    print("Exiting the assistant. Goodbye!")
                    break

                llm_response = llm_service.get_response(system_prompt, user_prompt)
                print(f"\nAssistant: {llm_response}")

            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
