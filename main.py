import os, re, sys, subprocess, psutil, fileinput
import cpuid, struct, keyboard
import display, registry, windows, linux
def main():
    display.loading()
    display.print_banner()
    print("\n")
    pause = input("Press enter to start..")
    if os.name == "nt":
        windows.process_check()
        windows.hypervisor_check()
        windows.memory_check()
        windows.disk_check()
        windows.rdstc_check()
        windows.registry_check()
        windows.driver_check()
        windows.username_check()
        windows.hostname_check()
        #windows.guest_additions_check()
    else:
        linux.guest_check()
        linux.memory_check()
        linux.disk_check()
        linux.docker_check()
    display.menu()


if __name__ == "__main__":
    main()

#TODO detect linux & windows in virtualbox and vmware
#TODO detect files related to virtualisation in linux host
#TODO detect iommu on host system, assist in applying patches all linux
