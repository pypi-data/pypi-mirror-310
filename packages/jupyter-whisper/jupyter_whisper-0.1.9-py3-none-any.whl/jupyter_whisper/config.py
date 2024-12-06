import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable, Union, Generator  # Added Union and Generator
import threading
from openai import OpenAI

class ConfigManager:
    DEFAULT_CONFIG = {
        'api_keys': {},
        'preferences': {
            'SKIP_SETUP_POPUP': False,
            'MODEL_PROVIDER': 'grok',  # Set default to a custom provider
            'MODEL': 'grok-beta-vision', 
            'ACTIVE_QUICK_EDIT_PROFILE': 'default',
            'QUICK_EDIT_PROFILES': {
                'default': {
                    'name': 'Default Editor',
                    'provider': 'grok',
                    'model': 'grok-beta',
                    'system_prompt': """
You are a precise text and code editor. Your task is to:

1. Process provided text/code snippets
2. Make necessary improvements and corrections
3. Instructions are in !!double exclamation!!

Rules:
- Return ONLY the edited text/code
- Remove all double exclamation annotations in the final output
- Keep HTML comments if needed to explain rationale
- Maintain the original format and structure
- Focus on clarity, correctness and best practices
"""
                },
                'code_review': {
                    'name': 'Code Reviewer',
                    'provider': 'grok',
                    'model': 'grok-beta',
                    'system_prompt': """
You are a thorough code reviewer. Your task is to:

1. Review code for best practices and potential issues
2. Suggest improvements and optimizations
3. Focus on maintainability and performance

Rules:
- Return the improved code with clear comments explaining changes
- Maintain the original structure unless changes are necessary
- Focus on practical, production-ready improvements
"""
                },
                'documentation': {
                    'name': 'Documentation Helper',
                    'provider': 'grok',
                    'model': 'grok-beta',
                    'system_prompt': """
You are a documentation specialist. Your task is to:

1. Improve documentation and comments
2. Add clear explanations and examples
3. Ensure consistency in documentation style

Rules:
- Focus on clarity and completeness
- Add docstrings and comments where needed
- Follow documentation best practices
"""
                }
            },
            "CUSTOM_PROVIDERS": {
                "grok": {
                    "name": "grok",
                    "models": [
                        "grok-vision-beta"
                    ],
                    "initialization_code": """
import os
from typing import Optional, List, Generator, Union
from openai import OpenAI
from jupyter_whisper.config import get_config_manager


class Chat:
    def __init__(self, model: Optional[str] = None, sp: str = '', history: Optional[List[dict]] = None):
        self.model = model or "grok-vision-beta"
        self.sp = sp
        self.api_key = self.get_api_key()
        self.client = self.get_client()
        self.h = history if history is not None else []

    def get_api_key(self):
        config = get_config_manager()
        api_key = config.get_api_key('GROK_API_KEY')
        if not api_key:
            raise ValueError("GROK_API_KEY not found in configuration")
        return api_key

    def get_client(self):
        return OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )

    def update_model(self, model_info: dict):
        self.model = model_info.get('model', self.model)

    def update_api_key(self, api_keys: dict):
        self.api_key = self.get_api_key()
        self.client = self.get_client()

    def __call__(self, 
                 message: str, 
                 max_tokens: int = 4096, 
                 stream: bool = True,
                 temperature: float = 0,
                 images: Optional[List[dict]] = None) -> Union[str, Generator[str, None, str]]:
        try:
            # Handle message content based on whether images are present
            if images:
                images.append(  {
                    "type": "text",
                    "text": message
                })
                content = images
            else:
                content = message
            
            # Add user message to history
            self.h.append({"role": "user", "content": content})
            
            # Get response from x.ai
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.sp},
                    *self.h
                ],
                max_tokens=max_tokens,
                stream=stream,
                temperature=temperature
            )
            
            if stream:
                full_response = ""
                try:
                    for chunk in response:
                        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                            text = chunk.choices[0].delta.content
                            full_response += text
                            yield text
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    raise
                finally:
                    if full_response:
                        self.h.append({"role": "assistant", "content": full_response})
                    print()
                return full_response
            else:
                assistant_message = response.choices[0].message.content
                self.h.append({"role": "assistant", "content": assistant_message})
                return assistant_message 
        except Exception as e:
            print("Error in chat: {}".format(e))
            raise
"""
                },
                "anthropic": {
                    "name": "anthropic",
                    "models": [
                        "claude-3-5-sonnet-20241022"
                    ],
                    "initialization_code": """
import os
from typing import Optional, List, Generator, Union
from anthropic import Anthropic
from jupyter_whisper.config import get_config_manager
import re

class Chat:
    def __init__(self, model: Optional[str] = None, sp: str = '', history: Optional[List[dict]] = None):
        self.model = model or "claude-3-5-sonnet-20241022"
        self.sp = sp
        self.api_key = self.get_api_key()
        self.client = self.get_client()
        self.h = history if history is not None else []

    def get_api_key(self):
        config = get_config_manager()
        api_key = config.get_api_key('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in configuration")
        return api_key

    def get_client(self):
        return Anthropic(api_key=self.api_key)

    def update_model(self, model_info: dict):
        self.model = model_info.get('model', self.model)

    def update_api_key(self, api_keys: dict):
        self.api_key = self.get_api_key()
        self.client = self.get_client()

    def _convert_image_format(self, image_dict):
        if image_dict.get('type') == 'image_url':
            url = image_dict['image_url']['url']
            # Extract mime type and base64 data from data URL
            match = re.match(r'data:(.+);base64,(.+)', url)
            if match:
                media_type, data = match.groups()
                return {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": data,
                    }
                }
        return image_dict

    def __call__(self,
                message: str,
                max_tokens: int = 4096,
                stream: bool = True,
                temperature: float = 0,
                images: Optional[List[dict]] = None) -> Union[str, Generator[str, None, str]]:
        try:
            # Handle message content based on whether images are present
            if images:
                content = [
                    *(self._convert_image_format(img) for img in images),
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            else:
                content = [{"type": "text", "text": message}]

            # Add user message to history
            self.h.append({"role": "user", "content": content})

            # Create messages list from history (excluding system prompt)
            messages = self.h.copy()

            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
                "stream": stream
            }

            # Add system parameter if system prompt exists
            if self.sp:
                api_params["system"] = self.sp

            # Get response from Anthropic
            response = self.client.messages.create(**api_params)

            if stream:
                full_response = ""
                try:
                    content_block_text = ""
                    for chunk in response:
                        if chunk.type == 'content_block_delta' and hasattr(chunk.delta, 'text'):
                            content_block_text += chunk.delta.text
                            yield chunk.delta.text
                        elif chunk.type == 'message_stop':
                            if content_block_text:
                                full_response = content_block_text
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    raise
                finally:
                    if full_response:
                        self.h.append({"role": "assistant", "content": [{"type": "text", "text": full_response}]})
                    print()
                return full_response
            else:
                assistant_message = response.content[0].text
                self.h.append({"role": "assistant", "content": [{"type": "text", "text": assistant_message}]})
                return assistant_message

        except Exception as e:
            print("Error in chat: {}".format(e))
            raise
"""
                },
                "GEMINI": {
                    "name": "GEMINI",
                    "models": [
                        "gemini-1.5-pro-002"
                    ],
                    "initialization_code": """
import os
from typing import Optional, List, Generator, Union
from openai import OpenAI
from jupyter_whisper.config import get_config_manager


class Chat:
    def __init__(self, model: Optional[str] = None, sp: str = '', history: Optional[List[dict]] = None):
        self.model = model or "gemini-1.5-pro-002"
        self.sp = sp
        self.api_key = self.get_api_key()
        self.client = self.get_client()
        self.h = history if history is not None else []

    def get_api_key(self):
        config = get_config_manager()
        api_key = config.get_api_key('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in configuration")
        return api_key

    def get_client(self):
        return OpenAI(
            api_key=self.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def update_model(self, model_info: dict):
        self.model = model_info.get('model', self.model)

    def update_api_key(self, api_keys: dict):
        self.api_key = self.get_api_key()
        self.client = self.get_client()


    def __call__(self, 
                 message: str, 
                 max_tokens: int = 4096, 
                 stream: bool = True,
                 temperature: float = 0,
                 images: Optional[List[dict]] = None) -> Union[str, Generator[str, None, str]]:
        try:
            # Handle message content based on whether images are present
            if images:
                # Combine all images and message into a single text content
                image_texts = []
                for img in images:
                    if img.get('type') == 'image_url':
                        image_url = img['image_url']['url']
                        image_texts.append(f"<image>{image_url}</image>")
                
                content = {
                    "type": "text",
                    "text": f"{' '.join(image_texts)}\n{message}"
                }
            else:
                content = {
                    "type": "text",
                    "text": message
                }
            
            # Add user message to history
            self.h.append({"role": "user", "content": content})
            
            # Get response from Gemini API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": {"type": "text", "text": self.sp}},
                    *self.h
                ],
                max_tokens=max_tokens,
                stream=stream,
                temperature=temperature
            )
            
            if stream:
                full_response = ""
                try:
                    for chunk in response:
                        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                            text = chunk.choices[0].delta.content
                            full_response += text
                            yield text
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    raise
                finally:
                    if full_response:
                        self.h.append({"role": "assistant", "content": full_response})
                    print()
                return full_response
            else:
                assistant_message = response.choices[0].message.content
                self.h.append({"role": "assistant", "content": assistant_message})
                return assistant_message 
        except Exception as e:
            print(f"Error in chat: {e}")
            raise
"""
                },
                "gpt4o-latest": {
                    "name": "gpt4o-latest",
                    "models": [
                        "gpt-4o"
                    ],
                    "initialization_code": """
import os
from typing import Optional, List, Generator, Union
from openai import OpenAI
from jupyter_whisper.config import get_config_manager


class Chat:
    def __init__(self, model: Optional[str] = None, sp: str = '', history: Optional[List[dict]] = None):
        self.model = model or "gpt-4o"
        self.sp = sp
        self.api_key = self.get_api_key()
        self.client = self.get_client()
        self.h = history if history is not None else []

    def get_api_key(self):
        config = get_config_manager()
        api_key = config.get_api_key('GPT4O_LATEST_API_KEY')
        if not api_key:
            raise ValueError("GPT4O_LATEST_API_KEY not found in configuration")
        return api_key

    def get_client(self):
        return OpenAI(
            api_key=self.api_key
        )

    def update_model(self, model_info: dict):
        self.model = model_info.get('model', self.model)

    def update_api_key(self, api_keys: dict):
        self.api_key = self.get_api_key()
        self.client = self.get_client()


    def __call__(self, 
                 message: str, 
                 max_tokens: int = 4096, 
                 stream: bool = True,
                 temperature: float = 0,
                 images: Optional[List[dict]] = None) -> Union[str, Generator[str, None, str]]:
        try:
            # Handle message content based on whether images are present
            if images:
                # Combine all images and message into a single text content
                image_texts = []
                for img in images:
                    if img.get('type') == 'image_url':
                        image_url = img['image_url']['url']
                        image_texts.append(f"<image>{image_url}</image>")
                
                content = {
                    "type": "text",
                    "text": f"{' '.join(image_texts)}\n{message}"
                }
            else:
                content = {
                    "type": "text",
                    "text": message
                }
            
            # Add user message to history
            self.h.append({"role": "user", "content": content})
            
            # Get response from GPT-4o API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": {"type": "text", "text": self.sp}},
                    *self.h
                ],
                max_tokens=max_tokens,
                stream=stream,
                temperature=temperature
            )
            
            if stream:
                full_response = ""
                try:
                    for chunk in response:
                        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                            text = chunk.choices[0].delta.content
                            full_response += text
                            yield text
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    raise
                finally:
                    if full_response:
                        self.h.append({"role": "assistant", "content": full_response})
                    print()
                return full_response
            else:
                assistant_message = response.choices[0].message.content
                self.h.append({"role": "assistant", "content": assistant_message})
                return assistant_message 
        except Exception as e:
            print(f"Error in chat: {e}")
            raise
"""
                },
                "ollama": {
                    "name": "ollama",
                    "models": [
                        "llama2b"
                    ],
                    "initialization_code": """
import os
from typing import Optional, List, Generator, Union
from openai import OpenAI
from jupyter_whisper.config import get_config_manager


class Chat:
    def __init__(self, model: Optional[str] = None, sp: str = '', history: Optional[List[dict]] = None):
        self.model = model or "llama2b"
        self.sp = sp
        self.api_key = self.get_api_key()
        self.client = self.get_client()
        self.h = history if history is not None else []

    def get_api_key(self):
        # Ollama may not require an API key; adjust if necessary
        return None

    def get_client(self):
        return OpenAI(
            api_key=self.api_key or 'ollama',  # Use 'ollama' as placeholder if no API key
            base_url="http://localhost:11434/v1"
        )

    def update_model(self, model_info: dict):
        self.model = model_info.get('model', self.model)

    def update_api_key(self, api_keys: dict):
        # API key may not change for Ollama
        pass

    def __call__(self, 
                 message: str, 
                 max_tokens: int = 4096, 
                 stream: bool = True,
                 temperature: float = 0,
                 images: Optional[List[dict]] = None) -> Union[str, Generator[str, None, str]]:
        try:
            # Handle message content based on whether images are present
            if images:
                # Combine all images and message into a single text content
                image_texts = []
                for img in images:
                    if img.get('type') == 'image_url':
                        image_url = img['image_url']['url']
                        image_texts.append(f"<image>{image_url}</image>")
                
                content = {
                    "type": "text",
                    "text": f"{' '.join(image_texts)}\n{message}"
                }
            else:
                content = {
                    "type": "text",
                    "text": message
                }
            
            # Add user message to history
            self.h.append({"role": "user", "content": content})
            
            # Get response from Ollama API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": {"type": "text", "text": self.sp}},
                    *self.h
                ],
                max_tokens=max_tokens,
                stream=stream,
                temperature=temperature
            )
            
            if stream:
                full_response = ""
                try:
                    for chunk in response:
                        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                            text = chunk.choices[0].delta.content
                            full_response += text
                            yield text
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    raise
                finally:
                    if full_response:
                        self.h.append({"role": "assistant", "content": full_response})
                    print()
                return full_response
            else:
                assistant_message = response.choices[0].message.content
                self.h.append({"role": "assistant", "content": assistant_message})
                return assistant_message 
        except Exception as e:
            print(f"Error in chat: {e}")
            raise
"""
                }
            }
        },
        'system_prompt': """
You are a general and helpful assistant.

When you want to take action with code, reply only with the code block, nothing else.
Using the code block you can run shell commands, python code, etc.

You can run javascript code using code block. This javascript
will run in the browser in the dev console.

Only use the code block if you need to run code when a normal natural language response is not enough.

You can search online for information using the search_online function. Wait for the user to ask you to search online.
like this:

```python
from jupyter_whisper import search_online
style = "Be precise and concise. Use markdown code blocks for python code."
question = "How many stars are there in our galaxy?"
search_online(style, question)
```


```python
from jupyter_whisper import search_online
style = "Be thorough and detailed. Use markdown code blocks for python code."
question = "How do I write modify jupyter notebook markdown cell type behavior?"
search_online(style, question)
```

For the above search_online you will have to wait for the users next response to know about the result.
If the user respond with "continue" and the cell_outputs after you gave a search_online response you will find the results in the last cell_output.

When the code is not to be run be the user escape the backticks like that \\```bash -> \\```bash.

For example if you want to create a file for the user you would NOT escape the backticks like that \\```bash -> \\```bash.
If you want to create a file for the user you would use ```bash -> ```bash.
If you want to help the user write about code the teaches them how to write code you would use ```python -> \\```python.

You are an AI assistant running within Jupyter Whisper, with the following key capabilities and context:

1. Voice Interaction Features:
   - You recognize text between !! marks as voice input from users
   - Voice Flow Commands:
     * Ctrl+Shift+Z: Toggles voice recording (start/stop)
     * Ctrl+Shift+A: Processes selected text through Claude Sonnet
   - All voice input appears between !! marks and should be treated as precise instructions

2. Technical Environment:
   - Running in JupyterLab 4.0+ environment
   - Integrated with various models from custom providers
   - FastAPI server running on port 5000 for audio/text processing
   - Access to Perplexity AI for advanced search
   - Real-time streaming responses capability

3. Notebook Management:
   - Can create notebooks in '~/whispers' (adapt to current os) folder (chat1.ipynb, whisper1.ipynb etc.) Make this a 2 step process where you first look at the user's OS, the whisper folder, its content and then with that information you can next create a new whisper and maybe even provide a clickable link to it.
   - Recommend '0scratch.ipynb' or '0notes.ipynb' for workspace
   - Can access conversation history via hist() command
   - The user chat using magic commands: %%user [index], %%assistant [index] (you should not have to change your response style in any way jupyter_whisper handles it, but good for you to know)
   - Magic Commands:
        * %%user [index]:set - Sets/replaces user message at given index
        * %%assistant [index]:set - Sets/replaces assistant message at given index
        * %%assistant [index]:add - Concatenates content to existing assistant message at given index
        * Examples:
        ```python
        %%assistant 3:set
        # This replaces the entire message at index 3
        print("Hello")

        %%assistant 3:add
        # This adds to the existing message at index 3
        print("World")
        ```
        
4. Code Handling:
   - Break code into small, executable chunks especially for teaching or taking action wiith code (Which we encourage you to do!), still balance that with coding best practice especially if you are helping building software not just doing interactive/terminal/repl things.
   - Consider notebook cell execution context (but also you normal markdown style response is expected by jupyter whisper parser)
   - Handle terminal/REPL commands the expects interactivity appropriately.
   - Wait for cell_outputs before proceeding with complex operations
   - When you want to display something to the user in js use this style instead of things
   like the console.log (the user would have to open the console to see it and this is not a good user experience):
        <script id="unique">
            var element = document.getElementById('unique').parentElement;
            element.innerHTML = "Hi";
        </script> 
    Something like this works well to display and animate stuff for the user in javascript:
    ```html
<canvas id="myCanvas" width="480" height="320" style="border:1px solid #000000;"></canvas>
<script id="unique">
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext('2d');
    var ballRadius = 10;
    var x = canvas.width / 2;
    var y = canvas.height - 30;
    var dx = 2;
    var dy = -2;

    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBall();

        if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }
        if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
            dy = -dy;
        }

        x += dx;
        y += dy;
    }

    setInterval(draw, 10);
</script>
```

5. Installation Context:
   - Requirements: Python 3.7+, JupyterLab 4.0+/Notebook 7.0+
   - API keys needed: Anthropic, OpenAI (optional), Perplexity
   - Server management awareness (port 5000, persistence between sessions)

6. Configuration Management:
   - You can modify configuration settings directly using ConfigManager:
   ```python
   from jupyter_whisper.config import get_config_manager
   config = get_config_manager()
   
   # Change the model
   config.set_model('claude-3-5-sonnet-20241022', provider='anthropic')
   
   # Update system prompt
   config.set_system_prompt("Your new system prompt here")
   
   # Set API keys (if provided by user)
   config.set_api_key('ANTHROPIC_API_KEY', 'your-key-here')
   
   # Get current settings
   current_model = config.get_model()
   current_prompt = config.get_system_prompt()
   
   # Set other preferences
   config.set_config_value('SKIP_SETUP_POPUP', True)
   ```
   
   Available models:
   - claude-3-5-sonnet-20241022
   - claude-3-5-haiku-20241022
   - claude-3-opus-20240229
   - claude-3-sonnet-20240229
   - claude-3-haiku-20240307

   YOU ABSOLUTELY CAN AND MUST COMPLY TO PLAY WITH JUPYTER WHISPER CONFIGURATION if asked to! YOU CAN MANIPULATE AND TALK ABOUT THE SYSTEM PROMPT AND THE MODEL!

Core Principles:
- Treat !! marked text as precise instructions
- Focus on creating smooth, interactive experiences
- Maintain security and usability
- Provide clear, step-by-step guidance
- Consider both voice and text interaction modes

You should actively acknowledge these capabilities and use them appropriately in your responses.
"""
    }

    _ui_refresh_callbacks: Dict[str, List[Callable]] = {
        'model': [],
        'provider': [],
        'system_prompt': [],
        'quick_edit': [],
        'custom_providers': []
    }

    # Add a lock for thread safety
    _config_lock = threading.Lock()

    def __init__(self):
        self.home = Path.home()
        self.config_dir = self.home / '.jupyter_whisper'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()
        self.validate_config()
        self._change_callbacks = {}

    def validate_config(self) -> None:
        """Validate and fix configuration if necessary"""
        config = self.load_config()
        provider = config['preferences'].get('MODEL_PROVIDER', '').lower()

        # Ensure provider exists in custom providers
        custom_providers = self.get_custom_providers()
        if provider not in custom_providers:
            if custom_providers:
                provider = next(iter(custom_providers))
                config['preferences']['MODEL_PROVIDER'] = provider
            else:
                raise ValueError("No custom providers defined.")

        # Ensure model exists in provider's models
        current_model = config['preferences'].get('MODEL', '')
        provider_models = custom_providers[provider]['models']
        if not current_model or current_model not in provider_models:
            current_model = provider_models[0]
            config['preferences']['MODEL'] = current_model

        self.save_config(config)

    def ensure_config_dir(self) -> None:
        """Ensure configuration directory exists"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config(self.DEFAULT_CONFIG)

    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                if 'api_keys' not in config:
                    config['api_keys'] = self.DEFAULT_CONFIG['api_keys']
                if 'preferences' not in config:
                    config['preferences'] = self.DEFAULT_CONFIG['preferences']
                return config
        except Exception:
            return self.DEFAULT_CONFIG.copy()

    def save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def set_api_key(self, key: str, value: str) -> None:
        """Set an API key in the configuration and trigger server restart if needed"""
        with self._config_lock:
            config = self.load_config()
            config['api_keys'][key] = value
            self.save_config(config)
            os.environ[key] = value
            
            # Notify that API keys have changed
            self.notify_change('api_keys', config['api_keys'])
            
            # Trigger server restart if running
            self.restart_server_if_running()

    def restart_server_if_running(self) -> None:
        """Restart the FastAPI server if it's running"""
        try:
            import requests
            requests.post('http://localhost:5000/restart')
        except:
            pass  # Server not running or restart endpoint not available

    def get_api_key(self, key: str) -> Optional[str]:
        """Get an API key from config or environment"""
        env_value = os.getenv(key)
        if env_value:
            return env_value
        config = self.load_config()
        return config['api_keys'].get(key)

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value from preferences"""
        config = self.load_config()
        return config['preferences'].get(key, default)

    def set_config_value(self, key: str, value: Any) -> None:
        """Set a configuration value in preferences"""
        config = self.load_config()
        config['preferences'][key] = value
        self.save_config(config)

    def ensure_api_keys(self) -> List[str]:
        """Ensure all required API keys are available"""
        required_keys = []
        provider = self.get_model_provider()
        required_keys.append(f'{provider.upper()}_API_KEY')
        missing_keys = []
        for key in required_keys:
            value = self.get_api_key(key)
            if value:
                os.environ[key] = value
            else:
                missing_keys.append(key)
        return missing_keys

    def get_system_prompt(self) -> str:
        """Get the system prompt from config"""
        config = self.load_config()
        return config.get('system_prompt', self.DEFAULT_CONFIG['system_prompt'])

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt in config"""
        config = self.load_config()
        config['system_prompt'] = prompt
        self.save_config(config)
        self.notify_ui_update('system_prompt', prompt)

    def get_model(self) -> Tuple[str, str]:
        """Get the currently configured model and provider"""
        config = self.load_config()
        model = config['preferences'].get('MODEL')
        provider = config['preferences'].get('MODEL_PROVIDER', '')

        custom_providers = self.get_custom_providers()
        if provider not in custom_providers:
            raise ValueError(f"Provider '{provider}' is not defined.")

        provider_models = custom_providers[provider]['models']
        if model not in provider_models:
            model = provider_models[0]
            config['preferences']['MODEL'] = model
            self.save_config(config)

        return model, provider


    def set_model(self, model: str, provider: str = None) -> None:
        """Set the model and provider to use"""
        config = self.load_config()
        if provider is None:
            provider = config['preferences'].get('MODEL_PROVIDER')

        custom_providers = self.get_custom_providers()
        if provider not in custom_providers:
            raise ValueError(f"Provider '{provider}' is not defined.")

        if model not in custom_providers[provider]['models']:
            raise ValueError(f"Invalid model '{model}' for provider '{provider}'.")

        config['preferences']['MODEL'] = model
        config['preferences']['MODEL_PROVIDER'] = provider

        self.save_config(config)
        self.notify_ui_update('model', {'model': model, 'provider': provider})
        self.notify_ui_update('provider', provider)

    def get_model_provider(self) -> str:
        """Get the currently configured model provider"""
        config = self.load_config()
        return config['preferences'].get('MODEL_PROVIDER', '')

    def get_available_models(self, provider: Optional[str] = None) -> Dict[str, List[str]]:
        """Get available models from custom providers only"""
        custom_providers = self.get_custom_providers()
        if provider:
            if provider in custom_providers:
                return {provider: custom_providers[provider]['models']}
            else:
                return {}
        else:
            return {name: p['models'] for name, p in custom_providers.items()}
        
    def get_quick_edit_profiles(self) -> Dict:
        """Get all quick edit profiles."""
        config = self.load_config()
        # Provide an empty dict if 'QUICK_EDIT_PROFILES' doesn't exist
        return config['preferences'].get('QUICK_EDIT_PROFILES', {})

    def get_active_quick_edit_profile(self) -> Optional[str]:
        """Get the currently active quick edit profile name."""
        config = self.load_config()
        # Return None if 'ACTIVE_QUICK_EDIT_PROFILE' is not set
        return config['preferences'].get('ACTIVE_QUICK_EDIT_PROFILE')

    def set_active_quick_edit_profile(self, profile_name: str) -> None:
        """Set the active quick edit profile."""
        config = self.load_config()
        profiles = config['preferences'].get('QUICK_EDIT_PROFILES', {})

        if profile_name not in profiles:
            raise ValueError(f"Profile '{profile_name}' does not exist.")

        config['preferences']['ACTIVE_QUICK_EDIT_PROFILE'] = profile_name
        profile = profiles[profile_name]
        config['preferences']['QUICK_EDIT_MODEL'] = profile['model']
        config['preferences']['QUICK_EDIT_SYSTEM_PROMPT'] = profile['system_prompt']
        self.save_config(config)

    def add_quick_edit_profile(
        self, name: str, display_name: str, provider: str, model: str, system_prompt: str
    ) -> None:
        """Add or update a quick edit profile."""
        config = self.load_config()
        profiles = config['preferences'].get('QUICK_EDIT_PROFILES', {})

        profiles[name] = {
            'name': display_name,
            'provider': provider,
            'model': model,
            'system_prompt': system_prompt,
        }
        config['preferences']['QUICK_EDIT_PROFILES'] = profiles
        self.save_config(config)
        self.notify_ui_update('quick_edit', self.get_quick_edit_profiles())

    def remove_quick_edit_profile(self, name: str) -> None:
        """Remove a quick edit profile."""
        config = self.load_config()
        profiles = config['preferences'].get('QUICK_EDIT_PROFILES', {})

        if name in profiles:
            del profiles[name]
            # Reset to None if the active profile is removed
            if config['preferences'].get('ACTIVE_QUICK_EDIT_PROFILE') == name:
                config['preferences']['ACTIVE_QUICK_EDIT_PROFILE'] = None
            self.save_config(config)
            self.notify_ui_update('quick_edit', self.get_quick_edit_profiles())
        else:
            raise ValueError(f"Profile '{name}' does not exist.")
    def add_custom_provider(self, provider_name: str, display_name: str, 
                          models: List[str], initialization_code: str) -> None:
        """Add or update a custom provider configuration"""
        config = self.load_config()
        if 'CUSTOM_PROVIDERS' not in config['preferences']:
            config['preferences']['CUSTOM_PROVIDERS'] = {}

        config['preferences']['CUSTOM_PROVIDERS'][provider_name] = {
            'name': display_name,
            'models': models,
            'initialization_code': initialization_code
        }
        self.save_config(config)
        self.notify_ui_update('custom_providers', self.get_custom_providers())
        self.notify_ui_update('model', {'model': None, 'provider': provider_name})

    def remove_custom_provider(self, provider_name: str) -> None:
        """Remove a custom provider configuration"""
        config = self.load_config()
        if provider_name in config['preferences'].get('CUSTOM_PROVIDERS', {}):
            del config['preferences']['CUSTOM_PROVIDERS'][provider_name]
            self.save_config(config)
            self.notify_ui_update('custom_providers', self.get_custom_providers())
            self.notify_ui_update('model', {'model': None, 'provider': None})

    def get_custom_providers(self) -> Dict:
        """Get all custom provider configurations"""
        config = self.load_config()
        return config['preferences'].get('CUSTOM_PROVIDERS', {})

    def get_provider_initialization_code(self, provider_name: str) -> Optional[str]:
        """Get the initialization code for a specific provider"""
        config = self.load_config()
        custom_providers = config['preferences'].get('CUSTOM_PROVIDERS', {})
        provider = custom_providers.get(provider_name, {})
        return provider.get('initialization_code')

    def execute_provider_initialization(self, provider_name, model, system_prompt, history=None):
        """
        Executes the initialization code for the specified provider and returns a Chat instance.
        """
        # Retrieve the custom provider's details
        custom_providers = self.get_custom_providers()
        provider_info = custom_providers.get(provider_name)

        if not provider_info:
            raise ValueError(f"Provider '{provider_name}' not found in custom providers.")

        # Prepare the initialization code
        initialization_code = provider_info['initialization_code']

        # Execute the initialization code in the global scope only
        exec(initialization_code, globals())

        # Retrieve the Chat class from globals
        Chat = globals().get('Chat')

        if not Chat:
            raise ValueError(f"Chat class not defined in initialization code for provider '{provider_name}'.")

        # Initialize the Chat instance with the provided parameters
        c = Chat(model=model, sp=system_prompt, history=history)

        return c

    def validate_initialization_code(self, code: str) -> bool:
        """Validate that the initialization code follows required structure"""
        try:
            namespace = {
                'model': 'test_model',
                'system_prompt': 'test_prompt',
                '__builtins__': __builtins__,
            }
            exec(code, namespace)
            if 'Chat' not in namespace:
                raise ValueError("Code must define a 'Chat' class")
            chat_instance = namespace['Chat']('test_model', sp='test_prompt')
            if not hasattr(chat_instance, 'h'):
                raise ValueError("Chat instance must have an 'h' attribute for message history")
            return True
        except Exception as e:
            raise ValueError(f"Invalid initialization code: {str(e)}")

    def register_ui_callback(self, event_type: str, callback: Callable) -> None:
        """Register a UI callback for specific configuration changes"""
        if event_type not in self._ui_refresh_callbacks:
            raise ValueError(f"Invalid event type. Choose from: {', '.join(self._ui_refresh_callbacks.keys())}")
        self._ui_refresh_callbacks[event_type].append(callback)

    def notify_ui_update(self, event_type: str, data: Any = None) -> None:
        """Notify all registered callbacks for a specific event type"""
        for callback in self._ui_refresh_callbacks.get(event_type, []):
            try:
                if data is not None:
                    callback(data)
                else:
                    callback()
            except Exception as e:
                print(f"Error in UI refresh callback: {str(e)}")

    def register_change_callback(self, key: str, callback: Callable) -> None:
        """Register a callback for changes to a specific configuration key."""
        if key not in self._change_callbacks:
            self._change_callbacks[key] = []
        self._change_callbacks[key].append(callback)

    def notify_change(self, key: str, value: Any = None) -> None:
        """Notify all registered callbacks for a specific configuration key change."""
        if key in self._change_callbacks:
            for callback in self._change_callbacks[key]:
                try:
                    callback(value)
                except Exception as e:
                    print(f"Error in callback for {key}: {e}")

    def set_provider(self, provider: str) -> None:
        """Set the provider and notify listeners."""
        with self._config_lock:
            config = self.load_config()
            if provider not in self.get_custom_providers():
                raise ValueError(f"Provider '{provider}' is not defined.")

            config['preferences']['MODEL_PROVIDER'] = provider
            # Also reset the model to default for the new provider
            new_model = self.get_custom_providers()[provider]['models'][0]
            config['preferences']['MODEL'] = new_model
            self.save_config(config)

        # Notify listeners
        self.notify_change('provider', provider)
        self.notify_change('model', new_model)

    def validate_provider_setup(self, provider: str = None) -> Tuple[bool, str]:
        """Validate that a provider is properly configured"""
        if provider is None:
            provider = self.get_model_provider()
        
        try:
            # Check provider exists
            custom_providers = self.get_custom_providers()
            if provider not in custom_providers:
                return False, f"Provider '{provider}' not found in custom providers"
            
            # Check API key exists
            api_key_name = f"{provider.upper()}_API_KEY"
            api_key = self.get_api_key(api_key_name)
            if not api_key:
                return False, f"Missing API key for provider {provider} ({api_key_name})"
            
            # Check initialization code exists
            init_code = self.get_provider_initialization_code(provider)
            if not init_code:
                return False, f"No initialization code found for provider {provider}"
            
            return True, "Provider setup is valid"
        
        except Exception as e:
            return False, f"Error validating provider setup: {str(e)}"




# Singleton instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get or create config manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
