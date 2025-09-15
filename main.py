import os
import sys
from dotenv import load_dotenv
from google import genai
from tools import (
    get_files_info,
    create_file,
    read_file,
    delete_file,
    search_files,
    rename_file
    )

AVAILABLE_TOOLS = {
    'create_file': create_file,
    'delete_file': delete_file,
    'get_files_info': get_files_info,
    'read_file': read_file,
    'search_files': search_files,
    'rename_file': rename_file
}

def main():
    """
    Main program that runs the CLI agent
    """
    load_dotenv()
    api_key=os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    verbose_flag = False

    if len(sys.argv) > 1:

        if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
            verbose_flag = True

        prompt = sys.argv[1]

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )

        print(response.text)
    else:
        interactive_mode(client, verbose_flag)

    if response is None or response.usage_metadata is None:
        print("response is malformed")
        return
    
    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def interactive_mode(client: genai.Client, verbose=False):
    """
    Runs an interactive command-line loop that lets the user chat with
    the Gemini model and allows the model to request local tool execution.

    This function:
        1. Repeatedly reads user input from the terminal until the user
           types 'exit' or 'quit', or presses Ctrl-C / Ctrl-D.
        2. Maintains a conversation history (`context`) that is sent to
           the model each turn, so the model has full dialogue memory.
        3. Sends the user input and accumulated context to the Gemini API
           (`client.models.generate_content`).
        4. Examines the model's textual reply:
             - If the reply begins with the pattern
               "TOOL:<tool_name> <arg1> <arg2> …",
               it treats this as a request to invoke one of the
               registered Python functions listed in `AVAILABLE_TOOLS`.
             - The requested tool is looked up by name, executed with the
               provided arguments, and the result is printed back to the
               console. The result is also appended to the context so the
               model can "see" the tool's output on the next turn.
             - If the reply does not request a tool, the plain text
               answer from the model is printed and stored in the context.
        5. Optionally prints raw debug information if `verbose` is True.

    Parameters
    ----------
    client : genai.Client
        An authenticated Google GenAI client used to send prompts and
        receive model responses.
    verbose : bool, optional
        If True, prints the raw response object from the Gemini API
        for debugging purposes. Defaults to False.

    Notes
    -----
    - Conversation history is kept in a list of dicts with keys
      "role" ('user', 'model', or 'tool') and "parts" (message text).
    - Tool invocation relies on a simple convention where the model
      explicitly prefixes its response with "TOOL:" followed by the
      tool name and its arguments separated by spaces.
    - Any exception during tool execution or API call is caught and
      displayed; the loop then continues.
    """
    print("Interactive Gemini CLI. Type 'exit/quit' to leave")

    context = [] # history message where model has memory to keep the dialogue with user

    while True:
        try:
            # prompt user for a single line of input
            user_input = input(">> ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Bye!")
                break
            
            # append user message to the running conversation
            context.append({"role": "user", "parts": user_input})
            
            # send conversation to model
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=context
            )

            # extract and clean the text reply from the model
            text = response.text.strip()

            # Check if the model wants to call a registered tool
            if text.upper().startswith("TOOL:"):
                # divide text with max 3 tokens according to white spaces
                # [0] -> TOOL:create_file
                # [1] -> myfile.txt
                # [2] -> Hello world
                parts = text.split(maxsplit=2)
                if len(parts) < 3:
                    print("[WARN] Not valid tool syntax")
                    continue

                # divide stringa after first ':' and get element [1] - tool_name
                # only works because 'TOOL:' is defined with ':' instead would be IndexError
                tool_name = parts[0].split(":", 1)[1]
                args = parts[1:]
                tool_fn = AVAILABLE_TOOLS.get(tool_name)
                if not tool_fn:
                    print(f"[WARN] Unknown tool: {tool_name}")
                    continue

                try:
                    # ask user to delete the provided context because it might be destructive
                    if tool_fn == "delete_file":
                        confirm = input(f"Are you sure you want to delete {args[0]}? (y/n): ").strip().lower()
                        if confirm != "y":
                            print("Deletion cancelled.")
                            continue

                    result = tool_fn(*args)
                    print(f"[TOOL RESULT] {result}")
                    context.append({"role": "tool", "parts": str(text)})
                except Exception as e:
                    print(f"[ERROR] Calling the {tool_name} failed: {e}")
                    context.append({"role": "tool", "parts": f"error: {e}"})
            else:
                # Simply display the model's message
                print(text)
                context.append({"role": "model", "parts": text})

                if verbose:
                    print("--- DEBUG  ---")
                    print(response)

        except (KeyboardInterrupt, EOFError):
                # Handle CTRL-C / CTRL-D
                print("\nBye")
                break
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    main()