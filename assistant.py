import subprocess
import requests

# ─────────────────────────────────────────
# PART 1: Run a command and detect errors
# ─────────────────────────────────────────

def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result


# ─────────────────────────────────────────
# PART 2: Send error to local AI
# ─────────────────────────────────────────

def explain_error(error_text, command):
    print("\n🤔 Analyzing error with AI...")

    prompt = f"""You are a helpful Linux terminal assistant.
The user ran this command:

    {command}

It failed with this error:

    {error_text}

Please explain in simple beginner-friendly terms:
1. What went wrong
2. Why it happened  
3. The exact fix with command to run

Be concise and clear. Use simple English."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        result = response.json()
        return result["response"]

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Fix: sudo systemctl start ollama"

    except Exception as e:
        return f"Could not get explanation: {str(e)}"


# ─────────────────────────────────────────
# PART 3: Main assistant loop
# ─────────────────────────────────────────

def main():
    print("=" * 50)
    print("   LOCAL AI TERMINAL ASSISTANT")
    print("   Powered by gemma:2b + Ollama")
    print("   Type 'exit' to quit")
    print("=" * 50)

    while True:

        # Get command from user
        try:
            command = input("\n⚡ Enter command: ").strip()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        # Handle exit
        if command.lower() in ["exit", "quit", "bye"]:
            print("\nGoodbye! Happy coding!")
            break

        # Skip empty input
        if not command:
            continue

        # Run the command
        print(f"\n>>> Running: {command}")
        result = run_command(command)

        # Show output if any
        if result.stdout:
            print(f"\n Output:\n{result.stdout}")

        # Check for errors
        if result.returncode != 0:
            print("\n❌ Error detected!")
            print(f"\n{result.stderr}")

            # Ask AI to explain
            explanation = explain_error(result.stderr, command)

            print("\n" + "=" * 50)
            print("💡 AI EXPLANATION:")
            print("=" * 50)
            print(explanation)
            print("=" * 50)

        else:
            print("✅ Command completed successfully!")


# ─────────────────────────────────────────
# PART 4: Start the assistant
# ─────────────────────────────────────────

if __name__ == "__main__":
    main()
