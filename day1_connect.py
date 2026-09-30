import subprocess

def run_vtysh(node, command):
    result = subprocess.run(
        ["sudo", "docker", "exec", node, "vtysh", "-c", command],
        capture_output=True,
        text=True,
    )
    return result.stdout

output = run_vtysh("clab-lab1-r1", "show interface json")
print(output)