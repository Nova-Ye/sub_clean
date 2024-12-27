import re

def process_vtt(lines):
    # Step 1: Remove lines containing '</c>'
    lines = [line for line in lines if "</c>" not in line]

    # Step 2: Remove "align:start position:0%" and trailing whitespace
    lines = [line.split(" align:start position:0%")[0].strip() for line in lines]

    # Step 3: Remove empty lines
    lines = [line for line in lines if line]

    return lines

def merge_timelines(lines):
    pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})(.+)"
    time_sub_pairs = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            start_time, end_time, sub = match.groups()
            time_sub_pairs.append((start_time, end_time, sub.strip()))

    merged_pairs = []
    for start_time, end_time, sub in time_sub_pairs:
        if merged_pairs and merged_pairs[-1][2] == sub:
            # Combine timelines: use earliest start time and latest end time
            merged_pairs[-1] = (merged_pairs[-1][0], end_time, sub)
        else:
            # Add as a new entry
            merged_pairs.append((start_time, end_time, sub))

    return merged_pairs
