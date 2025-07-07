import subprocess
import os
import multi
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent, PreferencesUpdateEvent,ExtensionCustomAction
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
        self.subscribe(ExtensionCustomAction, CustomActionEventListener())


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.preferences.update(event.preferences)


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        extension.preferences[event.id] = event.new_value


class KeywordQueryEventListener(EventListener):
    """
    def on_event(self, event, extension):
        items = []
        stringinput = event.get_argument() or ""
        args = stringinput.strip().split()
        filename=args[0]
        if len(args)==1:
            search_path =os.path.expanduser("~")  #change if the user gives additional path
        else:
            search_path=args[1]

        # Run the fd command
        result = subprocess.run(['fd', filename, search_path], capture_output=True, text=True)
        output = result.stdout
        lines = [line for line in output.split('\n') if line.strip()]
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
        """
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        if not query:
            return RenderResultListAction([])

        # Return one item prompting user to press enter to search
        item = ExtensionResultItem(
            icon='images/icon.png',
            name=f"Press Enter to search for '{query}'",
            description="Run the actual search",
            on_enter=ExtensionCustomAction({"query": query})
        )
        return RenderResultListAction([item])

class CustomActionEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        stringinput = event.get_argument() or ""
        args = stringinput.strip().split(' in ')
        filename=args[0]
        if len(args)==1:
            search_path =os.path.expanduser("~")  #change if the user gives additional path
            result = subprocess.run(['fd', filename, search_path], capture_output=True, text=True)
            output = result.stdout
            lines = [line for line in output.split('\n') if line.strip()]
        else:
            search_path=args[1]
            lines=multi.command(filename,search_path)
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
