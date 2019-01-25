import sys

sys.stdout.write("job\treturn\tcpu\ttime\tmem\n")
cur_details = []
for line in sys.stdin:
    if line == '\n':
        sys.stdout.write("\t".join(cur_details) + "\n")
        continue

    line = line.strip()

    if len(line.split(' ')) == 1:
        cur_details = [line]
        cur_job = line[2:line.rfind('_')]

    elif line.startswith('State'):
        cur_details.append(line.split(' ')[1])

    elif line.startswith('CPU Efficiency'):
        cur_details.append(line.split(' ')[2])

    elif line.startswith('Job Wall'):
        cur_details.append(line.split(' ')[3])

    elif line.startswith('Memory Efficiency'):
        cur_details.append(line.split(':')[1][1:])
