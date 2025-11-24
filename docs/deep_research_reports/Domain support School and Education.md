Research Report: Domain Support - School & Education for Levial
Date: November 24, 2025 Topic: Architectural patterns for School & Education Support in a local-first AI agent.

1. Executive Summary
   Calendar Integration: Use the Google Calendar API directly via a local Python script (using google-auth-oauthlib for "Desktop App" flow). While MCP servers exist, a custom "Calendar Tool" using the official library is more robust for specific needs like "Find next exam."
   Intelligent Scheduling: Implement a Backward Planning Algorithm. Start from the Exam Date, subtract study hours required, and fill backwards into available slots. Use networkx to model dependencies (Chapter 1 before Chapter 2).
   Study RAG:
   Textbooks (PDF): Use LlamaParse or Unstructured for high-quality extraction (preserving headers/tables).
   Handwritten Notes: Use TrOCR (Transformer OCR) or Azure Computer Vision (if cloud is allowed) for best accuracy. Tesseract is often too weak for handwriting.
   Flashcards: Use genanki to generate .apkg files locally. The LLM should output JSON { "front": "...", "back": "..." }, which genanki compiles.
   Web Search: Filter for academic quality by using site:.edu operators and looking for PDF links. Use semanticscholar API if possible for true academic paper search.
2. Foundations & Definitions
   Backward Planning: A scheduling method that starts at the deadline and works backwards to find the start date.
   Spaced Repetition (SRS): The learning technique used by Anki.
   genanki: A Python library to generate Anki decks programmatically.
   OAuth 2.0: The protocol used to securely log in to Google Calendar without giving Levial your password.
3. Conceptual Map / Framework
   The "Academic Manager" Architecture:

Calendar Agent:
Tool: list_upcoming_exams(), add_study_session(start, end).
Source: Google Calendar API.
Scheduler Engine:
Input: Exam Date, "10 hours of study needed", "Flying Lesson on Saturday".
Logic: Backward Planning + Conflict Resolution.
Output: A proposed schedule to write back to Calendar.
Study Buddy (RAG):
Ingest: PDF/Images -> OCR -> Vector Store.
Action: "Quiz me on Chapter 3".
Flashcard Generator:
Input: Summarized notes.
Action: LLM generates Q&A pairs -> genanki creates Deck -> User imports to Anki. 4. Current State of the Field
Study Apps: Quizlet and Chegg dominate but are walled gardens.
Local Tools: AnkiConnect allows local apps to push cards to Anki, but genanki is safer as it generates a file to import.
Scheduling: Most students use manual calendars or Notion templates. AI auto-schedulers (like Motion) exist but are expensive SaaS. 5. Approaches, Methods, and Tools
Calendar Integration
Official Google API: Best reliability. Requires a credentials.json file.
MCP Server: Good if one exists, but custom Python code gives more control over "Exam" specific logic.
RAG for Notes
Handwriting is Hard: Tesseract will fail on messy notes.
Solution: Use a multimodal LLM (like GPT-4o or Llama 3.2 Vision) to "transcribe" the notes image before embedding the text. This is often better than pure OCR. 6. Risks, Limitations, and Failure Modes
Calendar Sync: Deleting the wrong event. Mitigation: Levial should only delete events it created (tag them).
OCR Errors: "5 mg" becomes "500 mg". Mitigation: Always show the original image source alongside the answer.
Over-scheduling: The agent books 8 hours of study in a row. Mitigation: Hard rules (max 2h blocks, 15m breaks). 7. Actionable Recommendations for Levial
Recommended Stack
Calendar: google-api-python-client.
Scheduling: Custom Python logic (no heavy library needed for simple backward planning).
Flashcards: genanki.
Notes: LlamaParse for PDFs. Llama 3.2 Vision (via Ollama) for transcribing handwritten notes.
Implementation Steps
Auth Setup: Create a Google Cloud Project, enable Calendar API, download credentials.json.
Build mcp-server-calendar:
Tool: get_events(start, end).
Tool: create_event(summary, start, end).
Build StudyScheduler:
Algorithm: exam_date - study_hours = start_time. Check for conflicts. If conflict, move earlier.
Build FlashcardTool:
Prompt: "Extract 5 key concepts from this text as Front/Back flashcards in JSON."
Code: Parse JSON -> genanki.Note -> genanki.Deck -> output.apkg. 8. Assumptions & Uncertainties
Assumption: The user is okay with creating a Google Cloud Project (it's free but has a setup process).
Uncertainty: The quality of local Vision models (Llama 3.2) for handwriting transcription needs testing.
