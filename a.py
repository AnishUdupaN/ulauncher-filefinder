ExtensionResultItem(
    icon='images/icon.png',
    name=f"Search for '{query}'",
    description="Press Enter to search",
    on_enter=RunScriptAction(f"/usr/bin/find /home -name '*{query}*'", terminal=True)
)
