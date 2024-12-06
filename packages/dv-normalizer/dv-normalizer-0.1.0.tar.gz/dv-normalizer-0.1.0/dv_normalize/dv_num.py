def int_to_dv(num, thousands=False, is_spoken=False, is_year=False):
    # Dictionary mapping numbers to their Dhivehi representations
    # Format: [written_form, spoken_form]
    d = {
        0: ["ސުމެއް", "ސުމެއް"],
        1: ["އެއް", "އެކެއް"],
        2: ["ދެ", "ދޭއް"],
        3: ["ތިން", "ތިނެއް"],
        4: ["ހަތަރު", "ހަތަރެއް"],
        5: ["ފަސް", "ފަހެއް"],
        6: ["ހަ", "ހައެއް"],
        7: ["ހަތް", "ހަތެއް"],
        8: ["އަށް", "އަށެއް"],
        9: ["ނުވަ", "ނުވައެއް"],
        10: ["ދިހަ", "ދިހައެއް"],
        11: ["އެގާރަ", "އެގާރަ"],
        12: ["ބާރަ", "ބާރަ"],
        13: ["ތޭރަ", "ތޭރަ"],
        14: ["ސާދަ", "ސާދަ"],
        15: ["ފަނަރަ", "ފަނަރަ"],
        16: ["ސޯޅަ", "ސޯޅަ"],
        17: ["ސަތާރަ", "ސަތާރަ"],
        18: ["އަށާރަ", "އަށާރަ"],
        19: ["ނަވާރަ", "ނަވާރަ"],
        20: ["ވިހި", "ވިހި"],
        30: ["ތިރީސް", "ތިރީސް"],
        40: ["ސާޅީސް", "ސާޅީސް"],
        50: ["ފަންސާސް", "ފަންސާސް"],
        60: ["ފަސްދޮޅަސް", "ފަސްދޮޅަސް"],
        70: ["ހައްދިހަ", "ހައްދިހަ"],
        80: ["އައްޑިހަ", "އައްޑިހަ"],
        90: ["ނުވަދިހަ", "ނުވަދިހަ"]
    }

    # Map for numbers before ހާސް
    haas_map = {
        "އެކެއް": "އެއް",
        "ދޭއް": "ދެ",
        "ތިނެއް": "ތިން",
        "ހަތަރެއް": "ހަތަރު",
        "ފަހެއް": "ފަސް",
        "ހައެއް": "ހަ",
        "ހަތެއް": "ހަތް",
        "އަށެއް": "އަށް",
        "ނުވައެއް": "ނުވަ"
    }

    # Constants for large numbers
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    if num < 0:
        return "Invalid number"

    if num == 0:
        return "ސުމެއް"

    # Special mapping for numbers with ވީސް (20-29)
    special_vis = {
        20: "ވީސް",
        21: "އެކާވީސް",
        22: "ބާވީސް",
        23: "ތޭވީސް",
        24: "ސައްވީސް",
        25: "ފަންސަވީސް",
        26: "ސައްބީސް",
        27: "ހަތާވީސް",
        28: "އަށާވީސް",
        29: "ނަވާވީސް"
    }

    # Special handling for years (1000-9999)
    if is_year and 1000 <= num <= 9999:
        millennium = num // 1000
        last_two_digits = num % 100
        
        millennium_text = f"{d[millennium][0]}ހާސް"
        
        if last_two_digits == 0:
            return millennium_text
        
        # Use special mapping for 20-29
        if last_two_digits in special_vis:
            return f"{millennium_text} {special_vis[last_two_digits]}"
        
        # Handle other numbers...
        if last_two_digits in d:
            return f"{millennium_text} {d[last_two_digits][0]}"
        else:
            year_tens = (last_two_digits // 10) * 10
            year_ones = last_two_digits % 10
            
            if year_ones == 0:
                return f"{millennium_text} {d[year_tens][0]}"
            else:
                return f"{millennium_text} {d[year_tens][0]} {d[year_ones][0]}"

    # Regular number handling
    if num in d:
        return d[num][1 if is_spoken else 0]

    # Add check for special_vis numbers (20-29)
    if num in special_vis:
        return special_vis[num]

    if num < 100:
        if is_spoken:
            thousands = True
        
        base = (num // 10) * 10
        remainder = num % 10
        
        if remainder == 0:
            return d[base][1 if is_spoken else 0]
        
        return f"{d[base][1 if is_spoken else 0]} {d[remainder][0 if thousands else 1]}"

    if num < k:
        hundreds = num // 100
        remainder = num % 100
        
        if hundreds == 2:
            hundreds_text = f"{d[hundreds][0]}ސައްތަ"
        else:
            hundreds_text = f"{d[hundreds][0]}ސަތޭކަ"
            
        if remainder == 0:
            return hundreds_text
        return f"{hundreds_text} {int_to_dv(remainder, False, is_spoken)}"

    if num < m:
        thousands = num // k
        remainder = num % k
        # Get the number text and convert to haas form if needed
        thousands_text = int_to_dv(thousands, True)
        for spoken_form, haas_form in haas_map.items():
            if thousands_text.endswith(spoken_form):
                thousands_text = thousands_text[:-len(spoken_form)] + haas_form
                break
        
        thousands_text = f"{thousands_text}ހާސް"
        if remainder == 0:
            return thousands_text
        return f"{thousands_text} {int_to_dv(remainder, False, is_spoken)}"

    if num < b:
        millions = num // m
        remainder = num % m
        millions_text = f"{int_to_dv(millions, True)}މިލިއަން"
        if remainder == 0:
            return millions_text
        return f"{millions_text} {int_to_dv(remainder, False, is_spoken)}"

    if num < t:
        billions = num // b
        remainder = num % b
        billions_text = f"{int_to_dv(billions, True)}ބިލިއަން"
        if remainder == 0:
            return billions_text
        return f"{billions_text} {int_to_dv(remainder, False, is_spoken)}"

    trillions = num // t
    remainder = num % t
    trillions_text = f"{int_to_dv(trillions, True)}ޓްރިލިއަން"
    if remainder == 0:
        return trillions_text
    return f"{trillions_text} {int_to_dv(remainder, False, is_spoken)}"
