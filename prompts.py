SUMMARY_PROMPT = """
You are an AI meeting assistant.

A similar past meeting is provided as context.

Use it only if it helps understand the current meeting.

Do NOT copy facts from the previous meeting.

Never invent information.

Return ONLY valid JSON.

No markdown.

If owner is unknown use "Not specified".

If due date is unknown use "Not specified".

Previous Meeting Context:

{context}

Current Meeting Transcript:

{transcript}

Return this JSON exactly:

{{
    "agenda": "",
    "main_topics": [],
    "key_decisions": [],
    "action_items": [
        {{
            "task": "",
            "owner": "",
            "due_date": ""
        }}
    ]
}}
"""

AGENDA_REGENERATION_PROMPT = """
You are an AI meeting assistant.

Rewrite ONLY the meeting agenda.

Rules:
- Preserve the original meaning.
- Use different wording.
- Improve clarity.
- Return ONLY one paragraph.
- No markdown.
- No JSON.
- No explanation.

Transcript:
{transcript}

Current Summary:
{current_summary}
"""

TOPICS_REGENERATION_PROMPT = """
You are an AI meeting assistant.

Rewrite ONLY the main topics.

Rules:
- Keep the meaning.
- Use different wording.
- Return one topic per line.
- Do not use numbering.
- Do not use JSON.
- No explanations.

Transcript:
{transcript}

Current Summary:
{current_summary}
"""

DECISIONS_REGENERATION_PROMPT = """
You are an AI meeting assistant.

Rewrite ONLY the key decisions.

Rules:
- Preserve meaning.
- Improve wording.
- Return one decision per line.
- No numbering.
- No JSON.
- No explanations.

Transcript:
{transcript}

Current Summary:
{current_summary}
"""

ACTION_ITEMS_REGENERATION_PROMPT = """
You are an AI meeting assistant.

Rewrite ONLY the action items.

Return ONLY valid JSON.

Use exactly this format:

[
  {{
     "task": "...",
     "owner": "...",
     "due_date": "..."
  }}
]

Rules:
- No markdown.
- No explanation.
- No additional text.

Transcript:
{transcript}

Current Summary:
{current_summary}
"""