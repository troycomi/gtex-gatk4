import sys

sys.stdout.write("job\treturn\tcpu\ttime\tmem\n")
job_details = {}
for line in sys.stdin:
    if line == '\n':
        if cur_job not in job_details:
            job_details[cur_job] = []

        job_details[cur_job].append(cur_details)

    line = line.strip()

    if line.startswith('.'):
        cur_details = [line]
        cur_job = line[2:line.rfind('_')]

    if line.startswith('State'):
        cur_details.append(line.split(' ')[1])

    if line.startswith('CPU Efficiency'):
        cur_details.append(line.split(' ')[2])

    if line.startswith('Job Wall'):
        cur_details.append(line.split(' ')[3])

    if line.startswith('Memory Efficiency'):
        cur_details.append(line.split(':')[1][1:])

for values in job_details.values():
    for l in values:
        sys.stdout.write("\t".join(l) + "\n")
