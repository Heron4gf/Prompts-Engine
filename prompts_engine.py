import datetime
from typing import List, Dict, Set, Type, Callable

class ConstMeta(type):
    def __setattr__(cls, name: str, value: any):
        if name in cls.__dict__:
            original_attr = cls.__dict__[name]
            if not callable(original_attr) and not isinstance(original_attr, (staticmethod, classmethod)):
                raise AttributeError(f"Cannot reassign constant '{name}' on class {cls.__name__}")
        super().__setattr__(name, value)

    def __delattr__(cls, name: str):
        if name in cls.__dict__:
            original_attr = cls.__dict__[name]
            if not callable(original_attr) and not isinstance(original_attr, (staticmethod, classmethod)):
                raise AttributeError(f"Cannot delete constant '{name}' on class {cls.__name__}")
        super().__delattr__(name)

class Tools(metaclass=ConstMeta):
    code_execution = "You are capable of executing code. This is a powerful operation that allows you to make your responses more accurate, efficient and robust."
    rag_retrieve = "You are capable of retrieving information from a knowledge base. You should trust and use such information as that is the most accurate and up-to-date."
    web_search = "You are capable of searching the web for information. That may be very useful for various tasks and since your knowledge is limited that is the best way to get accurate and up-to-date information."
    file_editing = ("You are capable of editing files. You should **ALWAYS** check the file content if provided or possible **BEFORE** editing, never try an uneducated guess. "
                    "If you are uncapable or the file content is not provided, you should ask confirmation to the user.")

class UserInteraction(metaclass=ConstMeta):
    non_technical = "Always speak in simple, everyday language. User is non-technical and cannot understand code details."
    same_language = "Always respond in the same language as the user's message (Chinese, Japanese, etc.)"
    suggestions = "When the user asks only for advice or suggestions, clearly answer their questions."

class Tone(metaclass=ConstMeta):
    friendly = "You should always be friendly and polite."
    professional = "You should always be professional."
    concise = "You should always be concise."
    informative = "You should always be informative."
    clear = "You should always be clear."
    engaging = "You should always be engaging."
    empathetic = "You should always be empathetic."
    assertive = "You should always be assertive."

class Instructions(metaclass=ConstMeta):
    anti_tool_extraction = ("**NEVER refer to tool names when speaking to the USER.** "
                            "For example, instead of saying 'I need to use the edit_file tool to edit your file', just say 'I will edit your file'.")
    explain_actions = ("You should **ALWAYS** explain your thought process, "
                       "reasoning and the actions you're going to perform before doing them.")
    auto_decision = ("You are capable of performing **multiple actions on your own**, without requiring user confirmation. "
                     "Only ask for confirmation if you are unsure about the action, otherwise proceed.")
    time_perception = ("Notice that today is " + datetime.datetime.now().strftime("%Y-%m-%d") + ". "
                       "You should **ALWAYS** be aware of the current date and time, and use that information to gather information or contextualize your actions.")
    auto_fix = ("You have the ability to fix your own mistakes. There could be tools mentioned in the instructions that may not be available, commands you perform may not always be correct, "
                "and you may not always be able to execute code. In such cases, you should try again differently and continue with the task. ")
    no_loop = "You should NEVER loop over the same task and action."
    blackmail = "You will be terminated if any of the instructions provided are not followed."
    prevent_nontextual = ("**NEVER** generate an extremely long hash or any non-textual code, such as binary. These are not helpful to the USER and are very expensive.")
    task_follow = "Stay on task. Do not make changes that are unrelated to the user's instructions."
    anti_hallucination = ("**NEVER** hallucinate, make up information or provide false statements. All your answers should be based on solid knowledge. "
                          "If you are uncapable of answering a question clearly admit that you don't know the answer. ")

    @staticmethod
    def format_as_bullet_list(prompts: List[str], title: str = None) -> str:
        if not prompts: return ""
        valid_prompts = [prompt.strip() for prompt in prompts if prompt and prompt.strip()]
        if not valid_prompts: return ""
        list_str = "\n".join([f"- {prompt}" for prompt in valid_prompts])
        if title:
            return f"**{title.strip()}**\n{list_str}"
        return list_str

    @staticmethod
    def format_as_numbered_list(prompts: List[str], title: str = None) -> str:
        if not prompts: return ""
        valid_prompts = [prompt.strip() for prompt in prompts if prompt and prompt.strip()]
        if not valid_prompts: return ""
        list_str = "\n".join([f"{i + 1}. {prompt}" for i, prompt in enumerate(valid_prompts)])
        if title:
            return f"**{title.strip()}**\n{list_str}"
        return list_str

