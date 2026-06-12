from datetime import datetime
from pathlib import Path
from typing import Any

from google import genai
from loguru import logger

from config import GOOGLE_API_KEY


def summarize_html_files() -> None:
    """
    Uploads a list of HTML files to the Gemini Files API using an explicit API key,
    generates a consolidated Markdown summary, and cleans up the remote files.
    """
    # Initialize the GenAI Client by explicitly passing your pre-existing API key variable
    client: genai.Client = genai.Client(api_key=GOOGLE_API_KEY)

    print("Uploading HTML files to Gemini...")
    target_dir: Path = Path(Path.cwd())
    uploaded_file_refs: list[Any] = []

    try:
        for html_file in target_dir.glob("*.html"):
            ref: Any = client.files.upload(file=html_file)
            uploaded_file_refs.append(ref)
            logger.info(f"Uploaded {html_file.name} -> {ref.name}")

        # 2. Craft the prompt for combined summary
        prompt: str = """
        You are an expert technical writer. I have uploaded multiple HTML files. 
        Please extract the core content from each file, ignoring boilerplate HTML structures, scripts, or styling.
        
        Provide a comprehensive, unified summary of all these documents combined into one cohesive report. 
        If there are links in the html documents, follow them to add substance to the summary.
        The order of the informations should be determined by the number of time it is mentioned across the documents.
        If a piece of information is mentioned in multiple documents, it should be prioritized higher in the summary.
        Obvious adds should be avoided, but if they are necessary to understand the content, they can be included.
        Please include the links in the summary if they are relevant to the content. If a link is mentioned multiple times, it should be prioritized higher in the summary.
        Format your output using clean Markdown, complete with descriptive headings, bullet points, and key takeaways.
        """

        logger.info("Generating combined summary with Gemini...")

        # Unpack the file references into the contents list alongside the textual prompt
        response: Any = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt, *uploaded_file_refs])

        # 3. Save the output to a Markdown document using pathlib
        output_file: Path = Path(f"combined_summary{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.md")
        if response.text:
            output_file.write_text(response.text, encoding="utf-8")
            logger.info(f"\nSuccess! Combined summary saved to: {output_file}")
        else:
            logger.warning("\nWarning: Received an empty response from the model.")

    finally:
        # 4. Cleanup files from the server
        logger.info("\nCleaning up files from Gemini server...")
        ref_to_delete: Any
        for ref_to_delete in uploaded_file_refs:
            try:
                client.files.delete(name=ref_to_delete.name)
                logger.info(f"Deleted {ref_to_delete.name}")
            except Exception as e:
                logger.error(f"Failed to delete {ref_to_delete.name}: {e}")
