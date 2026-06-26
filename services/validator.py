class SummaryValidator:

    @staticmethod
    def validate(summary: dict, transcript: str):

        summary.setdefault("agenda", "")
        summary.setdefault("main_topics", [])
        summary.setdefault("key_decisions", [])
        summary.setdefault("action_items", [])

        if not isinstance(summary["main_topics"], list):
            summary["main_topics"] = []

        if not isinstance(summary["key_decisions"], list):
            summary["key_decisions"] = []

        if not isinstance(summary["action_items"], list):
            summary["action_items"] = []

        transcript_lower = transcript.lower()

        validated_actions = []

        for item in summary["action_items"]:

            task = item.get("task", "Not specified")
            owner = item.get("owner", "Not specified")
            due_date = item.get("due_date", "Not specified")

            if (
                owner != "Not specified"
                and owner.lower() not in transcript_lower
            ):
                owner = "Not specified"

            validated_actions.append(
                {
                    "task": task,
                    "owner": owner,
                    "due_date": due_date
                }
            )

        summary["action_items"] = validated_actions

        return summary