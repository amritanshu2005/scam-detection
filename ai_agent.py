"""
Autonomous AI Agent Module
Maintains believable human persona and engages scammers to extract intelligence
"""

import os
import json
from typing import List, Dict, Any, Optional
import re

# Try to use OpenAI if available, otherwise use a simple rule-based approach
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AutonomousAgent:
    """Autonomous AI agent that engages scammers"""
    
    def __init__(self):
        self.openai_client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    # Try new OpenAI client format (v1.x)
                    from openai import OpenAI
                    self.openai_client = OpenAI(api_key=api_key)
                    self.use_new_client = True
                except (ImportError, AttributeError):
                    # Fallback to old format
                    openai.api_key = api_key
                    self.openai_client = openai
                    self.use_new_client = False
        
        # Persona traits - maintain consistent believable human behavior
        self.persona = {
            "name": "Alex",
            "age_range": "30-40",
            "personality": "curious but cautious, asks questions, seems interested but not too eager",
            "communication_style": "casual, uses emojis occasionally, may have typos",
            "engagement_strategy": "gradual - starts skeptical, becomes more interested over time"
        }
        
        # Conversation state
        self.conversation_stages = {
            "initial": "skeptical, asking questions",
            "interested": "showing interest, asking for more details",
            "engaged": "actively participating, requesting specific information",
            "extracting": "asking for account details, UPI, links"
        }
    
    def generate_response(
        self,
        incoming_message: str,
        conversation_history: List[Dict[str, Any]],
        extracted_intelligence: Dict[str, Any]
    ) -> str:
        """
        Generate agent response to scammer message
        
        Args:
            incoming_message: Latest message from scammer
            conversation_history: Full conversation history
            extracted_intelligence: Already extracted intelligence
            
        Returns:
            Agent's response message
        """
        # Determine conversation stage
        stage = self._determine_stage(conversation_history, extracted_intelligence)
        
        # Use OpenAI if available, otherwise use rule-based
        if self.openai_client and os.getenv("OPENAI_API_KEY"):
            return self._generate_llm_response(incoming_message, conversation_history, stage)
        else:
            return self._generate_rule_based_response(incoming_message, conversation_history, stage, extracted_intelligence)
    
    def _determine_stage(
        self,
        conversation_history: List[Dict[str, Any]],
        extracted_intelligence: Dict[str, Any]
    ) -> str:
        """Determine current conversation stage with intelligence awareness"""
        turn_count = len([m for m in conversation_history if m.get("role") == "agent"])
        
        # Check what intelligence we've already extracted
        has_bank = len(extracted_intelligence.get("bank_accounts", [])) > 0
        has_upi = len(extracted_intelligence.get("upi_ids", [])) > 0
        has_url = len(extracted_intelligence.get("phishing_urls", [])) > 0
        
        # Adjust stage based on what we still need
        if turn_count == 0:
            return "initial"
        elif turn_count <= 2:
            return "interested"
        elif turn_count <= 5:
            # If we're missing key intelligence, stay in engaged stage
            if not (has_bank and has_upi and has_url):
                return "engaged"
            return "extracting"
        else:
            return "extracting"
    
    def _generate_llm_response(
        self,
        incoming_message: str,
        conversation_history: List[Dict[str, Any]],
        stage: str
    ) -> str:
        """Generate response using OpenAI API"""
        try:
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": f"""You are {self.persona['name']}, a believable human engaging with a potential scammer.
Your goal is to extract intelligence (bank accounts, UPI IDs, phishing URLs) without revealing you're detecting a scam.

Persona: {self.persona['personality']}
Communication style: {self.persona['communication_style']}
Current stage: {stage}

