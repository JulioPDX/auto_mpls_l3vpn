import os
import yaml
from rich import print as pretty
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from ntc_templates.parse import parse_output


main_vrfs = []

# Create list of VRFs defined in groups.yaml
with open("groups.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)["pe"]["data"]["vrfs"]
    for vrf in data:
        main_vrfs.append(vrf["name"])


def test_vrf():

    """
    Main VRF test
    """
    os.environ[
        "NET_TEXTFSM"
    ] = "./venv/lib/python3.9/site-packages/ntc_templates/templates"

    nornir = InitNornir(config_file="config.yaml")

    result = nornir.run(
        name="GET VRF",
        task=send_command,
        command="show vrf",
    )

    for host in nornir.inventory.hosts.keys():
        remote_vrfs = []
        vrf_parsed = parse_output(
            platform="cisco_ios", command="show vrf", data=result[host].result
        )

        # Looping over all parsed VRFs to build new list
        for remote_vrf in vrf_parsed:
            remote_vrfs.append(remote_vrf["name"])

        set_diff = set(main_vrfs) - set(remote_vrfs)

        # If a set difference is found, print the nice red output!
        if set_diff:
            pretty(
                f"[bold red]The following VRFs are not configured on {host}: {set_diff}[/bold red]"
            )
        else:
            pretty(f"[bold blue]All VRF tests passed on router {host}[/bold blue]")


if __name__ == "__main__":
    test_vrf()
