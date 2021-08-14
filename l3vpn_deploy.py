"""
Script used for MPLS L3VPN deployment using Nornir
"""

from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from rich import print as pretty
from net_utils import address, mask


def l3vpn(task):

    """
    Main function built for L3VPN deployment tasks
    """
    task1_result = task.run(
        name=f"{task.host.name}: Creating VRFs Configuration",
        task=template_file,
        template="vrf.j2",
        path="templates/",
        data=task.host["vrfs"],
    )
    vrf_config = task1_result[0].result

    task2_result = task.run(
        name=f"{task.host.name}: Configuring VRFs on PE Nodes",
        task=send_configs,
        configs=vrf_config.split("\n"),
    )

    task3_result = task.run(
        name=f"{task.host.name}: Create VRF to Interfaces Configuration",
        task=template_file,
        template=f"interfaces.j2",
        path="templates/",
        data=task.host.data,
        address=address,
        mask=mask,
    )
    int_config = task3_result[0].result

    task4_result = task.run(
        name=f"{task.host.name}: Configuring VRFs on Interfaces",
        task=send_configs,
        configs=int_config.split("\n"),
    )

    task5_result = task.run(
        name=f"{task.host.name}: Create BGP Neighbor Configuration",
        task=template_file,
        template=f"bgp.j2",
        path="templates/",
        data=task.host.data,
    )
    bgp_config = task5_result[0].result

    task6_result = task.run(
        name=f"{task.host.name}: Configuring BGP Neighbors under VRFs",
        task=send_configs,
        configs=bgp_config.split("\n"),
    )

    # Backup because, why not?
    # backup_result = task.run(name="Get Configuration", task=napalm_get, getters=["config"])

    # task.run(
    #     task=write_file,
    #     content=str(backup_result[0].result["config"]["running"]),
    #     filename=f"backups/{task.host.name}_CFG.txt",
    # )


def main():

    """
    Main that calls l3vpn function
    """

    nornir = InitNornir(config_file="config.yaml")
    pretty("Nornir initialized with the following hosts:\n")
    for host in nornir.inventory.hosts.keys():
        pretty(f"{host}\n")

    result = nornir.run(task=l3vpn)

    print_result(result)


if __name__ == "__main__":
    main()
