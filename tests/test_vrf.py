import os
from nornir import InitNornir
# from nornir_netmiko import netmiko_send_command
from rich import print as pretty
from nornir_scrapli.tasks import send_command
from ntc_templates.parse import parse_output


main_vrfs = ["CUSTOMER_777", "CUSTOMER_789", "MGMT"]

# pytest -v -s --maxfail=4


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
        list_of_vrf_values = [value for elem in vrf_parsed for value in elem.values()]

        for remote_vrf in vrf_parsed:
            remote_vrfs.append(remote_vrf["name"])
        # print(remote_vrfs)
        set_diff = set(main_vrfs) - set(remote_vrfs)
        if set_diff:
            pretty(f"The following VRFs are not configured on {host}: {set_diff}")

        # for vrf in main_vrfs:
        #     if vrf in list_of_vrf_values:
        #         pretty(f"[bold blue]{vrf} VRF is configured on {host}[/bold blue]")
        #     else:
        #         pretty(f"[bold red]{vrf} VRF is not configured on {host}[/bold red]")

    # result = nornir.run(
    #     name="GET VRF",
    #     task=netmiko_send_command,
    #     command_string="show vrf",
    #     use_textfsm=True,
    # )

    # for host in nornir.inventory.hosts.keys():
    #     vrf_parsed = result[host].result
    #     list_of_vrf_values = [value for elem in vrf_parsed for value in elem.values()]

    #     print()

    #     for value in main_vrfs:
    #         if value in list_of_vrf_values:
    #             pretty(f"[bold blue]{value} VRF is configured on {host}[/bold blue]")
    #         else:
    #             pretty(f"[bold red]{value} VRF is not configured on {host}[/bold red]")


if __name__ == "__main__":
    test_vrf()
