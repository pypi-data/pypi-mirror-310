# 🧠🧱 IntelliBricks: The Building Blocks for Intelligent Applications

Welcome to **IntelliBricks**—your streamlined toolkit for developing AI-powered applications. Whether you're interacting with large language models (LLMs), training machine learning models, or implementing Retrieval Augmented Generation (RAG), IntelliBricks simplifies the complex so you can focus on what truly matters: your application logic.

> ⚠️ **Warning:**  
> *This project is currently under development and is **not ready for production**.*  
> If you resonate with our vision, please consider supporting the project to help bring it to life! This is a personal endeavor I've nurtured for months and am excited to open source it. I work during the day and attend university classes at night. That’s why the support of the community is essential—I can’t do this alone. I’m excited to share this journey with you! The plan is to launch in 2025.

---

## 🚀 Key Features

- **✨ Simplified LLM Interaction:**  
  Interact seamlessly with multiple AI providers through a unified interface. Switch models effortlessly using simple enum changes. Supports both single prompt completions and chat-based interactions.

- **🤖 Effortless Model Training:**  
  Train machine learning models with minimal code using the intuitive `SupervisedLearningEngine`. Includes data preprocessing, model selection, evaluation, and artifact management.

- **🔍 Retrieval Augmented Generation (RAG):**  
  Connect to your knowledge bases for context-aware AI responses *(currently under development)*.

- **📦 Built-in Parsing:**  
  Eliminate boilerplate parsing code with automatic response deserialization into your defined data structures.

- **📊 Langfuse Integration:**  
  Gain deep insights into your LLM usage with seamless integration with Langfuse. Monitor traces, events, and model costs effortlessly. IntelliBricks automatically calculates and logs model costs for you.

- **💸 Transparent Cost Tracking:**  
  Automatically calculates and tracks LLM usage costs, providing valuable insights into your spending.

