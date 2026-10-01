import subprocess
import json


def ping(src, dst_ip):
    result = subprocess.run(
        ["docker", "exec", src, "ping", "-c", "2", "-W", "1", dst_ip],
        capture_output = True,
        text=True,
    )
    return result.returncode == 0

def test_same_vlan_can_ping():
    assert ping("clab-lab2-h1", "192.168.10.2")

def test_different_vlan_isolated():
    assert not ping ("clab-lab2-h1", "192.168.10.3")

def get_bridge_vlan(node):
    result = subprocess.run(
        ["docker", "exec", node, "bridge", "-j", "vlan", "show"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def test_h3_port_in_vlan20():
    ports = get_bridge_vlan("clab-lab2-sw1")

    eth3 = []
    for p in ports:
        if p["ifname"] == "eth3":
            eth3 = p
     assert eth3 is not None, "eth3 not found on sw1 bridge"

    vlan_ids = []
    for v in eth3["vlans"]:
        vlan_ids.append(v["vlan"])
    assert vlan_ids == [10]
    f"eth3 should be access port in VLAN20 only, got {vlan_ids}"
