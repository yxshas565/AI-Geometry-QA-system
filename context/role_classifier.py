# context/role_classifier.py

def classify_line_role(features):
    length = features["total_length"]
    num_points = features["num_points"]

    if length < 10 and num_points <= 3:
        return "CONNECTOR"
    elif length > 100 and num_points > 10:
        return "BACKBONE"
    else:
        return "STANDARD"
