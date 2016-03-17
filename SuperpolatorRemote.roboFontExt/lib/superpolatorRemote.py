from mojo.UI import *
import vanilla
from AppKit import NSDistributedNotificationCenter
from mojo.events import addObserver, removeObserver

# because sometimes superpolator is too far away

class SuperpolatorRemote(object):
    version = "1.0"
    def __init__(self):
        self.w = vanilla.Window((260, 80), "Superpolator Remote is off")
        self.w.background = vanilla.ImageView((0,0,80,-0))
        self.w.background.setImage(imagePath="./icon_128x128.png")
        self.w.switchButton = vanilla.Button((90, 5, -5, 20), "Start", callback=self.switchCallback)
        self.w.copyButton = vanilla.Button((90, 30, -5, 20), "Send spacecenter text", callback=self.callbackSetText)
        self.w.caption = vanilla.TextBox((92, 60, -5, -5), "Version %s"%self.version, sizeStyle="mini")
        self.running = False
        self.w.bind("close", self.windowClose)
        self.w.open()
    
    def windowClose(self, sender):
        self.stopRemoting()
    
    def switchCallback(self, sender):
        self.running = not self.running
        if not self.running:
            self.w.switchButton.setTitle("Start")
            self.w.setTitle("Superpolator Remote is off")
            self.w.caption.set("")
            self.stopRemoting()
        else:
            self.w.switchButton.setTitle("Stop")
            self.w.setTitle("Superpolator Remote is on")
            self.w.caption.set("Superpolator updates on save!")
            self.startRemoting()
    
    def stopRemoting(self):
        # remove the observer
        removeObserver(self, "fontDidSave")
    
    def startRemoting(self):
        # add the observer
        addObserver(self, "callbackSaveUFO", "fontDidSave")
    
    def callbackSaveUFO(self, data):
        options = {'path': data['path']}
        dnc = NSDistributedNotificationCenter.defaultCenter()
        dnc.postNotificationName_object_userInfo_deliverImmediately_("com.letterror.superpolator.updateUFO", None, options, True)

    def callbackSetText(self, data):
        space = CurrentSpaceCenter()
        if space is None:
            return
        currentName = None
        g = CurrentGlyph()
        if g is not None:
            currentName = g.name
        text = space.get()
        newText = []
        for glyph in text:
            if glyph == "/?":
                if currentName is not None:
                    newText.append(currentName)
            else:
                newText.append(glyph)
        newText = "/"+"/".join(newText)
        direction = space.getLeftToRight()
        options = {'text': newText, 'direction':direction}
        dnc = NSDistributedNotificationCenter.defaultCenter()
        dnc.postNotificationName_object_userInfo_deliverImmediately_("com.letterror.superpolator.setText", None, options, True)

if __name__ == "__main__":
    sr = SuperpolatorRemote()