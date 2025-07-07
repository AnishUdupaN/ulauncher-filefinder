import subprocess
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
class ClipboardHistoryExtension(Extension):
    def __init__(self):
        super(ClipboardHistoryExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.preferences.update(event.preferences)


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        extension.preferences[event.id] = event.new_value


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        query = event.get_argument() or ""

        # Set the filename and path
        filename = query
        search_path =os.path.expanduser("~")  #change if the user gives additional path

        # Run the fd command
        result = subprocess.run(['fd', filename, search_path], capture_output=True, text=True)
        output = result.stdout
        lines=output.split('\n')
        for item in range(len(lines)-1):
            print(f"Item {item+1} : {lines[item]}")


        for i in range(len(lines)):
            items.append(ExtensionResultItem(
                icon=os.path.join(os.getcwd(),'images/icon.png'),
                name=lines[i],
                description="Click to Open",
                on_enter=RunScriptAction(f'xdg-open "{lines[i]}"', [])
            ))
        num_entries = int(extension.preferences.get('num_entries', 10))
        return RenderResultListAction(items[:num_entries])
        

if __name__ == '__main__':
    ClipboardHistoryExtension().run()
