XSOAR DLP Case Summarizer
Project Overview

This project focuses on generating executive case summaries for DLP incidents within XSOAR. The summary is generated automatically using fields collected throughout the playbook execution. A custom LLM, hosted on a GPU server, is used to generate the summary based on the incident data.

The summarization step is executed toward the end of the playbook. No manual input or button press is required. Once the playbook reaches the summarization stage, it constructs a prompt using selected fields and makes an API call to the backend.

The generated summary is saved into the incident context and is also displayed in the case layout for review.


How It Works

    Playbook Execution
    As the DLP playbook progresses, relevant fields (such as alert type, incident timeline, asset details, etc.) are captured and stored in the context.

    Summary Generation Step
    Toward the end of the playbook, an automation task sends an API call to the backend summarization server. This call includes the incident ID and any required context data.

    Backend Processing
    The backend handles prompt construction and model inference. It uses the incident data to generate a concise executive summary using the custom LLM hosted on a GPU server.

    Summary Return
    The generated summary is returned in the API response. It is then:

        Saved into the incident context.

        Displayed in the case layout under a dedicated field or tab.
