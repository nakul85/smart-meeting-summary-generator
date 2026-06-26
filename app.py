import json
import os

import streamlit as st

from services.summarizer import MeetingSummarizer
from services.regenerate import SectionRegenerator
from services.validator import SummaryValidator


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Smart Meeting Summary Generator",
    layout="wide"
)


# ==========================================================
# Session State Initialization
# ==========================================================

DEFAULT_SESSION_STATE = {
    "summary": None,
    "transcript": ""
}

for key, value in DEFAULT_SESSION_STATE.items():
    st.session_state.setdefault(key, value)


# ==========================================================
# Helper Functions
# ==========================================================

def generate_summary(transcript: str) -> dict:
    """
    Generate and validate meeting summary.
    """

    summarizer = MeetingSummarizer()

    response = summarizer.summarize(transcript)

    summary = json.loads(response)

    summary = SummaryValidator.validate(
        summary,
        transcript
    )

    return summary


def regenerate_section(section: str):
    """
    Regenerate a specific summary section.
    """

    regenerator = SectionRegenerator()

    regenerated = regenerator.regenerate(
        st.session_state.transcript,
        st.session_state.summary,
        section
    )

    if section == "Agenda":

        st.session_state.summary["agenda"] = regenerated

    elif section == "Main Topics":

        st.session_state.summary["main_topics"] = [
            topic.strip("-• ").strip()
            for topic in regenerated.splitlines()
            if topic.strip()
        ]

    elif section == "Key Decisions":

        st.session_state.summary["key_decisions"] = [
            decision.strip("-• ").strip()
            for decision in regenerated.splitlines()
            if decision.strip()
        ]

    elif section == "Action Items":
     try:

        actions = json.loads(regenerated)

        if isinstance(actions, list):
            st.session_state.summary["action_items"] = actions
        else:
            raise ValueError("Expected a list of action items.")
     except json.JSONDecodeError:
        st.error(
        "The regenerated action items were not valid JSON."
        )
        return


def build_text_summary(summary: dict) -> str:
    """
    Create downloadable TXT summary.
    """

    output = []

    output.append("SMART MEETING SUMMARY")
    output.append("=" * 50)
    output.append("")

    output.append("AGENDA")
    output.append("-" * 20)
    output.append(summary.get("agenda", ""))
    output.append("")

    output.append("MAIN TOPICS")
    output.append("-" * 20)

    for topic in summary.get("main_topics", []):

        output.append(f"• {topic}")

    output.append("")

    output.append("KEY DECISIONS")
    output.append("-" * 20)

    for decision in summary.get("key_decisions", []):

        output.append(f"• {decision}")

    output.append("")

    output.append("ACTION ITEMS")
    output.append("-" * 20)

    for index, item in enumerate(
        summary.get("action_items", []),
        start=1
    ):

        output.append(f"Action Item {index}")
        output.append(
            f"Task      : {item.get('task', 'Not specified')}"
        )
        output.append(
            f"Owner     : {item.get('owner', 'Not specified')}"
        )
        output.append(
            f"Due Date  : {item.get('due_date', 'Not specified')}"
        )
        output.append("")


    return "\n".join(output)


def render_regenerate_button(section: str, key: str):
    """
    Render regenerate button below each section.
    """

    if st.button(
        "Regenerate",
        key=key,
        use_container_width=True
    ):

        try:

            with st.spinner(f"Regenerating {section}..."):

                regenerate_section(section)

            st.success(f"{section} regenerated successfully.")

            st.rerun()

        except Exception as error:

            st.error(str(error))


# ==========================================================
# Header
# ==========================================================

st.title("Smart Meeting Summary Generator")

st.write(
    "Generate structured meeting summaries using Gemini AI."
)

st.divider()


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.header("Meeting Input")

input_option = st.sidebar.radio(
    "Choose Input",
    (
        "Paste Transcript",
        "Load Sample Meeting"
    )
)


# ==========================================================
# Transcript Input
# ==========================================================

if input_option == "Paste Transcript":

    transcript = st.text_area(
        "Meeting Transcript",
        value=st.session_state.transcript,
        height=350,
        placeholder="Paste your meeting transcript here..."
    )

