**Overview**

- **Project**: Agentic_AI — collection of small examples demonstrating LangChain runnables, tools, and agent patterns.
- **Environment**: Uses a `.env` file for API keys. Required keys: `OPENWEATHER_API_KEY`, `TAVILY_API_KEY`.

**File Notes**

- **Agents.py**: Implements an interactive "city assistant" agent with two tools: [get_weather](Agents.py) and [get_news](Agents.py). Uses `TavilyClient` for news and `ChatMistralAI` as the LLM. Includes a human-approval middleware that prompts before each tool call. Known issue: requires the `langchain-mistralai` package (import may raise ModuleNotFoundError if not installed).
- **main.py**: Minimal entrypoint printing a greeting. Useful as a quick smoke-run: `python main.py`.
- **newssummarizer.py**: Runs a Tavily search (`TavilySearchResults`) then passes results through a `ChatMistralAI` prompt to produce a summarized bullet list.
- **owntool.py**: Example of defining a LangChain `@tool` (`get_greeting`) and invoking it locally. Prints tool metadata (`name`, `description`, `args`).
- **parallelrunnable.py**: Demonstrates `RunnableParallel` to run short and long explanations in parallel using `RunnableLambda`, `ChatPromptTemplate`, and `ChatMistralAI`.
- **runnablepassthrough.py**: Shows `RunnablePassthrough` combined with a code-generation prompt and an explanation prompt; composes runnables and prints both code and explanation outputs.
- **sequencerunnable.py**: Simple `prompt | model | parser` sequence using `ChatMistralAI` and `StrOutputParser`.
- **toolcalling.py**: Interactive example where an LLM binds to a tool (`get_text_length`) and the script handles tool-calls and final responses.
- **streamlit_app.py**: Streamlit web UI for fetching weather or news by city using the same API workflows and `.env` keys.

**How to run**

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Add a `.env` file with the required API keys:

```
OPENWEATHER_API_KEY=your_openweather_key
TAVILY_API_KEY=your_tavily_key
```

4. Run an example, for instance the agent:

```powershell
python {filename}.py
```

5. Run the Streamlit interface:

```powershell
streamlit run streamlit_app.py
```
