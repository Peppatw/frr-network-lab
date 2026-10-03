import json
import subprocess
import pytest

SWITCHES = ["clab-lab3-sw1", "clab-lab3-sw2"]

def run(node, *cmd):
    return subprocess.run(
        ["docker", "exec", node, *cmd],
        capture_output=True,
        text=True,
    )

def ping(src, dst_ip):
    return run(src, "ping", "-c", "2", "-W", "1", dst_ip).returncode == 0

def get_bridge_vlans(node):
    return json.loads(run(node, "bridge", "-j", "vlan", "show").stdout)


@pytest.fixture(scope="session", autouse=True)
def lab_ready():
    for sw in SWITCHES:
        if run(sw, "ip", "link", "show", "br0").returncode != 0:
            pytest.fail(f"{sw}: br0 not found. Lab not deployed, or exec failed during deploy.")


@pytest.mark.parametrize("src, dst_ip", [
    ("clab-lab3-h1", "192.168.10.2"),
    ("clab-lab3-h1", "192.168.10.4"),
    ("clab-lab3-h2", "192.168.10.4"),
    ("clab-lab3-h3", "192.168.10.5"),
])
def test_same_vlan_reachable(src, dst_ip):
    assert ping(src, dst_ip), f"{src} should reach {dst_ip}: same VLAN"


@pytest.mark.parametrize("src, dst_ip", [
    ("clab-lab3-h1", "192.168.10.3"),
    ("clab-lab3-h1", "192.168.10.5"),
    ("clab-lab3-h3", "192.168.10.4"),
])
def test_cross_vlan_isolated(src, dst_ip):
    assert not ping(src, dst_ip), f"{src} should NOT reach {dst_ip}: different VLAN"

@pytest.mark.parametrize("sw, port", [
    ("clab-lab3-sw1", "eth4"),
    ("clab-lab3-sw2", "eth3"),
])
def test_trunk_carries_vlan10_and_20(sw, port):
    ports = get_bridge_vlans(sw)

    trunk = None
    for p in ports:
        if p["ifname"] == port:
            trunk = p
    assert trunk is not None, f"{port} not found on {sw} bridge"

    vlan_ids = []
    for v in trunk["vlans"]:
        vlan_ids.append(v["vlan"])
    assert vlan_ids == [10, 20], f"{sw} {port} should be trunk with VLAN 10 and 20, got {vlan_ids}"