else:

    sample_folder = "sample_data"

    sample_files = sorted(
        file
        for file in os.listdir(sample_folder)
        if file.endswith(".txt")
    )

    selected_sample = st.selectbox(
        "Sample Meeting",
        sample_files
    )

    with open(
        os.path.join(sample_folder, selected_sample),
        "r",
        encoding="utf-8"
    ) as file:

        transcript = st.text_area(
            "Meeting Transcript",
            value=file.read(),
            height=350
        )

# ==========================================================
# Generate Summary
# ==========================================================

if st.button(
    "Generate Summary",
    use_container_width=True
):

    if not transcript.strip():

        st.warning(
            "Please provide a meeting transcript."
        )

        st.stop()

    try:

        with st.spinner(
            "Generating meeting summary..."
        ):

            summary = generate_summary(
                transcript
            )

        st.session_state.summary = summary
        st.session_state.transcript = transcript

        st.success(
            "Meeting summary generated successfully."
        )

        st.rerun()

    except json.JSONDecodeError:

        st.error(
            "The AI returned an invalid response. Please try again."
        )

        st.stop()

    except Exception as error:

        st.error(str(error))

        st.stop()


# ==========================================================
# Stop Until Summary Exists
# ==========================================================

if st.session_state.summary is None:
    st.stop()

summary = st.session_state.summary

st.divider()


# ==========================================================
# Reusable Section Header
# ==========================================================

def section_title(title: str):

    st.subheader(title)


# ==========================================================
# Agenda
# ==========================================================

section_title("Agenda")

st.write(
    summary.get(
        "agenda",
        "No agenda generated."
    )
)

render_regenerate_button(
    "Agenda",
    "regen_agenda"
)

st.divider()


# ==========================================================
# Main Topics
# ==========================================================

section_title("Main Topics")

topics = summary.get(
    "main_topics",
    []
)

if topics:

    for topic in topics:

        st.markdown(f"- {topic}")

else:

    st.info(
        "No main topics identified."
    )

render_regenerate_button(
    "Main Topics",
    "regen_topics"
)

st.divider()

# ==========================================================
# Key Decisions
# ==========================================================

section_title("Key Decisions")

decisions = summary.get(
    "key_decisions",
    []
)

if decisions:

    for decision in decisions:

        st.markdown(f"- {decision}")

else:

    st.info(
        "No key decisions identified."
    )

render_regenerate_button(
    "Key Decisions",
    "regen_decisions"
)

st.divider()


# ==========================================================
# Action Items
# ==========================================================

section_title("Action Items")

action_items = summary.get(
    "action_items",
    []
)

if action_items:

    for index, item in enumerate(
        action_items,
        start=1
    ):

        with st.expander(
            f"Action Item {index}",
            expanded=True
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown("**Task**")

                st.write(
                    item.get(
                        "task",
                        "Not specified"
                    )
                )

            with col2:

                st.markdown("**Owner**")

                st.write(
                    item.get(
                        "owner",
                        "Not specified"
                    )
                )

            with col3:

                st.markdown("**Due Date**")

                st.write(
                    item.get(
                        "due_date",
                        "Not specified"
                    )
                )

else:

    st.info(
        "No action items identified."
    )

render_regenerate_button(
    "Action Items",
    "regen_actions"
)

st.divider()


# ==========================================================
# Download Summary
# ==========================================================

st.subheader("Download Summary")

json_summary = json.dumps(
    summary,
    indent=4,
    ensure_ascii=False
)

txt_summary = build_text_summary(
    summary
)

download_col1, download_col2 = st.columns(2)

with download_col1:

    st.download_button(
        label="Download as TXT",
        data=txt_summary,
        file_name="meeting_summary.txt",
        mime="text/plain",
        use_container_width=True
    )

with download_col2:

    st.download_button(
        label="Download as JSON",
        data=json_summary,
        file_name="meeting_summary.json",
        mime="application/json",
        use_container_width=True
    )


# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(
    "Smart Meeting Summary Generator • Powered by Gemini AI"
)