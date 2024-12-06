from typing import List, Literal, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from ._internal_types import (
    KeywordsAIParams,
    BasicLLMParams,
    KeywordsAIBaseModel,
    Customer,
)

"""
Conventions:

1. KeywordsAI as a prefix to class names
2. Params as a suffix to class names

Logging params types:
1. TEXT
2. EMBEDDING
3. AUDIO
4. GENERAL_FUNCTION
"""


class KeywordsAITextLogParams(KeywordsAIParams, BasicLLMParams):

    @field_validator("customer_params", mode="after")
    def validate_customer_params(cls, v: Customer):
        if v.customer_identifier is None:
            return None
        return v

    @model_validator(mode="before")
    def _preprocess_data(cls, data):
        data = KeywordsAIParams._preprocess_data(data)
        return data

    def serialize_for_logging(self) -> dict:
        # Fields to include in logging, grouped by category
        FIELDS_TO_INCLUDE = {
            # Request Identification
            "ip_address",            # Client IP address
            "unique_id",            # Unique request identifier
            "prompt_id",            # Prompt identifier
            "thread_identifier",    # Thread tracking ID
            "custom_identifier",    # User-provided identifier
            
            # Request Status & Control
            "blurred",              # Whether log is blurred due to unpaid balance
            "status",               # Request status
            "status_code",          # HTTP status code
            "cached",               # Whether response was cached
            "cache_bit",            # Cache control flag
            "is_test",              # Test request flag
            "environment",          # Deployment environment
            
            # Token & Cost Metrics
            "prompt_tokens",        # Number of tokens in prompt
            "completion_tokens",    # Number of tokens in completion
            "total_request_tokens", # Total tokens used
            "cost",                 # Total cost
            "amount_to_pay",        # Billable amount
            "evaluation_cost",      # Cost of evaluation
            "tokens_per_second",    # Token generation speed
            
            # Performance Metrics
            "latency",              # Overall request latency
            "time_to_first_token",  # Time until first token generated
            
            # Model & Configuration
            "model",                # Language model used
            "temperature",          # Randomness parameter
            "max_tokens",           # Maximum tokens to generate
            "logit_bias",          # Token probability adjustments
            "logprobs",            # Token probability logging
            "top_logprobs",        # Top token probabilities
            "frequency_penalty",    # Repetition penalty
            "presence_penalty",     # Topic steering penalty
            "stop",                # Stop sequences
            "n",                   # Number of completions
            "response_format",      # Expected response format
            
            # User & Organization
            "user_id",             # User identifier
            "organization_id",      # Organization identifier
            "organization_key_id",  # Organization API key ID
            "customer_identifier", # Customer identifier
            "customer_email",      # Customer email
            "used_custom_credential", # Custom credential usage
            "covered_by",          # Cost coverage source
            
            # Messages & Content
            "prompt_messages",      # Input messages
            "completion_message",   # Final completion
            "completion_messages",  # All completion messages
            "full_request",        # Complete request data
            "full_response",       # Complete response data
            
            # Tool Usage
            "tools",               # Available tools
            "tool_choice",         # Selected tool
            "tool_calls",          # Tool call records
            "has_tool_calls",      # Tool usage flag
            "parallel_tool_calls", # Parallel tool execution
            
            # Evaluation & Analysis
            "evaluation_identifier", # Evaluation ID
            "for_eval",            # Evaluation flag
            
            # Metadata & Diagnostics
            "metadata",            # Additional metadata
            "keywordsai_params",   # API parameters
            "stream",              # Streaming flag
            "stream_options",      # Streaming configuration
            "warnings",            # Warning messages
            "recommendations",     # Improvement suggestions
            "error_message",       # Error description
            "log_method",          # Logging method
            "log_type",           # Type of log entry
        }
        
        if self.disable_log:
            FIELDS_TO_INCLUDE.discard("full_request")
            FIELDS_TO_INCLUDE.discard("full_response")
            FIELDS_TO_INCLUDE.discard("tool_calls")
            FIELDS_TO_INCLUDE.discard("prompt_messages")
            FIELDS_TO_INCLUDE.discard("completion_messages")
            FIELDS_TO_INCLUDE.discard("completion_message")

        # Get all non-None values using model_dump
        data = self.model_dump(exclude_none=True)

        # Filter to only include fields that exist in Django model
        return {k: v for k, v in data.items() if k in FIELDS_TO_INCLUDE}

    model_config = ConfigDict(from_attributes=True)


class SimpleLogStats(KeywordsAIBaseModel):
    """
    Add default values to account for cases of error logs
    """

    total_request_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost: float = 0
    organization_id: int
    user_id: int
    organization_key_id: str
    model: str | None = None
    metadata: dict | None = None
    used_custom_credential: bool = False

    def __init__(self, **data):
        for field_name in self.__annotations__:
            if field_name.endswith("_id"):
                related_model_name = field_name[:-3]  # Remove '_id' from the end
                self._assign_related_field(related_model_name, field_name, data)

        super().__init__(**data)
