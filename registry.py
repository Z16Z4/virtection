import winreg
import re
#connecting to key in registry
access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)

access_key = winreg.OpenKey(access_registry,r"SYSTEM\HardwareConfig")
#accessing the key to open the registry directories under
for i in range(20):
   try:
       asubkey_name=winreg.EnumKey(access_key,i)
       asubkey=winreg.OpenKey(access_key, asubkey_name)
       #querying registry for the biosvendor
       BIOSVendor = winreg.QueryValueEx(asubkey, "BIOSVendor")
       #querying registry for system product name
       SystemProductName = winreg.QueryValueEx(asubkey, "SystemProductName")
       #querying registry for system version
       SystemVersion = winreg.QueryValueEx(asubkey, "SystemVersion")
       
   except:
      break
#convert to strings
bios_vendor = ''.join(str(BIOSVendor))
system_product_name_ = ''.join(str(SystemProductName))

#finding a keyword in this registry
development_kit = bios_vendor.find('Development Kit')
#alerting user
if development_kit:
    print("we found development kit")
else:
    print("no development kit found, likely the system is not using OVMF")
#finding a keyword in this registry
qemu = system_product_name_.find('Q35')
if qemu:
    print("Detected QEMU")
else:
    print("they are probably not sing qemu")
