
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig, IPv6SubnetConfig
from ttlinks.ipservice.ip_subnet_type_classifiers import IPSubnetTypeClassifier

ip_subnet_type_classifier = IPSubnetTypeClassifier

print('IPv4 subnet types:'.center(50, '-'))
ipv4_subnet1 = IPv4SubnetConfig("192.168.0.0/16")
ipv4_subnet2 = IPv4SubnetConfig("192.168.0.0/15")
ipv4_subnet3 = IPv4SubnetConfig("224.0.0.0/4")
print('IPv4 subnet 1 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv4_subnet_types(ipv4_subnet1)])
print('IPv4 subnet 2 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv4_subnet_types(ipv4_subnet2)])
print('IPv4 subnet 3 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv4_subnet_types(ipv4_subnet3)])

print('IPv6 subnet types:'.center(50, '-'))
ipv6_subnet1 = IPv6SubnetConfig("2001:db8::/32")
ipv6_subnet2 = IPv6SubnetConfig("fe80::/64")
ipv6_subnet3 = IPv6SubnetConfig("2002::/16")
print('IPv6 subnet 1 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv6_subnet_types(ipv6_subnet1)])
print('IPv6 subnet 2 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv6_subnet_types(ipv6_subnet2)])
print('IPv6 subnet 3 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv6_subnet_types(ipv6_subnet3)])