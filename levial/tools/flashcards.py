import logging
import genanki
import random
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flashcards")

mcp = FastMCP("Flashcards")

@mcp.tool()
def create_deck(title: str, cards: List[Dict[str, str]], output_file: str = "deck.apkg") -> str:
    """
    Create an Anki deck from a list of cards.
    
    Args:
        title: Deck title.
        cards: List of dicts with 'question' and 'answer'.
        output_file: Output filename.
    """
    try:
        model_id = random.randrange(1 << 30, 1 << 31)
        deck_id = random.randrange(1 << 30, 1 << 31)
        
        model = genanki.Model(
            model_id,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ])
            
        deck = genanki.Deck(deck_id, title)
        
        for card in cards:
            note = genanki.Note(
                model=model,
                fields=[card['question'], card['answer']]
            )
            deck.add_note(note)
            
        genanki.Package(deck).write_to_file(output_file)
        return f"Deck '{title}' created successfully at {output_file}"
        
    except Exception as e:
        return f"Error creating deck: {str(e)}"

if __name__ == "__main__":
    mcp.run()
