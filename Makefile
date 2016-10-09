#
# Makefile
# mchristof, 2016-10-07 22:26
#

default: up

up:
	vagrant up

provision:
	vagrant provision

requirements: debops.docker

debops.docker: roles/debops.docker/
	ansible-galaxy install debops.docker
	

clean:
	vagrant destroy -f

squid:
	ansible-playbook setup.yml -t squid -b -e squid=true

test:
	ansible-playbook setup.yml -t test

all:
	@echo "Makefile needs your attention"


# vim:ft=make
#
