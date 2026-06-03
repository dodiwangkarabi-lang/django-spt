class SPTStateMachine:
    DRAFT = "draft"
    DIPROSES = "diproses"
    REVISI = "revisi"
    SELESAI = "selesai"

    TRANSITIONS = {
        DRAFT: [DIPROSES],
        DIPROSES: [REVISI, SELESAI],
        REVISI: [DIPROSES],
        SELESAI: []
    }

    @classmethod
    def can_transition(cls, current, target):
        """
        

        Args:
            current (_type_): _description_
            target (_type_): _description_

        Returns:
            _type_: _description_
            
        Example:
            >>> SPTStateMachine.can_transition(current=SPTStateMachine.DRAFT, target=SPTStateMachine.DIPROSES)
            
        Contoh Data:
            >>> current = SPTStateMachine.DRAFT
            >>> target = SPTStateMachine.DIPROSES
            >>> SPTStateMachine.can_transition(current=current, target=target)
        """
        return target in cls.TRANSITIONS.get(current, [])