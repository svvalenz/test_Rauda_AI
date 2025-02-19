from utils import get_openai_client, read_tickets
import pandas as pd
import os
import json
from pydantic import BaseModel, Field, validator
from typing import List

class Ticket(BaseModel):
    ticket: str = Field(..., min_length=1)
    reply: str = Field(..., min_length=1)

    @validator('ticket', 'reply')
    def validate_fields(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

class EvaluationResponse(BaseModel):
    content_score: int = Field(..., ge=1, le=5)
    content_explanation: str = Field(..., min_length=10, max_length=200)
    format_score: int = Field(..., ge=1, le=5)
    format_explanation: str = Field(..., min_length=10, max_length=200)

    @validator('content_score', 'format_score')
    def validate_score(cls, v):
        if not 1 <= v <= 5:
            raise ValueError(f'Score must be between 1 and 5, got {v}')
        return v

class TicketEvaluation(BaseModel):
    ticket: str
    reply: str
    content_score: int = Field(..., ge=0, le=5)  # 0 for error cases
    content_explanation: str
    format_score: int = Field(..., ge=0, le=5)  # 0 for error cases
    format_explanation: str

class TicketEvaluator:
    def __init__(self, input_file):
        self.client = get_openai_client()
        df = read_tickets(input_file)
        # Validate all tickets at initialization
        self.tickets = [Ticket(ticket=row['ticket'], reply=row['reply']) 
                       for _, row in df.iterrows()]
        
    def evaluate_response(self, ticket: Ticket) -> TicketEvaluation:
        """Evaluates a customer service response"""
        prompt = f"""Evaluate the following customer service response:

Customer ticket: {ticket.ticket}
Response: {ticket.reply}

Please evaluate two aspects:
1. Content (relevance, correctness, completeness) - Rate from 1 to 5
2. Format (clarity, structure, grammar) - Rate from 1 to 5

Respond in JSON format with exactly these fields:
{{
    "content_score": <number from 1-5>,
    "content_explanation": "<explanation between 10 and 200 characters>",
    "format_score": <number from 1-5>,
    "format_explanation": "<explanation between 10 and 200 characters>"
}}

Explanations should be concise but informative."""

        try:
            response = self.client.chat.completions.create(
                model=os.getenv('MODEL_NAME'),
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            
            # Parse and validate response
            response_data = json.loads(response.choices[0].message.content)
            validated_response = EvaluationResponse(**response_data)
            
            # Create complete evaluation
            return TicketEvaluation(
                ticket=ticket.ticket,
                reply=ticket.reply,
                **validated_response.model_dump()
            )
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON response: {str(e)}")
        except Exception as e:
            return TicketEvaluation(
                ticket=ticket.ticket,
                reply=ticket.reply,
                content_score=0,
                content_explanation=f"Error: {str(e)}",
                format_score=0,
                format_explanation=f"Error: {str(e)}"
            )

    def process_all_tickets(self) -> pd.DataFrame:
        """Process all tickets and generate final CSV"""
        results = []
        
        for idx, ticket in enumerate(self.tickets):
            evaluation = self.evaluate_response(ticket)
            results.append(evaluation.model_dump())
            
            if evaluation.content_score == 0:  # Error case
                print(f"Error processing ticket {idx + 1}: {evaluation.content_explanation}")
        
        output_df = pd.DataFrame(results)
        output_df.to_csv('tickets_evaluated.csv', sep=';', index=False)
        return output_df 