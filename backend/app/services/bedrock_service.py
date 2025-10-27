"""
Bedrock Service - Wrapper for AWS Bedrock API calls
"""
import json
import boto3
import os
from typing import Dict, Any, Optional, List
from botocore.exceptions import ClientError


class BedrockService:
    """Service for interacting with AWS Bedrock."""

    def __init__(self, region_name: str = None, model_id: Optional[str] = None):
        # Read from environment variables
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")

        self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=self.region_name)
        self.bedrock = boto3.client("bedrock", region_name=self.region_name)

    def invoke_model(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        model_id: Optional[str] = None
    ) -> str:
        """
        Invoke a Bedrock model with a prompt.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            model_id: Override default model ID

        Returns:
            The model's text response
        """
        model = model_id or self.model_id

        # Build messages
        messages = [{"role": "user", "content": prompt}]

        # Build request body
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature
        }

        # Add system prompt if provided
        if system_prompt:
            body["system"] = system_prompt

        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model,
                body=json.dumps(body)
            )

            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']

        except ClientError as e:
            raise Exception(f"Bedrock API error: {str(e)}")

    def invoke_model_with_response_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """
        Invoke model with streaming response.

        Yields chunks of text as they arrive.
        """
        messages = [{"role": "user", "content": prompt}]

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature
        }

        if system_prompt:
            body["system"] = system_prompt

        try:
            response = self.bedrock_runtime.invoke_model_with_response_stream(
                modelId=self.model_id,
                body=json.dumps(body)
            )

            stream = response.get('body')
            if stream:
                for event in stream:
                    chunk = event.get('chunk')
                    if chunk:
                        chunk_obj = json.loads(chunk.get('bytes').decode())
                        if chunk_obj['type'] == 'content_block_delta':
                            if chunk_obj['delta']['type'] == 'text_delta':
                                yield chunk_obj['delta']['text']

        except ClientError as e:
            raise Exception(f"Bedrock streaming error: {str(e)}")

    def list_foundation_models(self) -> List[Dict[str, Any]]:
        """List available foundation models."""
        try:
            response = self.bedrock.list_foundation_models()
            return response.get('modelSummaries', [])
        except ClientError as e:
            raise Exception(f"Failed to list models: {str(e)}")

    def get_model_info(self, model_id: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a specific model."""
        model = model_id or self.model_id

        try:
            response = self.bedrock.get_foundation_model(modelIdentifier=model)
            return response.get('modelDetails', {})
        except ClientError as e:
            raise Exception(f"Failed to get model info: {str(e)}")
