"""
JARVIS Notion Module
Integration with Notion task databases
"""

from notion_client import Client
from config import NOTION_TOKEN, NOTION_DATABASE_ID

class NotionManager:
    """Manage Notion tasks and pages."""
    
    def __init__(self):
        self.notion = Client(auth=NOTION_TOKEN) if NOTION_TOKEN else None
        self.database_id = NOTION_DATABASE_ID

    def add_task(self, title, status="To Do", category=None):
        """Add a task to the Notion database."""
        if not self.notion or not self.database_id:
            return "⚠️ Notion not configured."

        new_page = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Status": {"select": {"name": status}},
        }
        
        if category:
            new_page["Category"] = {"select": {"name": category}}

        try:
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=new_page
            )
            return f"✅ Task added to Notion: {title}"
        except Exception as e:
            return f"❌ Notion Error: {e}"

# Singleton instance
_notion_instance = None

def get_notion_manager():
    """Get the singleton notion manager instance."""
    global _notion_instance
    if _notion_instance is None:
        _notion_instance = NotionManager()
    return _notion_instance
