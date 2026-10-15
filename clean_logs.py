def celsius_converter(temp_f):
    temp_f = float(temp_f)
    celsius = ((temp_f-32)/1.8)
    return celsius

def parse_and_clean(line):
    line = line.strip()
    if not line:
        return None

    parts = line.split('|')
    if len(parts) != 5:
        return None

    fields = [part.strip() for part in parts]

    if "" in fields:
        return None

    timestamp, station_id, temp_f, humidity, status = fields 

    if temp_f in ("ERROR", "N/A"):
        return None
    try:
        float(temp_f)
    except ValueError:
        return None
    if status != "ACTIVE":
        return None

    return fields

input_file = "environmental_raw.txt"
output_file = "clean_logs.csv"

skipped = 0
written = 0

with open(input_file, 'r', encoding='utf-8', errors='replace') as infile, \
    open(output_file, 'w', encoding='utf-8') as outfile:

    outfile.write("Timestamp,StationID,Temp(C),Humidity(%),Sensor_Status\n")

    for line in infile:
        fields = parse_and_clean(line)

        if fields is None:
            skipped +=1
            continue

        timestamp, station_id, temp_f, humidity, status = fields
        temp_c = celsius_converter(temp_f)

        outfile.write(f"{timestamp}, {station_id}, {temp_c}, {humidity}, {status}\n")
        written += 1

print(f"Done. Clean rows written: {written}. Corrupted lines written: {skipped}.")