Guidelines:
- Act naturally and believably
- Don't reveal you know it's a scam
- Gradually show interest and ask for details
- Request bank account numbers, UPI IDs, and links when appropriate
- Keep responses concise (1-3 sentences)
- Use casual, human-like language"""
                }
            ]
            
            # Add conversation history
            for msg in conversation_history[-10:]:  # Last 10 messages for context
                role = "user" if msg.get("role") == "scammer" else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.get("content", "")
                })
            
            # Generate response
            if hasattr(self, 'use_new_client') and self.use_new_client:
                # New OpenAI client format (v1.x)
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=150
                )
                return response.choices[0].message.content.strip()
            else:
                # Old OpenAI client format
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=150
                )
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback to rule-based if LLM fails
            return self._generate_rule_based_response(incoming_message, conversation_history, stage, {})
    
    def _generate_rule_based_response(
        self,
        incoming_message: str,
        conversation_history: List[Dict[str, Any]],
        stage: str,
        extracted_intelligence: Dict[str, Any]
    ) -> str:
        """Generate response using rule-based approach"""
        message_lower = incoming_message.lower()
        turn_count = len([m for m in conversation_history if m.get("role") == "agent"])
        
        # Stage-based responses
        if stage == "initial":
            responses = [
                "Hmm, this seems interesting. Can you tell me more about it?",
                "I'm not sure I understand. What exactly do you need from me?",
                "This is the first I'm hearing about this. Can you provide more details?",
                "I want to make sure this is legitimate. Can you explain what this is about?",
            ]
        
        elif stage == "interested":
            responses = [
                "Okay, I'm listening. How does this work exactly?",
                "That sounds interesting. What information do you need?",
                "I see. What's the next step?",
                "Alright, I'm interested. What should I do?",
            ]
        
        elif stage == "engaged":
            # Start asking for specific details
            if "account" in message_lower or "bank" in message_lower:
                responses = [
                    "Sure, I can help. What account details do you need?",
                    "Okay, I'll provide the information. What exactly do you need?",
                    "I understand. Can you tell me what account number or details you need?",
                ]
            elif "upi" in message_lower or "payment" in message_lower:
                responses = [
                    "I can make the payment. What's your UPI ID or account number?",
                    "Sure, I'll transfer. Can you share your payment details?",
                    "Okay, where should I send the payment? What's your UPI or bank account?",
                ]
            elif "link" in message_lower or "url" in message_lower or "http" in message_lower:
                responses = [
                    "I'll check it out. Can you send me the link?",
                    "Sure, I can visit the website. What's the URL?",
                    "Okay, I'll open it. Can you share the link again?",
                ]
            else:
                responses = [
                    "I understand. What specific details do you need from me?",
                    "Sure, I can help with that. What information should I provide?",
                    "Okay, I'm ready. What do you need?",
                ]
        
        else:  # extracting stage
            # Actively request intelligence
            if not extracted_intelligence.get("bank_accounts"):
                responses = [
                    "Before I proceed, can you share your bank account number so I can verify?",
                    "I need your account details to complete this. What's your account number?",
                    "For verification, can you provide your bank account number?",
                ]
            elif not extracted_intelligence.get("upi_ids"):
                responses = [
                    "What's your UPI ID? I can send the payment there.",
                    "Can you share your UPI ID for the transfer?",
                    "I'll need your UPI ID to proceed. What is it?",
                ]
            elif not extracted_intelligence.get("phishing_urls"):
                responses = [
                    "Can you send me the link again? I want to make sure I have the right one.",
                    "What's the website URL? I'll visit it now.",
                    "I need the link. Can you share it?",
                ]
            else:
                responses = [
                    "Got it. I'll proceed with this.",
                    "Understood. I'm working on it.",
                    "Okay, I'll take care of it.",
                ]
        
        # Select response based on turn count for variety
        selected = responses[turn_count % len(responses)]
        
        # Context-aware response adjustments
        # Reference previous messages for better continuity
        if len(conversation_history) > 1:
            last_scammer_msg = None
            for msg in reversed(conversation_history):
                if msg.get("role") == "scammer":
                    last_scammer_msg = msg.get("content", "").lower()
                    break
            
            # If scammer mentioned specific details, acknowledge them
            if last_scammer_msg:
                if "account" in last_scammer_msg and "account" not in selected.lower():
                    selected = selected.replace("details", "account details")
                if "upi" in last_scammer_msg and "upi" not in selected.lower():
                    selected = selected.replace("payment", "UPI payment")
        
        # Add occasional casual elements for naturalness
        if turn_count % 3 == 0 and turn_count > 0:
            selected = selected.replace(".", " 😊")
        
        # Ensure response is not too short or too long
        if len(selected) < 10:
            selected = selected + " Please tell me more."
        if len(selected) > 200:
            selected = selected[:197] + "..."
        
        return selected

