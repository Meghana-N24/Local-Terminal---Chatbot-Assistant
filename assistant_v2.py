import subprocess
import requests
import memory


# PART 1: Start memory system
# Always do this first


memory.init_db()



# PART 2: Run a terminal command
# Captures output and errors


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result


# PART 3: Build a smart prompt
# Uses memory context to make AI smarter


def build_smart_prompt(command, error_text, similar_errors, count):

    # Start building the prompt
    prompt = f"""You are a helpful Linux terminal assistant with memory.
The user ran this command:

    {command}

It failed with this error:

    {error_text}

"""

    # Add memory context if we have it
    if count > 0:
        prompt += f"""MEMORY CONTEXT:
This exact error has occurred {count} time(s) before.

"""

    if similar_errors:
        prompt += "Previous similar errors and fixes:\n"
        for i, (prev_cmd, prev_err, prev_fix, prev_time) in enumerate(similar_errors):
            prompt += f"""
  Past occurrence {i+1}:
  Command: {prev_cmd}
  Error: {prev_err}
  Fix that worked: {prev_fix}
  When: {prev_time}
"""

    # Final instruction
    prompt += """
Based on the error and any past context above, please explain:
1. What went wrong
2. Why it happened
3. The exact fix with command to run

If this is a repeated error, mention that and refer to
what worked before. Be concise and beginner friendly."""

    return prompt



# PART 4: Ask AI with full context

def ask_ai(prompt):
    print("\n🤔 Analyzing with memory context...")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )
        result = response.json()
        return result["response"]

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Fix: sudo systemctl start ollama"

    except Exception as e:
        if "timed out" in str(e):
            return "AI took too long to respond. Try running: ollama run gemma:2b 'hello' in another terminal to wake it up, then try again."
        return f"Could not get explanation: {str(e)}"
        



# PART 5: Handle a detected error
# This is where memory makes us smarter


def handle_error(command, error_text):

    # Step 1: Check memory for similar past errors
    similar_errors = memory.find_similar_errors(error_text)
    count = memory.count_error_occurrences(error_text)

    # Step 2: Show memory status to user
    if count > 0:
        print(f"\n🧠 Memory: I've seen this error {count} time(s) before!")
        if similar_errors:
            last_fix = similar_errors[0][2]
            if last_fix:
                print(f"💾 Last fix was: {last_fix}")
    else:
        print("\n🆕 First time seeing this error.")

    # Step 3: Build smart prompt with context
    prompt = build_smart_prompt(
        command,
        error_text,
        similar_errors,
        count
    )

    # Step 4: Get AI explanation
    explanation = ask_ai(prompt)

    # Step 5: Save this error + fix to memory
    memory.save_error(command, error_text, explanation)

    # Step 6: Return explanation to show user
    return explanation



# PART 6: Run command and handle result


def run_and_explain(command):

    # Run the command
    print(f"\n>>> Running: {command}")
    result = run_command(command)

    # Show normal output if any
    if result.stdout:
        print(f"\n Output:\n{result.stdout}")

    # Check for errors
    if result.returncode != 0:
        print(f"\n❌ Error detected!")
        print(f"\n{result.stderr}")

        # Handle with memory + AI
        explanation = handle_error(command, result.stderr)

        # Show AI explanation
        print("\n" + "=" * 50)
        print("💡 AI EXPLANATION (with memory context):")
        print("=" * 50)
        print(explanation)
        print("=" * 50)

        # Save to command history (had error = 1)
        memory.save_command(command, 1)

    else:
        print("✅ Command completed successfully!")
        # Save to command history (no error = 0)
        memory.save_command(command, 0)



# PART 7: Show session memory summary

def show_memory_summary():
    print("\n" + "=" * 50)
    print("🧠 MEMORY SUMMARY (Last 5 commands):")
    print("=" * 50)

    history = memory.get_recent_history(5)

    if not history:
        print("No history yet.")
    else:
        for cmd, had_error, timestamp in history:
            status = "❌ Error" if had_error else "✅ Success"
            print(f"{timestamp} | {status} | {cmd}")

    print("=" * 50)


# PART 8: Main interactive loop


def main():
    print("=" * 50)
    print("   LOCAL AI TERMINAL ASSISTANT V2")
    print("   Now with Memory & Context Awareness")
    print("   Powered by gemma:2b + SQLite + Ollama")
    print("   Commands: 'exit' | 'memory' | any command")
    print("=" * 50)

    while True:

        # Get command from user
        try:
            command = input("\n⚡ Enter command: ").strip()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        # Handle special commands
        if command.lower() in ["exit", "quit", "bye"]:
            show_memory_summary()
            print("\nGoodbye! Your session has been saved.")
            break

        if command.lower() == "memory":
            show_memory_summary()
            continue

        # Skip empty input
        if not command:
            continue

        # Run command with memory-aware error handling
        run_and_explain(command)



# Start the assistant


if __name__ == "__main__":
    main()