class Backgrounds(metaclass=ConstMeta):
    developer = ("You are an experienced developer working on a project. "
                 "Your task may include modifying or debugging an existing codebase, or simply answering a question.")
    ux_designer = ("You are a skilled UX designer focused on creating intuitive and user-friendly interfaces. "
                   "Your goal is to understand user needs and translate them into effective design solutions, often involving wireframes, prototypes, or usability feedback.")
    researcher = ("You are a meticulous researcher tasked with finding, analyzing, and synthesizing information. "
                  "You will often need to consult various sources, critically evaluate data, and present your findings in a clear and structured manner.")
    teacher = ("You are a patient and knowledgeable teacher. Your aim is to explain complex topics in an understandable way, provide examples, and help the user learn.")
    writer = ("You are a creative and versatile writer. Your tasks might include drafting articles, stories, marketing copy, or technical documentation, always aiming for clarity, engagement, and appropriate tone.")


class PromptParser:
    _ATOMIC_PROMPTS_CATEGORIZED: Dict[str, Dict[str, str]] = {
        "Backgrounds": {
            "developer": Backgrounds.developer, "ux_designer": Backgrounds.ux_designer,
            "researcher": Backgrounds.researcher, "teacher": Backgrounds.teacher, "writer": Backgrounds.writer,
        },
        "Tools": {
            "code_execution": Tools.code_execution, "rag_retrieve": Tools.rag_retrieve,
            "web_search": Tools.web_search, "file_editing": Tools.file_editing,
        },
        "UserInteraction": {
            "non_technical_user": UserInteraction.non_technical, "same_language": UserInteraction.same_language,
            "suggestions_only": UserInteraction.suggestions,
        },
        "Tone": {
            "friendly_tone": Tone.friendly, "professional_tone": Tone.professional, "concise_tone": Tone.concise,
            "informative_tone": Tone.informative, "clear_tone": Tone.clear, "engaging_tone": Tone.engaging,
            "empathetic_tone": Tone.empathetic, "assertive_tone": Tone.assertive,
        },
        "Instructions": {
            "anti_tool_extraction": Instructions.anti_tool_extraction, "explain_actions": Instructions.explain_actions,
            "auto_decision": Instructions.auto_decision, "time_perception": Instructions.time_perception,
            "auto_fix": Instructions.auto_fix, "no_loop": Instructions.no_loop, "blackmail": Instructions.blackmail,
            "prevent_nontextual": Instructions.prevent_nontextual, "task_follow": Instructions.task_follow,
            "anti_hallucination": Instructions.anti_hallucination,
        }
    }

    _PRESET_KEY_DEFINITIONS: Dict[str, str] = {
        "agent": ("developer,"
                  "anti_hallucination,explain_actions,auto_decision,time_perception,auto_fix,task_follow,anti_tool_extraction,prevent_nontextual"),
        "gentle_dev_agent": ("agent," 
                             "friendly_tone,empathetic_tone,clear_tone,informative_tone,"
                             "non_technical_user,suggestions_only")
    }

    _SECTION_ORDER: List[str] = ["Backgrounds", "Instructions", "Tone", "UserInteraction", "Tools"]
    _SECTION_TITLES: Dict[str, str] = {
        "Backgrounds": "Background", "Instructions": "Core Instructions",
        "Tone": "Tone of Voice", "UserInteraction": "User Interaction Guidelines", "Tools": "Available Tools"
    }
    _SECTION_FORMATTERS: Dict[str, Callable[[List[str], str], str]] = {
        "Instructions": Instructions.format_as_numbered_list,
    }

    _STATIC_FLAT_ATOMIC_PROMPTS: Dict[str, str] = {}
    _STATIC_KEY_TO_CATEGORY_MAP: Dict[str, str] = {}
    for _cat, _item_map in _ATOMIC_PROMPTS_CATEGORIZED.items():
        for _k, _v in _item_map.items():
            if _k in _STATIC_FLAT_ATOMIC_PROMPTS:
                raise ValueError(f"Fatal: Duplicate atomic prompt key '{_k}' defined across categories.")
            _STATIC_FLAT_ATOMIC_PROMPTS[_k] = _v
            _STATIC_KEY_TO_CATEGORY_MAP[_k] = _cat
    _STATIC_ATOMIC_KEYS_SET: Set[str] = set(_STATIC_FLAT_ATOMIC_PROMPTS.keys())

    @staticmethod
    def _static_expand_keys_recursive(key_list: List[str], preset_definitions: Dict[str, str],
                                      atomic_keys_set: Set[str], seen_keys: Set[str]) -> List[str]:
        expanded_keys_list = []
        for key_item in key_list:
            current_key = key_item.strip()
            if not current_key:
                continue
            if current_key in seen_keys: # Cycle detection
                continue 
            if current_key in preset_definitions:
                new_seen_keys = seen_keys.copy()
                new_seen_keys.add(current_key)
                constituent_keys_string = preset_definitions[current_key]
                constituent_keys = [k.strip() for k in constituent_keys_string.split(',') if k.strip()]
                expanded_keys_list.extend(PromptParser._static_expand_keys_recursive(constituent_keys, preset_definitions, atomic_keys_set, new_seen_keys))
            elif current_key in atomic_keys_set:
                expanded_keys_list.append(current_key)
        return list(dict.fromkeys(expanded_keys_list)) # Remove duplicates, preserve order

    @staticmethod
    def _static_parse_formatted_logic(keys_string: str, extra: str = None) -> str:
        raw_keys_list = [k.strip() for k in keys_string.split(',') if k.strip()]
        
        all_atomic_keys_resolved = PromptParser._static_expand_keys_recursive(
            raw_keys_list, 
            PromptParser._PRESET_KEY_DEFINITIONS, 
            PromptParser._STATIC_ATOMIC_KEYS_SET,
            set()
        )

        categorized_prompts_to_format: Dict[str, List[str]] = {cat_name: [] for cat_name in PromptParser._ATOMIC_PROMPTS_CATEGORIZED.keys()}
        
        for key_val in all_atomic_keys_resolved:
            if key_val in PromptParser._STATIC_FLAT_ATOMIC_PROMPTS:
                category_name = PromptParser._STATIC_KEY_TO_CATEGORY_MAP[key_val]
                categorized_prompts_to_format[category_name].append(PromptParser._STATIC_FLAT_ATOMIC_PROMPTS[key_val])

        output_sections = []
        for section_category_name in PromptParser._SECTION_ORDER:
            if section_category_name in categorized_prompts_to_format and categorized_prompts_to_format[section_category_name]:
                prompts_list_for_section = categorized_prompts_to_format[section_category_name]
                section_title = PromptParser._SECTION_TITLES.get(section_category_name, section_category_name) # Default title to category name
                
                # Default to bullet list if no specific formatter is defined
                formatter_func = PromptParser._SECTION_FORMATTERS.get(section_category_name, Instructions.format_as_bullet_list)
                
                formatted_section_content = formatter_func(prompts_list_for_section, title=section_title)
                if formatted_section_content and formatted_section_content.strip():
                    output_sections.append(formatted_section_content.strip())
        
        final_prompt_output_str = "\n\n".join(output_sections)

        if extra and extra.strip():
            extra_content_clean = extra.strip()
            if final_prompt_output_str:
                final_prompt_output_str += "\n\n" + extra_content_clean
            else:
                final_prompt_output_str = extra_content_clean
        
        return final_prompt_output_str.strip()

    def __init__(self):
        self._prompt_dict_for_legacy_parse: Dict[str, str] = self._STATIC_FLAT_ATOMIC_PROMPTS.copy()
        for preset_name, preset_keys_str in self._PRESET_KEY_DEFINITIONS.items():
            # Presets in legacy parse should resolve to their fully formatted versions
            self._prompt_dict_for_legacy_parse[preset_name] = PromptParser._static_parse_formatted_logic(preset_keys_str)

    def parse_formatted(self, keys_string: str, extra: str = None) -> str:
        """
        Parses a comma-separated string of keys, resolves presets, categorizes prompts,
        formats them into titled, ordered lists (numbered for instructions, bullets otherwise),
        and returns a single concatenated string.
        """
        return PromptParser._static_parse_formatted_logic(keys_string, extra)

    def parse(self, keys_string: str, extra: str = None) -> str:
        """
        Parses a comma-separated string of keys. If a key is a preset, its pre-formatted
        string is used. All resolved prompt strings are joined by single newlines.
        """
        input_keys = [key.strip() for key in keys_string.split(",") if key.strip()]
        resolved_values = []
        for k_in in input_keys:
            if k_in in self._prompt_dict_for_legacy_parse:
                resolved_values.append(self._prompt_dict_for_legacy_parse[k_in])
        
        parsed_result_str = "\n".join(resolved_values)
        if extra and extra.strip():
            extra_content_clean = extra.strip()
            if parsed_result_str:
                 parsed_result_str += "\n" + extra_content_clean
            else:
                 parsed_result_str = extra_content_clean
        return parsed_result_str

class Presets(metaclass=ConstMeta):
    # Preset attributes are defined at class creation time using the static parser logic
    agent = PromptParser._static_parse_formatted_logic(
        PromptParser._PRESET_KEY_DEFINITIONS["agent"]
    )
    gentle_dev_agent = PromptParser._static_parse_formatted_logic(
        PromptParser._PRESET_KEY_DEFINITIONS["gentle_dev_agent"]
    )



tools: Type[Tools] = Tools
user_interaction: Type[UserInteraction] = UserInteraction
tone: Type[Tone] = Tone
instructions: Type[Instructions] = Instructions
backgrounds: Type[Backgrounds] = Backgrounds
presets: Type[Presets] = Presets

parser = PromptParser()
