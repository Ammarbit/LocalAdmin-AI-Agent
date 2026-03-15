import ollama
import os


def list_files_on_desktop():
    """Returns a list of all files on the user's Desktop."""
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return str(files)

def create_file(filename, content):
    """Creates a new file with the specific content."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Success: Created file '{filename}'."
    except Exception as e:
        return f"Error: {e}"

def read_file(filename):
    """Reads the content of a file."""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not found."


print("🖥️  Desktop Agent is Online! (Llama 3.2)")
print("I can read, write, and list files on your Desktop.")

history = []

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    history.append({'role': 'user', 'content': user_input})

    response = ollama.chat(
        model='llama3.2',
        messages=history,
        tools=[list_files_on_desktop, create_file, read_file]
    )

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            function_name = tool.function.name
            args = tool.function.arguments
            
            tool_output = ""
            
            if function_name == 'list_files_on_desktop':
                print(f"⚙️  Agent is scanning Desktop...")
                tool_output = list_files_on_desktop()
                
            elif function_name == 'create_file':
                print(f"⚙️  Agent is writing to '{args['filename']}'...")
                tool_output = create_file(args['filename'], args['content'])
                
            elif function_name == 'read_file':
                print(f"⚙️  Agent is reading '{args['filename']}'...")
                tool_output = read_file(args['filename'])

            history.append(response.message) 
            history.append({
                'role': 'tool', 
                'content': str(tool_output),
            })
            
            final_response = ollama.chat(model='llama3.2', messages=history)
            print(f"Agent: {final_response.message.content}")
            
            history.append(final_response.message)

    else:
        print(f"Agent: {response.message.content}")
        history.append(response.message)