- **🔗 Fully Typed:**  
  Enjoy a smooth development experience with complete type hints for `mypy`, `pyright`, and `pylance`, ensuring type safety throughout your codebase.

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [LLM Interaction](#llm-interaction)
   - [Chat Interactions](#chat-interactions)
2. [Advanced Usage](#advanced-usage)
   - [System Prompts and Chat History](#system-prompts-and-chat-history)
   - [Customizing Prompts](#customizing-prompts)
   - [Langfuse Integration](#langfuse-integration)
3. [Parameter Breakdown](#-parameter-breakdown)
4. [Key Points to Consider](#-key-points-to-consider)
5. [Training Machine Learning Models](#training-machine-learning-models)
6. [Coming Soon](#coming-soon)
7. [Documentation](#documentation)
8. [Contributing](#contributing)
9. [License](#license)
10. [Community & Support](#community--support)
11. [Showcase](#showcase)

---

## 🏁 Getting Started

### 📦 Installation

Install IntelliBricks via pip:

```bash
pip install intellibricks
```

### 🧠 LLM Interaction

IntelliBricks abstracts the complexities of interacting with different LLM providers. Specify your prompt, desired response format, and model, and IntelliBricks handles the rest.

#### 🔄 Synchronous Completion Example

```python
from msgspec import Struct
from intellibricks import CompletionEngine

class Joke(Struct):
    joke: str

# One line to rule them all 🔥
output = CompletionEngine().complete(prompt="Tell me a joke", response_format=Joke)

print(output.get_parsed())  # Joke obj
```

**Highlights:**
- **3 Easy Steps:** Define your structured output, call `complete()`, and parse the result.
- **No Boilerplate:** Forget about `OutputParsers` and repetitive code.
- **Environment Keys:** Make sure to have the correct model provider API_KEY in your enviroment and to use load_dotenv() to load them.


## How to do it with LangChain 🦜️🔗

LangChain offers a simplified approach to structured outputs using `with_structured_output`.  While convenient, it lacks some of the advanced features and flexibility of IntelliBricks. For instance, features like fallback models, caching, tracing, and custom tool integration are not readily available.  Additionally, the reliance on a single `invoke` method for diverse operations can make customization and specific parameter handling less intuitive.

```python
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Joke(BaseModel):
    joke: str

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_llm = model.with_structured_output(Joke)

joke = structured_llm.invoke(
    "Tell me a joke about cats"
) # Joke object

print(joke)
```

## How to do it with LlamaIndex 🦙

LlamaIndex also provides a way to achieve structured outputs, involving wrapping the LLM with  `as_structured_llm`.  This, however, introduces additional steps compared to IntelliBricks.  You also need to construct `ChatMessage`.  LlamaIndex's approach lacks the built-in retry mechanisms, comprehensive tracing with Langfuse, and other advanced parameters offered by IntelliBricks for fine-grained control and observability.

```python
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from pydantic import BaseModel

class Joke(BaseModel):
    joke: str


llm = OpenAI(model="gpt-3.5-turbo-0125")
sllm = llm.as_structured_llm(output_cls=Joke)

input_msg = ChatMessage.from_str("Tell me a joke about cats")

output = sllm.chat([input_msg])
output_obj = output.raw # Joke object

print(output_obj)
```


IntelliBricks streamlines the process by directly accepting the prompt and the desired output structure (`response_format`).  It handles the complexities of parsing and error handling internally. Furthermore, IntelliBricks provides a richer set of parameters like `fallback_models`, `max_retries`, `cache_config`, and `trace_params` for enhanced control, resilience, and monitoring, which are absent in the LangChain and LlamaIndex examples above.



#### 🔍 Type Safety with Mypy and Pyright

IntelliBricks is built with type hints, ensuring a smooth development experience.

```python
from dotenv import load_dotenv
from msgspec import Struct
from intellibricks import CompletionEngine

load_dotenv(override=True)

class Joke(Struct):
    joke: str

output = CompletionEngine().complete(
    prompt="Tell me a joke",
    response_format=Joke
)  # CompletionOutput[Joke]

choices = output.choices  # list[MessageChoice[Joke]]
message = output.choices[0].message  # CompletionMessage[Joke]
parsed = message.parsed  # Joke

# Easily get the parsed output
easy_parsed = output.get_parsed()  # Defaults to choice 0
```

## 🎯 My Goal: A Quick Breakdown

The primary goal of **IntelliBricks** is to make developers' lives easier by simplifying the process of building intelligent applications. I strive to provide an intuitive, feature-rich toolkit that abstracts complexity, enabling users to focus on their application's unique logic.

A cornerstone of this vision is ensuring **perfect type hints** for tools like `mypy` and modern IDEs. By prioritizing robust and accurate type annotations, IntelliBricks aims to offer a seamless and productive development experience, reducing errors and enhancing code clarity across the entire stack.

I also **AVOID** using `**kwargs`, unlike many frameworks that rely on it extensively. While `**kwargs` can offer flexibility, I believe it harms clarity and significantly detracts from the developer experience. Here's why:

1. **Lack of Explicitness:**  
   `**kwargs` obscures the actual parameters a function or method accepts, forcing developers to constantly refer to documentation or source code to understand the expected arguments.

2. **Reduced IDE Support:**  
   IDEs and type checkers struggle to provide accurate autocompletion and type hints for `**kwargs`. This lack of support can lead to errors and slow down development.

3. **Error-Prone Code:**  
   Misspelled or unexpected arguments can slip through unnoticed because `**kwargs` doesn’t validate the provided keys, leading to potential runtime errors.

4. **Harder to Maintain:**  
   Over time, as code evolves, the use of `**kwargs` can make it challenging to track which arguments are required or optional, increasing the cognitive load on developers maintaining the code.

5. **Less Readable Code:**  
   Code that relies heavily on `**kwargs` sacrifices readability, making it harder for teams to collaborate and for new developers to onboard effectively.

Instead of `**kwargs`, I prefer defining explicit parameters with detailed type hints. This approach ensures clarity, enhances IDE support, and improves the overall developer experience, aligning with IntelliBricks' mission to make development intuitive and enjoyable.

### 💬 Chat Interactions

Engage in multi-turn conversations with structured responses.

```python
from intellibricks import Message, MessageRole, CompletionOutput
from dotenv import load_dotenv
from msgspec import Meta, Struct

load_dotenv(override=True)

# Define structured response models
class President(Struct):
    name: str
    age: Annotated[int, Meta(ge=40, le=107)]

class PresidentsResponse(Struct):
    presidents: list[President]

messages = [
    Message(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
    Message(role=MessageRole.USER, content="Hello, how are you?"),
    Message(role=MessageRole.ASSISTANT, content="I'm fine! And you? IntelliBricks is awesome, isn't it? (This was completely generated by AI and not the owner of the project)"),
    Message(role=MessageRole.USER, content="I'm fine. What are the presidents of the USA?"),
]

response = engine.chat(
    messages=messages,
    response_format=PresidentsResponse
)

presidents_response: PresidentsResponse = response.get_parsed()
print(presidents_response)
```

---

## 🌐 Integrating IntelliBricks with Litestar

Create a simple API endpoint using the [Litestar](https://litestar.dev/) framework that receives a request and returns a structured response with IntelliBricks.

```python
from litestar import Litestar, post
from intellibricks import CompletionEngine, AIModel
from msgspec import Struct

# Define the request model
class JokeTheme(Struct):
    prompt: str

# Define the structured response model
class JokeResponse(Struct):
    joke: str

# Define the endpoint
@post("/joke", response_model=JokeResponse)
async def get_joke(data: JokeTheme) -> JokeResponse:
    response = CompletionEngine().complete(
        prompt=f"The theme of the joke is: {data.prompt}",
        system_prompt="You are an AI specialised in making the funniest jokes.",
        response_format=JokeResponse
        model=AIModel.STUDIO_GEMINI_1P5_FLASH
    )
    return response.get_parsed()

app = Litestar([get_joke])
```

---

## 🌐 Integrating IntelliBricks with FastAPI

Create a simple API endpoint using the [FastAPI](https://fastapi.tiangolo.com/) framework that receives a request and returns a structured response with IntelliBricks. Since FastAPI relies on Pydantic for data validation and IntelliBricks uses `msgspec.Struct`, we'll use Pydantic for the request model and encode the IntelliBricks response using `msgspec.json.encode()` before returning it.

```python
from fastapi import FastAPI, Response
from pydantic import BaseModel
from intellibricks import CompletionEngine, AIModel
from msgspec import Struct
import msgspec

# Define the request model using Pydantic
class JokeRequest(BaseModel):
    prompt: str

# Define the structured response model using msgspec
class JokeResponse(Struct):
    joke: str

# Initialize FastAPI and CompletionEngine
app = FastAPI()

# Define the endpoint
@app.post("/joke")
async def get_joke(data: JokeRequest) -> Response:
    response = CompletionEngine().complete(
        prompt=f"The theme of the joke is: {data.prompt}",
        system_prompt="You are an AI specialized in making the funniest jokes.",
        response_format=JokeResponse,
        model=AIModel.STUDIO_GEMINI_1P5_FLASH
    )
    joke_response = response.get_parsed()
    encoded_response = msgspec.json.encode(joke_response)
    return Response(content=encoded_response, media_type="application/json")
```

### 🛠️ Additional Notes

- **Why Use `msgspec.json.encode()`?**
  
  FastAPI is designed to work seamlessly with Pydantic models for both requests and responses. However, since IntelliBricks uses `msgspec.Struct` for structured responses, directly returning `msgspec` objects isn't compatible with FastAPI's response handling. By encoding the `msgspec` structured response into JSON bytes, we can integrate IntelliBricks' structured outputs with FastAPI's response system effectively. Intellibricks will not use pydantic's BaseModel, since msgspec is way faster to serialize/desserialize in performance critical / low latency LLM applications.

---

## 🛠️ Advanced Usage

### 🔄 CompletionOutput Overview

All methods provided by the `CompletionEngine` in **IntelliBricks** return an instance of `CompletionOutput`. Understanding the structure and components of `CompletionOutput` is essential for effectively handling and utilizing the responses from the AI models. This section provides a comprehensive overview of `CompletionOutput` and its associated subclasses.

### 📦 What is `CompletionOutput`?

`CompletionOutput` is a structured response object that encapsulates all relevant information returned by the AI model after processing a request. It provides not only the generated content but also metadata and usage statistics, enabling developers to manage and optimize their interactions with AI models efficiently.

### 🔑 Key Components of `CompletionOutput`

- **`id`**  
  A unique identifier for the completion request. This UUID can be used for tracking and referencing specific completions.

- **`object`**  
  Denotes the type of the returned object. For completions, this is always `"chat.completion"`.

- **`created`**  
  A Unix timestamp indicating when the completion was generated. This helps in tracking the timing of responses.

- **`model`**  
  Specifies the AI model used to generate the completion, allowing developers to identify which model processed the request.

- **`system_fingerprint`**  
  Represents the backend configuration fingerprint of the AI model. This is useful for understanding any backend changes that might affect response determinism.

- **`choices`**  
  A list of `MessageChoice` instances, each representing a possible response generated by the AI model. This is particularly useful when multiple completions are requested (`n > 1`).

- **`usage`**  
  Provides detailed statistics about the token usage and associated costs for both the prompt and the completion. This information is invaluable for monitoring and optimizing API usage and expenses.

### 🧩 Subclasses and Their Roles

#### 1. `MessageChoice`

Each `MessageChoice` in the `choices` list corresponds to a distinct response generated by the AI model. Key attributes include:

- **`index`**  
  The position of this choice in the list of all choices. Useful for referencing specific completions.

- **`message`**  
  An instance of `CompletionMessage` containing the actual content of the response along with any parsed structured data.

- **`logprobs`**  
  (Currently always `None`) Reserved for future use to provide log probabilities of the generated tokens.

- **`finish_reason`**  
  Indicates why the model stopped generating tokens. Common reasons include reaching the maximum token limit (`"length"`), encountering a stop sequence (`"stop"`), content filtering (`"content_filter"`), or invoking a tool (`"tool_calls"`).

#### 2. `CompletionMessage`

`CompletionMessage` extends the base `Message` class and includes an additional attribute:

- **`parsed`**  
  Contains the deserialized structured data as defined by the `response_format` parameter provided in the `CompletionEngine` method. This allows for type-safe access to the response data.

#### 3. `Usage`

The `Usage` class provides a detailed breakdown of token consumption and associated costs:

- **`prompt_tokens`**  
  Number of tokens used in the input prompt.

- **`completion_tokens`**  
  Number of tokens generated in the completion.

- **`total_tokens`**  
  Sum of `prompt_tokens` and `completion_tokens`.

- **`input_cost`**  
  Cost incurred for the input prompt in USD.

- **`output_cost`**  
  Cost incurred for the output completion in USD.

- **`total_cost`**  
  Total cost for the completion request in USD.

- **`prompt_tokens_details` & `completion_tokens_details`**  
  Further breakdown of token usage, including categories like `audio_tokens` and `reasoning_tokens` for more granular insights.

### 🛠️ Working with `CompletionOutput`

Here's how you can interact with `CompletionOutput` to access the generated responses and associated metadata:

```python
from intellibricks import CompletionEngine, AIModel
from msgspec import Struct

# Define your structured response model
class Joke(Struct):
    joke: str

# Initialize the CompletionEngine
engine = CompletionEngine()

# Make a completion request
response: CompletionOutput[Joke] = engine.complete(
    prompt="Tell me a joke",
    response_format=Joke,
    model=AIModel.GPT_4O
)

# Access the first choice
joke_message = response.get_message(choice=0)
print(joke_message.content)  # Outputs the raw joke string

# Access the parsed structured response
parsed_joke: Joke = response.get_parsed(choice=0)
print(parsed_joke.joke)  # Outputs the joke from the structured model

# Access usage statistics
print(response.usage.total_tokens)  # Total tokens used
print(response.usage.total_cost)    # Total cost in USD
```

### 🥸 But I don't want structured outputs!

Fine. CompletionEngine will adapt and types will work fine as well.

```python
from intellibricks import CompletionEngine

# Make a completion request
response = engine.complete(
    prompt="Tell me a joke",
) # CompletionOUtput[None]

# Access the first choice
joke_message = response.get_message(choice=0)
print(joke_message.content)  # Outputs the raw joke string

# Access the parsed structured response
parsed_joke = response.get_parsed(choice=0) # None

# Access usage statistics
print(response.usage.total_tokens)  # Total tokens used
print(response.usage.total_cost)    # Total cost in USD
```

### 📈 Benefits of Using `CompletionOutput`

- **Structured Data Handling:**  
  By utilizing `CompletionOutput` and its subclasses, developers can work with structured and type-safe data, reducing errors and improving code clarity.

- **Comprehensive Metadata:**  
  Access to detailed metadata such as token usage and costs enables better monitoring and optimization of AI interactions.

- **Multiple Choices Support:**  
  Ability to handle multiple completions (`n > 1`) allows for more flexible and diverse responses from the AI models.


### 📜 Complete `CompletionEngine.chat()` Usage Example

Gain a comprehensive understanding of how to leverage each parameter to customize your AI-powered chat interactions effectively.

#### **1. Load Environment Variables**

```python
load_dotenv(override=True)
```

#### **2. Define Structured Response Models**

```python
class President(Struct):
    name: str
    age: int

class PresidentsResponse(Struct):
    presidents: list[President]
```

#### **3. Initialize Langfuse (Optional)**

```python
langfuse_client = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
)
```

#### **4. Configure Vertex AI Credentials (Optional)**

```python
vertex_credentials = service_account.Credentials.from_service_account_file(
    "path/to/your/vertex_credentials.json"
)
```

#### **5. Initialize the CompletionEngine**

```python
engine = CompletionEngine(
    langfuse=langfuse_client,  # Optional: Integrate with Langfuse
    json_encoder=None,          # Optional: Use a custom JSON encoder
    json_decoder=None,          # Optional: Use a custom JSON decoder
    vertex_credentials=vertex_credentials,  # Optional: Vertex AI credentials
    web_searcher=SearxngWebSearchEngine(host="...") # IN DEVELOPMENT
)
```

#### **6. Set Up Cache Configuration (Optional) // Currently only works with VertexAI**

```python
from datetime import timedelta

cache_config = CacheConfig(
    enabled=True,  # Enable caching
    ttl=timedelta(minutes=10),  # Set TTL to 10 minutes
    cache_key='unique_key_for_runtime_app_mapping'  # Define a unique cache key
)

# **Example:**
# >>> cache_config = CacheConfig(enabled=True, ttl=timedelta(seconds=60), cache_key='user_prompt')
```

#### **7. Define Trace Parameters to show in Langfuse(Optional)**

```python
trace_params = TraceParams(
    name="ChatCompletionTrace",
    user_id="user_12345",
    session_id="session_67890",
    metadata={"feature": "chat_completion"},
    tags=["chat", "completion"],
    public=False
)

# **Example:**
# >>> trace_params = TraceParams(user_id="user_123", session_id="session_456")
# >>> print(trace_params)
# {'user_id': 'user_123', 'session_id': 'session_456'}
```

#### **8. Prepare Chat Messages**

```python
messages = [
    Message(role=MessageRole.SYSTEM, content="You are a knowledgeable assistant."),
    Message(role=MessageRole.USER, content="Hello! Can you help me with some information?"),
    Message(role=MessageRole.ASSISTANT, content="Of course! What do you need assistance with?"),
    Message(role=MessageRole.USER, content="I'm interested in knowing the current presidents of various countries.")
]
```

#### **9. Make a `chat` Request with All Parameters**

```python
try:
    chat_response = engine.chat(
        messages=messages,  # The conversation history
        response_format=PresidentsResponse,  # Structured response format
        model=AIModel.GPT_4O,  # Primary AI model
        fallback_models=[AIModel.STUDIO_GEMINI_1P5_FLASH, AIModel.GPT_3_5_TURBO],  # Fallback models
        n=2,  # Number of responses to generate
        temperature=0.7,  # Creativity of the responses
        max_tokens=500,  # Maximum tokens per response
        max_retries=3,  # Maximum number of retry attempts
        cache_config=cache_config,  # Cache configuration
        trace_params=trace_params,  # Tracing parameters for monitoring
        postergate_token_counting=False,  # Immediate token counting
        tools=[your_custom_tool_function],  # Custom tool functions *(Currently under development, interfaces are beeing designed.)*
        data_stores=[rag_data_store],  # RAG data stores for context-aware responses *(Currently under development interfaces are beeing designed.)*
        web_search=True,  # Enable web search capabilities *(Currently under development)*. Requires passing a `WebSearchable` instance in `CompletionEngine` constructor. interfaces are beeing designed.`.
    )

    # Access the parsed structured response
    presidents_response: PresidentsResponse = chat_response.get_parsed()
    for president in presidents_response.presidents:
        print(f"President: {president.name}, Age: {president.age}")

except MaxRetriesReachedException:
    print("Failed to generate a chat response after maximum retries.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

#### **10. Asynchronous `chat_async` Request (Optional)**

```python
async def async_chat_example():
    try:
        chat_response = await engine.chat_async(
            messages=messages,  # The conversation history
            response_format=PresidentsResponse,  # Structured response format
            model=AIModel.GPT_4O,  # Primary AI model
            fallback_models=[AIModel.STUDIO_GEMINI_1P5_FLASH, AIModel.GPT_3_5_TURBO],  # Fallback models
            n=2,  # Number of responses to generate
            temperature=0.7,  # Creativity of the responses
            max_tokens=500,  # Maximum tokens per response
            max_retries=3,  # Maximum number of retry attempts
            cache_config=cache_config,  # Cache configuration
            trace_params=trace_params,  # Tracing parameters for monitoring
            postergate_token_counting=False,  # Immediate token counting
            tools=[your_custom_tool_function],  # Custom tool functions *(Currently under development)*
            data_stores=[rag_data_store],  # RAG data stores for context-aware responses *(Currently under development)*
            web_search=True  # Enable web search capabilities *(Currently under development)*. Requires passing a `WebSearchConfig`.
        )

        # Access the parsed structured response
        presidents_response: PresidentsResponse = chat_response.get_parsed()
        for president in presidents_response.presidents:
            print(f"President: {president.name}, Age: {president.age}")

    except MaxRetriesReachedException:
        print("Failed to generate a chat response after maximum retries.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the asynchronous chat example
asyncio.run(async_chat_example())
```

#### **11. Custom Prompt Compilation**

Create dynamic prompts with placeholders for flexibility.

```python
from intellibricks import Prompt

# Define a prompt template with placeholders
prompt_template = Prompt(content="My name is {{name}}. I am {{age}} years old.")

# Compile the prompt with actual values
compiled_prompt = prompt_template.compile(name="Alice", age=30)

print(compiled_prompt)  # Output: My name is Alice. I am 30 years old.
```

#### **12. Handling Exceptions and Retries**

Gracefully manage failures and retries.

```python
try:
    output = engine.chat(
        messages=messages,
        response_format=None,  # No structured response
        model=AIModel.GPT_4O,
        max_retries=5,
        # ... other parameters
    )
    print(output.get_message().content)

except MaxRetriesReachedException:
    print("Unable to generate a response after multiple attempts. Please try again later.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

#### **13. Integrating with Retrieval Augmented Generation (RAG)**

Enhance responses with context from your knowledge bases.

```python
# Initialize your RAG data store
rag_data_store = YourRAGDataStore()

# Make a completion request with RAG integration
try:
    output = engine.chat(
        messages=messages,
        response_format=None,
        data_stores=[rag_data_store],  # Integrate RAG data stores *(Currently under development)*
        web_search=True,  # Enable web search capabilities *(Currently under development)*. Requires passing a `WebSearchConfig`.
        # ... other parameters
    )
    print(output.get_message().content)

except MaxRetriesReachedException:
    print("Failed to retrieve information after multiple attempts.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

---

### 🔍 Parameter Breakdown

Here's a detailed explanation of each parameter used in the `CompletionEngine.chat()` method:

| Parameter | Type | Description |
|---|---|---|
| `messages` | `list[Message]` | **Required.** A list of `Message` objects representing the conversation history.  Each message has a `role` (e.g., `SYSTEM`, `USER`, `ASSISTANT`) and `content`. |
| `response_format` | `Type[T]` or `None` | **Optional.** A structured data model (subclass of `msgspec.Struct`) to deserialize the AI's response. If `None`, the response remains unstructured (`str`). |
| `model` | `AIModel` or `None` | **Optional.** The primary AI model. Defaults to `AIModel.STUDIO_GEMINI_1P5_FLASH`. |
| `fallback_models` | `list[AIModel]` or `None` | **Optional.** Alternative AI models to try if the primary model fails. |
| `n` | `int` or `None` | **Optional.** The number of completions to generate. Defaults to `1`. |
| `temperature` | `float` or `None` | **Optional.** Controls response creativity (0.0-1.0).  Higher values are more random. |
| `max_tokens` | `int` or `None` | **Optional.** Maximum tokens per response. Defaults to `5000`. |
| `max_retries` | `Literal[1, 2, 3, 4, 5]` or `None` | **Optional.** Maximum retry attempts. Defaults to `1`. |
| `cache_config` | `CacheConfig` or `None` | **Optional.** Caching configuration. See [CacheConfig Examples](docs/examples/cache_config_examples.md). |
| `trace_params` | `TraceParams` or `None` | **Optional.** Tracing parameters. See [TraceParams Examples](docs/examples/trace_params_examples.md). |
| `postergate_token_counting` | `bool` | **Optional.** Defer token counting. Defaults to `True`. |
| `tools` | `list[Callable[..., Any]]` or `None` | **Optional.** Custom tool functions. *(Currently under development.)* |
| `data_stores` | `Sequence[RAGQueriable]` or `None` | **Optional.** RAG data stores. *(Currently under development.)* |
| `web_search` | `bool` or `None` | **Optional.** Enable web search. Requires `WebSearchable` to be passed in the `CompletionEngine` constructor. *(Currently under development.)* Defaults to `False`. |
---

## 💡 Key Points to Consider

- **📐 Structured Responses:**  
  Utilize the `response_format` parameter with `msgspec.Struct` models to ensure AI responses adhere to predefined structures, facilitating easier downstream processing and validation.

- **🔄 Fallback Models:**  
  Enhance the resilience of your application by specifying `fallback_models`, providing alternative AI models in case the primary model encounters issues or fails to generate a response.

- **⚡ Asynchronous Operations:**  
  Leverage `chat_async` to handle multiple concurrent AI interactions efficiently, improving overall performance and responsiveness.

- **💾 Caching:**  
  Properly configure `cache_config` to optimize performance and reduce costs by avoiding redundant AI calls for identical prompts.

- **📈 Tracing and Monitoring:**  
  Integrate with Langfuse and utilize `trace_params` to gain deep insights into your AI interactions, enabling effective monitoring, debugging, and cost tracking.

- **🛡️ Error Handling:**  
  Implement robust error handling to gracefully manage failures, especially when dealing with external AI services. The `MaxRetriesReachedException` helps identify when maximum retry attempts have been exhausted.

- **🔒 Security:**  
  Always handle sensitive information, such as API keys and credentials, securely. Use environment variables or secure secret management systems to protect your data.

---

## 🏋️ Training Machine Learning Models

Train supervised learning models effortlessly with the `SupervisedLearningEngine`. Provide your data and configuration, and let IntelliBricks manage the training and prediction pipeline.

```python
from intellibricks.models.supervised import SKLearnSupervisedLearningEngine, TrainingConfig, AlgorithmType
import base64

# Encode your dataset
with open("dataset.csv", "rb") as f:
    b64_file = base64.b64encode(f.read()).decode("utf-8")

# Define training configuration
config = TrainingConfig(
    algorithm=AlgorithmType.RANDOM_FOREST,
    hyperparameters={"n_estimators": 100, "max_depth": 5},
    target_column="target_variable",
    # ... other configurations
)

# Instantiate the training engine
engine = SKLearnSupervisedLearningEngine()

# Train the model
training_result = await engine.train(
    b64_file=b64_file,
    uid="my_model_123",
    name="My Model",
    config=config,
)

print(training_result)


# Make Predictions
input_data = {
    'feature1': 10,
    'feature2': 'A',
    'feature3': 5.5,
    # ... other features
}

predictions = await engine.predict(
    uid='my_model_123',
    input_data=input_data,
)

print(predictions)
```

---

## 🛠️ Advanced Usage

### 📜 System Prompts and Chat History

```python
from intellibricks import Message, MessageRole

messages = [
    Message(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
    Message(role=MessageRole.USER, content="Who won the world series in 2020?"),
    Message(role=MessageRole.ASSISTANT, content="The Los Angeles Dodgers."),
    Message(role=MessageRole.USER, content="Where was it played?"),
]

response = engine.chat(messages=messages)
message: Message = response.get_message()
print(message)
# >> Message(role=MessageRole.ASSISTANT, content="I don't know")
```

### 🛠️ Customizing Prompts

```python
from intellibricks import Prompt

prompt_template = Prompt(content="My name is {{name}}. I am {{age}} years old.")  # Implements __str__
compiled_prompt = prompt_template.compile(name="John", age=30)  # Returns Prompt
print(compiled_prompt)  # Output: My name is John. I am 30 years old.
```

### 📊 Langfuse Integration

IntelliBricks integrates with Langfuse for enhanced observability of your LLM interactions. Trace performance, track costs, and monitor events with ease. This integration is automatically activated when you instantiate a `CompletionEngine` with a Langfuse instance.

```python
import os
from langfuse import Langfuse

langfuse_client = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
)

engine = CompletionEngine(langfuse=langfuse_client)

# Now all LLM calls made with 'engine' will be automatically tracked in Langfuse, including costs.
```

---

## 🌟 Coming Soon

- **🔗 Enhanced RAG:**  
  A more robust RAG implementation for seamless integration with diverse knowledge sources. We aim to create adapters for each vector store, ensuring compatibility across interfaces.

- **📄 Unified Document Parsing:**  
  Stop wasting time choosing the right library for parsing PDFs. IntelliBricks will handle it for you with our `DocumentArtifact` model, easily convertible to `llama_index` and `langchain` documents. Support for NER and Relations extraction is on the horizon.  
  **Example:**

  ```python
  extractor: FileExtractorProtocol = ...  # In development

  # Example #1 - From file in filesystem:
  document_artifact_1 = extractor.extract(
      RawFile.from_file("./documents/some_file.pdf"),
      parsing_method=ParsingMethod.FAST,
      gpu=False,
  )

  # Example #2 - From an uplodaded files:
  # Imagine you're ingesting documents into a vector store, but you don't have them yet. Extract from uploaded files will be possible
  document_artifact_2 = extractor.extract(
      RawFile.from_litestar_uploadfile(some_litestar_upload_file),
      parsing_method=ParsingMethod.MEDIUM,
      gpu=True,
  )
  document_artifact_3 = extractor.extract(
      RawFile.from_fastapi_uploadfile(some_fastapi_upload_file),
      parsing_method=ParsingMethod.PROFESSIONAL,
      gpu=False,
  )


  langchain_documents = document_artifact_1.as_langchain_docs(
      transformations=[SemanticChunker(...)]
  )
  # Done. Now you can ingest your doc into
  some_vector_store.add_documents(langchain_documents)  # Langchain example
  ```

---

## 📖 Documentation

For now, the only documentation available is here in GitHub. I work as a Software Architect | Engineer, so I'm trying to manage my time for this project too.
---

## 🤝 Contributing

We welcome contributions to IntelliBricks! Whether it's reporting issues, suggesting features, or submitting pull requests, your involvement is invaluable.

---

## 📝 License

[MIT License](LICENSE)

---

## 👥 Community & Support

Join our community to stay updated, share your projects, and get support:

- **GitHub Discussions:** [IntelliBricks Discussions](https://github.com/arthurbrenno/intellibricks/discussions)
---

Thank you for choosing **IntelliBricks**!
