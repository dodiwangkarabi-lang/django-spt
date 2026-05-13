from . import actions

class WorkFlowService:
    def __init__(self, model):
        self.model = model
    
    def ajukan(self, user):
        return actions.ajukan(self.model, user)
    
    def setujui(self):
        return actions.setujui(self.model)
    
    def tolak(self, catatan=""):
        return actions.tolak(self.model, catatan)
    
    def revisi(self, catatan=""):
        return actions.revisi(self.model, catatan)
    
    def setujui_permohonan(self):
        return actions.setujui_permohonan(self.model)