"""
Current Model Detection
System to track which model is currently active in Cursor
"""

# Current active model in Cursor (set by user)
CURRENT_CURSOR_MODEL = None  # Will be set by user or detected

def set_current_model(model_name: str):
    """Set the current active model in Cursor"""
    global CURRENT_CURSOR_MODEL
    CURRENT_CURSOR_MODEL = model_name
    print(f"✅ Ustawiono aktywny model: {model_name}")

def get_current_model() -> str:
    """Get the current active model"""
    return CURRENT_CURSOR_MODEL or "unknown"

def show_current_model():
    """Show current model"""
    model = get_current_model()
    if model == "unknown":
        print("\n⚠️ Model nie jest ustawiony.")
        print("💡 Użyj: set_current_model('nazwa-modelu')")
        print("   Dostępne: gpt-5, gpt-5-high, claude-sonnet-4.5, claude-codex, gemini-pro-2.5\n")
    else:
        print(f"\n✅ Aktualnie aktywny model w Cursor: {model}\n")
