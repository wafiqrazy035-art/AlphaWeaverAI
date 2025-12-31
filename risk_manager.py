class riskmanager:
    def __init__(self, tp_percent=2.0, sl_percent=1.5):
        self.tp_percent = tp_percent
        self.sl_percent = sl_percent

    def calculate_targets(self, current_price, action):
        action_type = action.lower()
        
        if action_type == "buy":
            tp = current_price * (1 + self.tp_percent / 100)
            sl = current_price * (1 - self.sl_percent / 100)
            return round(tp), round(sl)
        elif action_type == "sell":
            tp = current_price * (1 - self.tp_percent / 100)
            sl = current_price * (1 + self.sl_percent / 100)
            return round(tp), round(sl)
        return None, None