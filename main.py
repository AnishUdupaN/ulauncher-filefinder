import subprocess
import os
import multi
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
        stringinput = event.get_argument() or ""
        args = stringinput.strip().split(' in ')
        filename=args[0]
        if len(args)==1:
            search_path =os.path.expanduser("~")  #change if the user gives additional path
            result = subprocess.run(['fd', filename, search_path,"--follow"], capture_output=True, text=True)
            output = result.stdout
            lines = [line for line in output.split('\n') if line.strip()]
            lines=multi.sort(lines,filename)
        else:
            search_path=args[1]
            lines=multi.command(filename,search_path)
            lines=multi.sort(lines,search_path+filename)
        for i in range(len(lines)):
            parts = lines[i].rsplit("/", 1)  # Split from the right only once
            items.append(ExtensionResultItem(
                icon=os.path.join(os.getcwd(),'images/icon.png'),
                name=parts[0],
                description=f"In {parts[1]}",
                on_enter=RunScriptAction(f'xdg-open "{lines[i]}"', [])
            ))
        num_entries = int(extension.preferences.get('num_entries', 10))
        return RenderResultListAction(items[:num_entries])

if __name__ == '__main__':
    ClipboardHistoryExtension().run()
